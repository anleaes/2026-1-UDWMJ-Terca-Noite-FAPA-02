document.addEventListener('click', (event) => {
    const link = event.target.closest('.nav-links .nav-link');
    const mobileNav = document.querySelector('.nav-mobile-toggle');

    if (!link || !mobileNav || !mobileNav.open) {
        return;
    }

    if (window.matchMedia('(max-width: 768px)').matches) {
        mobileNav.open = false;
    }
});
