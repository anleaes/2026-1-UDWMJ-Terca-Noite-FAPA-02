document.addEventListener('DOMContentLoaded', function () {
    initMobileNavAutoClose();
    initReservationDateValidation();
    initRequiredFieldHighlight();
    initPropertyCarousel();
    initRoomCalculators();
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

function initPropertyCarousel() {
    const carousel = document.querySelector('[data-carousel]');
    if (!carousel) {
        return;
    }

    const track = carousel.querySelector('[data-carousel-viewport]');
    const previousButton = carousel.querySelector('[data-carousel-prev]');
    const nextButton = carousel.querySelector('[data-carousel-next]');

    if (!track || !previousButton || !nextButton) {
        return;
    }

    const getSlideStep = function () {
        const slide = track.querySelector('.carousel__slide');
        if (!slide) {
            return track.clientWidth;
        }

        const slideStyles = window.getComputedStyle(track);
        const gap = parseFloat(slideStyles.columnGap || slideStyles.gap || '0') || 0;
        return slide.getBoundingClientRect().width + gap;
    };

    previousButton.addEventListener('click', function () {
        track.scrollBy({ left: -getSlideStep(), behavior: 'smooth' });
    });

    nextButton.addEventListener('click', function () {
        track.scrollBy({ left: getSlideStep(), behavior: 'smooth' });
    });
}

function initRoomCalculators() {
    const roomCards = document.querySelectorAll('[data-room-card]');
    if (roomCards.length === 0) {
        return;
    }

    const today = new Date();
    const todayValue = today.toISOString().split('T')[0];

    function formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
    }

    function calculateNights(checkInValue, checkOutValue) {
        if (!checkInValue || !checkOutValue) {
            return 0;
        }

        const checkIn = new Date(checkInValue);
        const checkOut = new Date(checkOutValue);
        const diff = checkOut.getTime() - checkIn.getTime();

        if (Number.isNaN(diff) || diff <= 0) {
            return 0;
        }

        return Math.round(diff / (1000 * 60 * 60 * 24));
    }

    roomCards.forEach(function (card) {
        const dailyRate = parseFloat(card.dataset.dailyRate || '0') || 0;
        const checkInInput = card.querySelector('[data-room-check-in]');
        const checkOutInput = card.querySelector('[data-room-check-out]');
        const totalOutput = card.querySelector('[data-room-total]');
        const nightsOutput = card.querySelector('[data-room-nights]');

        if (!checkInInput || !checkOutInput || !totalOutput || !nightsOutput) {
            return;
        }

        checkInInput.min = todayValue;

        function updateMinimumCheckout() {
            if (checkInInput.value) {
                checkOutInput.min = checkInInput.value;
            } else {
                checkOutInput.min = todayValue;
            }
        }

        function updateTotal() {
            updateMinimumCheckout();

            const nights = calculateNights(checkInInput.value, checkOutInput.value);
            if (nights <= 0) {
                totalOutput.textContent = formatCurrency(0);
                nightsOutput.textContent = 'Escolha as datas para calcular o valor.';
                return;
            }

            totalOutput.textContent = formatCurrency(nights * dailyRate);
            nightsOutput.textContent = `${nights} noite${nights > 1 ? 's' : ''} selecionada${nights > 1 ? 's' : ''}`;
        }

        checkInInput.addEventListener('change', updateTotal);
        checkOutInput.addEventListener('change', updateTotal);
        updateTotal();
    });
}
