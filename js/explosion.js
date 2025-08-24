const fadeWrapper = document.getElementById('fade-wrapper');

document.querySelectorAll('main a').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();
        const href = link.getAttribute('href');

        fadeWrapper.classList.add('explode');

        setTimeout(() => {
            window.location.href = href;
        }, 800); // matches CSS
    });
});
