// authorize.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        // Clear previous messages
        document.getElementById('emailError').innerHTML = '';
        document.getElementById('passwordError').innerHTML = '';
        document.getElementById('successMessage').innerHTML = '';

        // Get form inputs
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        let isFormValid = true;

        // Validate fields
        if (email === '') {
            document.getElementById('emailError').innerHTML = 'Email is required.';
            isFormValid = false;
        }
        if (password === '') {
            document.getElementById('passwordError').innerHTML = 'Password is required.';
            isFormValid = false;
        }

        if (isFormValid) {
            try {
                // Send AJAX request
                const response = await fetch('/login_submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (data.success) {
                    // Display success message
                    document.getElementById('successMessage').innerHTML = data.message;

                    // Redirect after a short delay to allow the user to read the message
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1500); // 1.5 seconds delay
                } else {
                    // Display error message
                    if (data.message.toLowerCase().includes('email')) {
                        document.getElementById('emailError').innerHTML = data.message;
                    } else if (data.message.toLowerCase().includes('password')) {
                        document.getElementById('passwordError').innerHTML = data.message;
                    } else {
                        // General error message
                        document.getElementById('passwordError').innerHTML = data.message;
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('passwordError').innerHTML = 'An unexpected error occurred.';
            }
        }
    });
});