
var body = document.querySelector("body")

var profile =  document.querySelector(".navbar .profile")
var leaf = profile.querySelector('.flex-col')


profile.addEventListener("click", ()=> {        // Open and closes the profile leaf
    leaf.style.display == 'none' ? leaf.style.display ='flex' : leaf.style.display = 'none'
})


var adminTasks = document.querySelectorAll(".container .admin-dash")
var action = document.querySelector(".container .acts")
var container = action.parentElement

