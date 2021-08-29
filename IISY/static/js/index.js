const infoScreen = document.querySelector(".info-screen")

const infoBtn = document.querySelector("[data-js='info-btn']")
infoBtn.addEventListener("click", function () {
    if (!infoScreen.classList.contains("is-showing")) {
        infoBtn.textContent = "X"
    } else {
        infoBtn.textContent = "i"
    }
    infoScreen.classList.toggle("is-showing")
})

const tipsLink = document.querySelector("#tips-link")
const tipsModal = document.querySelector("#tips-modal")
const tipsModalCloseBtn = document.querySelector("#tips-modal-close")
const screenOverlay = document.querySelector("#screen-overlay")
tipsLink.addEventListener("click", function () {
    if (!tipsModal.classList.contains("is-showing")) {
        tipsModal.classList += " is-showing"
        screenOverlay.classList += " is-showing"
    }
})
tipsModalCloseBtn.addEventListener("click", function () {
    tipsModal.classList.remove("is-showing")
    screenOverlay.classList.remove("is-showing")
})