// Show/hide password functionality
document.addEventListener('DOMContentLoaded', function() {
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

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });

    // Initialize all tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

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
});
