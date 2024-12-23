function validateForm(event) {
    event.preventDefault(); // Prevent form submission

    // Clear all error messages
    document.getElementById('nameError').innerHTML = '';
    document.getElementById('emailError').innerHTML = '';
    document.getElementById('phoneError').innerHTML = '';
    document.getElementById('passwordError').innerHTML = '';
    document.getElementById('repeatPasswordError').innerHTML = '';
    document.getElementById('userTypeError').innerHTML = '';
    document.getElementById('heardAboutError').innerHTML = '';
    document.getElementById('privacyError').innerHTML = '';
    document.getElementById('successMessage').innerHTML = '';

    // Select all required elements
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const repeatPassword = document.getElementById('repeat_password');
    const userType = document.querySelector('input[name="userType"]:checked');
    const heardAbout = document.getElementById('heardAbout');
    const privacy = document.getElementById('privacy');
    const phone = document.getElementById('phone');

    let isFormValid = true;

    // Validate each field
    if (name.value === '') {
        document.getElementById('nameError').innerHTML = 'Name is required.';
        isFormValid = false;
    }

    if (email.value === '') {
        document.getElementById('emailError').innerHTML = 'Email is required.';
        isFormValid = false;
    }

    if (phone.value === '') {
        document.getElementById('phoneError').innerHTML = 'Phone number is required.';
        isFormValid = false;
    } else if (!(/^\d{10}$/.test(phone.value))) {
        document.getElementById('phoneError').innerHTML = 'Please enter a valid 10-digit phone number.';
        isFormValid = false;
    }

    if (password.value === '') {
        document.getElementById('passwordError').innerHTML = 'Password is required.';
        isFormValid = false;
    }

    if (repeatPassword.value === '') {
        document.getElementById('repeatPasswordError').innerHTML = 'Please repeat your password.';
        isFormValid = false;
    } else if (password.value !== repeatPassword.value) {
        document.getElementById('repeatPasswordError').innerHTML = 'Passwords do not match.';
        isFormValid = false;
    }

    if (!userType) {
        document.getElementById('userTypeError').innerHTML = 'Please select a user type.';
        isFormValid = false;
    }

    if (heardAbout.value === '') {
        document.getElementById('heardAboutError').innerHTML = 'Please select how you heard about us.';
        isFormValid = false;
    }

    if (!privacy.checked) {
        document.getElementById('privacyError').innerHTML = 'You must agree to the privacy policy and terms.';
        isFormValid = false;
    }

    // If form is valid, display success message
    if (isFormValid) {
        document.getElementById('successMessage').innerHTML = 'Form submitted successfully!';
        // Here you can add code to handle form submission
    }

    if (isFormValid) {
        document.getElementById('successMessage').innerHTML = 'Form submitted successfully!';
        document.getElementById('registration-form').submit(); // Manually submit the form
    }
}