document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded.');
});


setTimeout(function() {
    var flashMessages = document.getElementsByClassName('flash-message');
    for (var i = 0; i < flashMessages.length; i++) {
        flashMessages[i].style.display = 'none';
    }
}, 3000); // 3000 milliseconds = 5 seconds




// //////////////////////////////////
// /////////////////////////////////////////////////


// const usernameEl = document.querySelector('#name');
// const emailEl = document.querySelector('#email');
// const passwordEl = document.querySelector('#password');
// // const confirmPasswordEl = document.querySelector('#confirm-password');
// const form_1 = document.querySelector('#signupForm');

// form_1.addEventListener('input', function (e) {
//     switch (e.target.id) {
//         case 'name':
//             checkUsername();
//             break;
//         case 'email':
//             checkEmail();
//             break;
//         case 'password':
//             checkPassword();
//             break;
//         // case 'confirm-password':
//         //     checkConfirmPassword();
//         //     break;
//     }
// });

// const isRequired = value => value === '' ? false : true;
// const isBetween = (length, min, max) => length < min || length > max ? false : true;
// const isEmailValid = (email) => {
//     const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
//     return re.test(email);
// };

// const isPasswordSecure = (password) => {
//     const re = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
//     return re.test(password);
// };

// // Password RegEx	Meaning
// // ^	The password starts
// // (?=.*[a-z])	The password must contain at least one lowercase character
// // (?=.*[A-Z])	The password must contain at least one uppercase character
// // (?=.*[0-9])	The password must contain at least one number
// // (?=.*[!@#$%^&*])	The password must contain at least one special character.
// // (?=.{8,})	The password must be eight characters or longer

// const showError = (input, message) => {
//     // get the form-field element
//     const formField = input.parentElement;
//     // add the error class
//     formField.classList.remove('success');
//     formField.classList.add('error');

//     // show the error message
//     const error = formField.querySelector('small');
//     error.textContent = message;
// };


// const showSuccess = (input) => {
//     // get the form-field element
//     const formField = input.parentElement;

//     // remove the error class
//     formField.classList.remove('error');
//     formField.classList.add('success');

//     // hide the error message
//     const error = formField.querySelector('small');
//     error.textContent = '';
// }

// const checkUsername = () => {

//     let valid = false;
//     const min = 3,
//         max = 25;
//     const username = usernameEl.value.trim();

//     if (!isRequired(username)) {
//         showError(usernameEl, 'Username cannot be blank.');
//     } else if (!isBetween(username.length, min, max)) {
//         showError(usernameEl, `Username must be between ${min} and ${max} characters.`)
//     } else {
//         showSuccess(usernameEl);
//         valid = true;
//     }
//     return valid;
// }


// const checkEmail = () => {
//     let valid = false;
//     const email = emailEl.value.trim();
//     if (!isRequired(email)) {
//         showError(emailEl, 'Email cannot be blank.');
//     } else if (!isEmailValid(email)) {
//         showError(emailEl, 'Email is not valid.')
//     } else {
//         showSuccess(emailEl);
//         valid = true;
//     }
//     return valid;
// }

// const checkPassword = () => {

//     let valid = false;

//     const password = passwordEl.value.trim();

//     if (!isRequired(password)) {
//         showError(passwordEl, 'Password cannot be blank.');
//     } else if (!isPasswordSecure(password)) {
//         showError(passwordEl, 'Password must has at least 8 characters that include at least 1 lowercase character, 1 uppercase characters, 1 number, and 1 special character in (!@#$%^&*)');
//     } else {
//         showSuccess(passwordEl);
//         valid = true;
//     }

//     return valid;
// };