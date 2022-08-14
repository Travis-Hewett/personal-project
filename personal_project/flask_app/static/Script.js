const primaryNav = document.querySelector('.primary-nav');
const navToggle = document.querySelector('.mobile-nav-toggle');

navToggle.addEventListener("click", () => {
    const visibility = primaryNav.getAttribute('data-visible')

    if (visibility === "false") {
        primaryNav.setAttribute('data-visible', true);
        navToggle.setAttribute('aria-visible', true);
    } else if (visibility === "true") {
        primaryNav.setAttribute('data-visible', false );
        navToggle.setAttribute('aria-visible', false);
    }
});





// document.addEventListener("click", e => {
//     const isDropdownButton = e.target.matches("[data-dropdown-button]")
//     if (!isDropdownButton && e.target.closest('[data-dropdown]') != null) return

//     let currentDropdown
//     if(isDropdownButton){
//         currentDropdown = e.target.closest('[data-dropdown]')
//         currentDropdown.classList.toggle('active')
//     }

//     document.querySelectorAll("[data-dropdown].active").forEach(dropdown =>{
//         if (dropdown === currentDropdown) return
//         dropdown.classList.remove("active")
//     })
// })

// #divide here

// const tabs = document.querySelectorAll('[data-tab-target]')
// const tabContents = document.querySelectorAll('[data-tab-content]')

// tabs.forEach(tab => {
//     tab.addEventListener('click', () => {
//     const target = document.querySelector(tab.dataset.tabTarget)
//     tabContents.forEach(tabContent => {
//         tabContent.classList.remove('active')
//     })
//     tabs.forEach(tab => {
//         tab.classList.remove('active')
//     })
//     tab.classList.add('active')
//     target.classList.add('active')
//     })
// })