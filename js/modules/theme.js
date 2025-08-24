export function setupThemeToggle() {
    const toggleBtn = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');
    const htmlEl = document.documentElement;
    const themeMeta = document.getElementById('theme-color-meta');

    const updateIcons = (dark) => {
        sunIcon.classList.toggle('hidden', dark);
        moonIcon.classList.toggle('hidden', !dark);
        toggleBtn.setAttribute('aria-pressed', dark);
        themeMeta.setAttribute('content', dark ? '#0f172a' : '#ffffff');
    };

    const storedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = storedTheme === 'dark' || (!storedTheme && prefersDark);
    htmlEl.classList.toggle('dark', isDark);
    updateIcons(isDark);

    toggleBtn.addEventListener('click', () => {
        const isCurrentlyDark = !htmlEl.classList.contains('dark');
        htmlEl.classList.toggle('dark', isCurrentlyDark);
        localStorage.setItem('theme', isCurrentlyDark ? 'dark' : 'light');
        updateIcons(isCurrentlyDark);
    });
}