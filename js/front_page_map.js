window.map = null;

document.addEventListener('DOMContentLoaded', () => {
    // Theme toggle
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

    // Map setup
    const savedState = JSON.parse(localStorage.getItem('mapState')) || { lat: 0, lon: 0, zoom: 2 };
    window.map = L.map('map', { zoomControl: false, scrollWheelZoom: true, dragging: true })
        .setView([savedState.lat, savedState.lon], savedState.zoom);

    const map = window.map;

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
            if (!res.ok) throw new Error('Network response not ok');
            const data = await res.json();
            const lat = data.latitude;
            const lon = data.longitude;
            issMarker.setLatLng([lat, lon]);

            const geocodeRes = await fetch(`https://api.opencagedata.com/geocode/v1/json?q=${lat}+${lon}&key=YOUR_OPENCAGE_API_KEY`);
            const geocodeData = await geocodeRes.json();
            const place = geocodeData.results[0]?.components?.country || 'the ocean';
            issMarker.setPopupContent(`The ISS is currently over ${place}`).openPopup();

            map.panTo([lat, lon]);
        } catch(e) { console.error(e); }
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
        if (!navigator.geolocation) { alert('Geolocation not supported'); return; }
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const latLng = [pos.coords.latitude, pos.coords.longitude];
                if (userMarker) userMarker.setLatLng(latLng);
                else userMarker = L.marker(latLng).addTo(map).bindPopup('You are here!').openPopup();
                map.setView(latLng, 10);
                localStorage.setItem('userLocation', JSON.stringify({ lat: pos.coords.latitude, lon: pos.coords.longitude }));
            },
            (err) => { console.error(err); alert('Unable to retrieve location'); }
        );
    });

    updateMap();
    setInterval(updateMap, 5000);
});
