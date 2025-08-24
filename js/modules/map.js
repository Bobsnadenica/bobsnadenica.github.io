export function setupMap(L) {
    // Check for last saved map state
    const savedState = JSON.parse(localStorage.getItem('mapState')) || { lat: 0, lon: 0, zoom: 2 };
    
    const map = L.map('map', {
        zoomControl: false, 
        scrollWheelZoom: true,
        dragging: true,
    }).setView([savedState.lat, savedState.lon], savedState.zoom);

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

            // Add reverse geocoding for a bonus feature
            const geocodeRes = await fetch(`https://api.opencagedata.com/geocode/v1/json?q=${lat}+${lon}&key=YOUR_OPENCAGE_API_KEY`);
            const geocodeData = await geocodeRes.json();
            const place = geocodeData.results[0]?.components?.country || 'the ocean';
            issMarker.setPopupContent(`The ISS is currently over ${place}`).openPopup();

            map.panTo([lat, lon]);
        } catch(e) {
            console.error('ISS fetch error:', e);
        }
        terminator.setTime();

        // Save map state
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