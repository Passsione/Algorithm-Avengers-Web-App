
var body = document.querySelector("body")

var profile =  document.querySelector(".navbar .profile")
var leaf = profile.querySelector('.flex-col')


profile.addEventListener("click", ()=> {        // Open and closes the profile leaf
    leaf.style.display == 'none' ? leaf.style.display ='flex' : leaf.style.display = 'none'
})


// var adminTasks = document.querySelectorAll(".container .admin-dash")
// var container = adminTasks[0].parentElement
// var action = document.querySelectorAll(".container .acts")

//     adminTasks.forEach( (at) => {
//         at.addEventListener("click", () =>{
//             if(container.dataset.tab != at.id){
//                 at.style.display = 'none'
//             }else{at.style.display = 'grid'}
//         })
//     });

//     action.addEventListener("click", () =>{
        
//     })

