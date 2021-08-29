const mobileNavLinks = document.querySelector("#navbar-mobile__dropdown")
const hamburger = document.querySelector("#hamburger")
hamburger.addEventListener("click", () => {
    mobileNavLinks.classList.toggle("is-showing")
})