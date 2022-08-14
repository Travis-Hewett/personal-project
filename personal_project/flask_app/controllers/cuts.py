from flask_app import app # Needed for @app.route() among other things
from flask_app.models import user, cut # Import models
from flask import render_template, redirect, request, session # Import methods from Flask



#visible routes
@app.route('/new')
def new_cut_page():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template('new_cut_page.html', this_user = user.User.get_user_by_id(data))

# route to take you to who_we_are
@app.route("/whoWeAre")
def who_we_are():
    return render_template("who_we_are.html")

# route to take you to about our beef
@app.route("/aboutbeef")
def about_beef():
    return render_template("aboutbeef.html")

#view one cut page
@app.route('/show/<int:id>')
def view_cut_page(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": id
    }
    return render_template('view_one_cut.html', this_user_with_cuts = cut.Cut.get_cuts_by_this_user(data), this_cut = cut.Cut.get_one_cut_with_user(data))

#Invisible route
#deleat cut
@app.route('/<int:id>/delete')
def delete_cut(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": id
    }
    cut.Cut.delete_cut(data)
    return redirect('/dashboard')

#add a cut
@app.route('/cuts/add_to_db', methods = ['POST'])
def add_cut_to_db():
    if "user_id" not in session:
        return redirect('/')
    if not cut.Cut.validate_cut(request.form): #if validations fail
        return redirect('/new') #send back to the form
        #add cut to the db via the model
    data = {
        'cut_of_beef': request.form['cut_of_beef'],
        'special_instructions': request.form['special_instructions'],
        'user_id': session['user_id'], #id of person logged in
    }
    cut.Cut.add_cut(data)
        #redirect to dashboard
    return redirect('/dashboard')

#edit a cut Post
@app.route('/cuts/<int:id>/edit_in_db', methods = ['POST'])
def edit_cut_in_db(id):
    if "user_id" not in session:
        return redirect('/')
    if not cut.Cut.validate_cut(request.form): #if validations fail
        return redirect(f'/cuts/{id}/edit') #send back to the form
        #edit the cut to the db via the model
    data = {
        'cut_of_beef': request.form['cut_of_beef'],
        'special_instructions': request.form['special_instructions'],
        "id": id
    }
    cut.Cut.edit_cut(data)
    return redirect("/dashboard")

#edit a cut Get
@app.route('/<int:id>/edit')
def edit_cut(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template('edit_cut.html', this_user = user.User.get_user_by_id(data))

