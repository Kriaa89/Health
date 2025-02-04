// Handle role and gender selection styling
document.addEventListener('DOMContentLoaded', function() {
    // Role selection
    const roleRadios = document.querySelectorAll('.role-radio');
    roleRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            // Remove selected class from all options
            document.querySelectorAll('.role-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            // Add selected class to chosen option
            if (this.checked) {
                this.nextElementSibling.classList.add('selected');
            }
        });

        // Initialize selected state
        if (radio.checked) {
            radio.nextElementSibling.classList.add('selected');
        }
    });

    // Gender selection
    const genderRadios = document.querySelectorAll('.gender-radio');
    genderRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            // Remove selected class from all options
            document.querySelectorAll('.gender-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            // Add selected class to chosen option
            if (this.checked) {
                this.nextElementSibling.classList.add('selected');
            }
        });

        // Initialize selected state
        if (radio.checked) {
            radio.nextElementSibling.classList.add('selected');
        }
    });

    // Phone number formatting
    const phoneInput = document.querySelector('input[name="phone_number"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            // Remove any non-digit characters
            let value = this.value.replace(/\D/g, '');
            // Limit to 8 digits
            if (value.length > 8) {
                value = value.slice(0, 8);
            }
            // Update input value
            this.value = value;
        });
    }
});
