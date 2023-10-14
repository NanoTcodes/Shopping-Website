// Get the navbar
var navbar = document.querySelector(".navbar");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Function to make the navbar sticky
function makeNavbarSticky() {
    if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky");
    } else {
        navbar.classList.remove("sticky");
    }
}

// Attach the function to the scroll event
window.onscroll = function() {
    makeNavbarSticky();
};
