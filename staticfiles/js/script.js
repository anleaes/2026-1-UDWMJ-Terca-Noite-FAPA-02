document.addEventListener('DOMContentLoaded', function () {
    initMobileNavAutoClose();
    initReservationDateValidation();
    initRequiredFieldHighlight();
});

function initMobileNavAutoClose() {
    document.addEventListener('click', function (event) {
        const link = event.target.closest('.nav-links .nav-link');
        const mobileNav = document.querySelector('.nav-mobile-toggle');

        if (!link || !mobileNav || !mobileNav.open) {
            return;
        }

        mobileNav.open = false;
    });
}

function initReservationDateValidation() {
    const checkInInputs = document.querySelectorAll('input[name="check_in"]');
    const checkOutInputs = document.querySelectorAll('input[name="check_out"]');

    if (checkInInputs.length === 0 || checkOutInputs.length === 0) {
        return;
    }

    const today = new Date().toISOString().split('T')[0];
    checkInInputs.forEach(function (input) {
        input.setAttribute('min', today);
    });

    function validateDates(form) {
        const checkIn = form.querySelector('input[name="check_in"]');
        const checkOut = form.querySelector('input[name="check_out"]');
        if (!checkIn || !checkOut) return true;

        if (checkOut.value && checkIn.value && checkOut.value <= checkIn.value) {
            alert('A data de check-out precisa ser depois do check-in.');
            return false;
        }
        return true;
    }

    document.querySelectorAll('form').forEach(function (form) {
        if (form.querySelector('input[name="check_in"]')) {
            form.addEventListener('submit', function (event) {
                if (!validateDates(form)) {
                    event.preventDefault();
                }
            });
        }
    });
}

function initRequiredFieldHighlight() {
    document.querySelectorAll('input[required], select[required], textarea[required]').forEach(function (field) {
        field.addEventListener('invalid', function () {
            field.classList.add('field-invalid');
        });
        field.addEventListener('input', function () {
            field.classList.remove('field-invalid');
        });
    });
}
