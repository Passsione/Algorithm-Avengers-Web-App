const searchEl = document.querySelector()

/* search bar function*/


    function search_items() {
        let input = document.getElementById('searchbar');  // Get the search bar input element
        let filter = input.value.toLowerCase();  // Get the value of the input field (convert to lowercase for case-insensitive search)
        let list = document.getElementById('list');  // Get the list of items
        let items = list.getElementsByTagName('li');  // Get all the <li> elements in the list

        // Loop through all list items and hide those that don't match the search query
        for (let i = 0; i < items.length; i++) {
            let item = items[i];
            let text = item.textContent || item.innerText;  // Get the text of the current item
            if (text.toLowerCase().indexOf(filter) > -1) {
                item.style.display = "";  // Show the item if it matches the search query
            } else {
                item.style.display = "none";  // Hide the item if it does not match the search query
            }
        }
    }

/* login function*/

function login() {
  // Simulate login validation (replace with your actual server-side logic)
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (username === "user" && password === "pass") { // Example credentials
    window.location.href = "welcome.html"; // Redirect to welcome page
  } else {
    alert("Invalid username or password");
  }
}