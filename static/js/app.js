// Common utilities for MedHealth application
document.addEventListener('DOMContentLoaded', function() {
    // Show/hide password functionality
    const togglePassword = document.querySelector('.toggle-password');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const password = document.querySelector(this.getAttribute('toggle'));
            if (password.type === 'password') {
                password.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                password.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    }

    // Auto-hide alerts after 5 seconds using Bootstrap Alert API
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                // Fallback for when Bootstrap JS is not available
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.style.display = 'none';
                }, 500);
            }
        }, 5000);
    });

    // Initialize all tooltips
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Role selection in registration
    const roleOptions = document.querySelectorAll('.role-option');
    const roleRadios = document.querySelectorAll('.role-radio');
    
    roleOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            const radio = this.previousElementSibling;
            radio.checked = true;
            roleOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    if (roleRadios.length > 0) {
        // Initialize selected state
        roleRadios.forEach(radio => {
            if (radio.checked) {
                radio.nextElementSibling.classList.add('selected');
            }
        });
    }

    // Gender selection in registration
    const genderOptions = document.querySelectorAll('.gender-option');
    const genderRadios = document.querySelectorAll('.gender-radio');
    
    genderOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            const radio = this.previousElementSibling;
            radio.checked = true;
            genderOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    if (genderRadios.length > 0) {
        // Initialize selected state
        genderRadios.forEach(radio => {
            if (radio.checked) {
                radio.nextElementSibling.classList.add('selected');
            }
        });
    }

    // Phone number formatting
    const phoneInput = document.querySelector('input[name="phone_number"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            // Remove any non-digit characters
            let value = this.value.replace(/\D/g, '');
            // Limit to 10 digits
            if (value.length > 10) {
                value = value.slice(0, 10);
            }
            // Format phone number: (XXX) XXX-XXXX
            if (value.length > 6) {
                this.value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
            } else if (value.length > 3) {
                this.value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
            } else if (value.length > 0) {
                this.value = `(${value}`;
            } else {
                this.value = '';
            }
        });
    }
});