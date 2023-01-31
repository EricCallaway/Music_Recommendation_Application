const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("login-error-msg");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    if (username === "user" && password === "user") {
        // alert("You have successfully logged in.");
        window.location.href = "/Users/ericcallaway/Google Drive/School Work/Spring 2023/Final_Year_Project/Music_Recommnedation_Application/website/main.html"
    } else {
        loginErrorMsg.style.opacity = 1;
    }
})