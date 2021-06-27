"use strict";

document.querySelector('#login-button').addEventListener('click', (evt) => {
    evt.preventDefault();

    const formData = {
        email: $('#email').val(),
        password: $('#password').val()
    };

    $.post('/login', formData, (res) => {
        if (res === "Not found") {
            Toastify({
                text: "An account for this email doesn't exist yet.",
                duration: 700,
                backgroundColor: "linear-gradient(to right, #874006, #330C04)",
                className: "info",
                }).showToast();
        }
        else if (res === 'Wrong password') {
            Toastify({
                text: 'Wrong password. Please try again.',
                duration: 2000,
                backgroundColor: "linear-gradient(to right, #874006, #330C04)"
                }).showToast();
        }
        else if (res === 'Logged in') {
            Toastify({
                text: 'Logged in!',
                duration: 2000,
                backgroundColor: "linear-gradient(to right, #BB6606, #693B08)"
                }).showToast();
                setTimeout(() => {window.location.href='/user-page'}, 2000);
        }
    })
});
