function initPage() {
    // Theme toggle logic
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

    // PWA Service Worker Registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service-worker.js')
                .then(reg => console.log('Service Worker registered!', reg))
                .catch(err => console.error('Service Worker registration failed:', err));
        });
    }

    // Map logic
    const savedState = JSON.parse(localStorage.getItem('mapState')) || { lat: 0, lon: 0, zoom: 2 };

    // Remove existing map if any (bfcache restoration)
    if (window._mapInstance) {
        window._mapInstance.remove();
    }

    const map = L.map('map', {
        zoomControl: false, 
        scrollWheelZoom: true,
        dragging: true,
    }).setView([savedState.lat, savedState.lon], savedState.zoom);

    window._mapInstance = map;

    L.tileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        { maxZoom: 19, attribution: '' }
    ).addTo(map);

    L.control.zoom({ position: 'bottomright' }).addTo(map);

    const issIcon = L.icon({
        iconUrl: 'https://icons.iconarchive.com/icons/goodstuff-no-nonsense/free-space/512/international-space-station-icon.png',
        iconSize: [40, 40],
        iconAnchor: [20, 20]
    });
    const issMarker = L.marker([0, 0], { icon: issIcon }).addTo(map);

    const terminator = L.terminator().addTo(map);

    async function updateMap() {
        try {
            const res = await fetch('https://api.wheretheiss.at/v1/satellites/25544');
            if (!res.ok) throw new Error('Network response was not ok');
            const data = await res.json();
            const lat = data.latitude;
            const lon = data.longitude;
            issMarker.setLatLng([lat, lon]);

            map.panTo([lat, lon]);
        } catch(e) {
            console.error('ISS fetch error:', e);
        }
        terminator.setTime();

        localStorage.setItem('mapState', JSON.stringify({
            lat: map.getCenter().lat,
            lon: map.getCenter().lng,
            zoom: map.getZoom(),
        }));
    }

    const userLocationBtn = document.getElementById('user-location-btn');
    let userMarker = null;
    const savedUserLocation = JSON.parse(localStorage.getItem('userLocation'));

    if (savedUserLocation) {
        userMarker = L.marker([savedUserLocation.lat, savedUserLocation.lon]).addTo(map)
            .bindPopup('You are here!').openPopup();
    }

    userLocationBtn.addEventListener('click', () => {
        if (!navigator.geolocation) {
            alert('Geolocation is not supported by your browser.');
            return;
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                const userLatLng = [latitude, longitude];

                if (userMarker) {
                    userMarker.setLatLng(userLatLng);
                } else {
                    userMarker = L.marker(userLatLng).addTo(map)
                        .bindPopup('You are here!').openPopup();
                }

                map.setView(userLatLng, 10);
                localStorage.setItem('userLocation', JSON.stringify({ lat: latitude, lon: longitude }));
            },
            (error) => {
                console.error('Geolocation error:', error);
                alert('Unable to retrieve your location.');
            }
        );
    });

    updateMap();
    setInterval(updateMap, 5000);
}

// Initialize on load
document.addEventListener('DOMContentLoaded', initPage);

// Re-initialize if coming back via browser back button
window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
        initPage();
    }
});
