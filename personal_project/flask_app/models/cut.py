from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash # Need this for validating the form data



class Cut:
    db_name = "personal"

    def __init__(self,data): # data is a DICTIONARY
        self.id = data["id"]
        self.cut_of_beef = data["cut_of_beef"]
        self.special_instructions = data["special_instructions"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None #Link a user to this beef

    @classmethod
    def add_cut(cls, data):
        query = "INSERT INTO cuts ( cut_of_beef, special_instructions, user_id) VALUES ( %(cut_of_beef)s, %(special_instructions)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def edit_cut(cls, data):
        query = "UPDATE cuts SET cut_of_beef = %(cut_of_beef)s, special_instructions = %(special_instructions)s, WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_cut(cls, data):
        query = "DELETE FROM cuts WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_cuts_with_users(cls):
        query = "SELECT * FROM cuts JOIN users ON cuts.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results, "HELLOHELLOHELLOHELLOHELLOHELLOHELLOHELLOHELLO")
        if len(results) == 0:
            return[] #return empty list
        else: #at least one cut exists
            all_cuts = [] #list of cuts(as objects)
            for this_cut_dictionary in results:
                #create the cut object
                this_cut_object = cls(this_cut_dictionary) #cls() calls on the __init__ method inside this class
                #grab the user data linked to this cut
                this_user_dictionary = {
                    'id' : this_cut_dictionary["users.id"],
                    'first_name' : this_cut_dictionary["first_name"],
                    'last_name' : this_cut_dictionary["last_name"],
                    'email' : this_cut_dictionary["email"],
                    'password' : this_cut_dictionary["password"],
                    'created_at' : this_cut_dictionary["users.created_at"],
                    'updated_at' : this_cut_dictionary["users.updated_at"],
                }
                #create the User object
                this_user_object = user.User(this_user_dictionary)
                #link the user to the cut
                this_cut_object.user = this_user_object
                #Add that cut to the list of cuts
                all_cuts.append(this_cut_object)
            return all_cuts

    @classmethod
    def get_one_cut_with_user(cls, data):
        query = "SELECT * FROM cuts JOIN users ON cuts.user_id = users.id WHERE cuts.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else: #at least one cut exists
            #create the cut object
            this_cut_object = cls(results[0]) #results[0] represents a dictionary at index 0 in the list called 'results'
            #grab the user data linked to this cut
            this_user_dictionary = {
                'id' : results[0]["users.id"],
                'first_name' : results[0]["first_name"],
                'last_name' : results[0]["last_name"],
                'email' : results[0]["email"],
                'password' : results[0]["password"],
                'created_at' : results[0]["users.created_at"],
                'updated_at' : results[0]["users.updated_at"],
            }
            #create the User object
            this_user_object = user.User(this_user_dictionary)
            #link the user to the cut
            this_cut_object.user = this_user_object
            return this_cut_object

    @classmethod
    def get_cuts_by_this_user(cls, data):
        query = "SELECT * FROM users LEFT JOIN cuts ON user_id = cuts.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else:
            #create teh user object
            this_user = user.User(results[0])
            #if we have at least one cut, go through each cut
            if results[0]["cuts.id"] != None: #if we have at least one cut found we can loop through the cuts
                #loop through all the cuts
                for this_cut_dictionary in results:
                    #grab the cut data as a seperate dictionary
                    new_cut_dictionary = {
                        "id" : this_cut_dictionary["cuts.id"],
                        "cut_of_beef" : this_cut_dictionary["cut_of_beef"],
                        "special_instructions" : this_cut_dictionary["special_instructions"],
                        "created_at" : this_cut_dictionary["cuts.created_at"],
                        "updated_at" : this_cut_dictionary["cuts.updated_at"],
                    }
                    #create the cut
                    this_cut_object = cls(new_cut_dictionary)
                    #add the cut to the list of cuts for this User
                    this_user.cuts.append(this_cut_object)
            #return the user
            return this_user

    @staticmethod #vaildation
    def validate_cut(form_data):
        is_valid = True
        print(form_data)
        #check cut name
        if len(form_data['cut_of_beef'])<2:
            is_valid = False
            flash('cut name must be more than two characters')
        #check the special_instructions
        if len(form_data['special_instructions'])<10:
            is_valid = False
            flash('special_instructions must be more than ten characters')
        # if 'food' not in form_data: #radio button check
        #     is_valid = False
        #     flash('please chose yes or no')
        return is_valid
