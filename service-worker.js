const CACHE_NAME = 'random-tools-cache-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/js/main.js',
    '/js/modules/map.js',
    '/js/modules/pwa.js',
    '/js/modules/theme.js',
    '/manifest.json',
    '/converter/index.html',
    '/games/index.html',
    '/iveto/index.html',
    '/conspiracy/index.html',
    '/whoami/whoami.html',
    '/test4/index.html',
    'https://cdn.tailwindcss.com',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://unpkg.com/@joergdietrich/leaflet.terminator@1.1.0/L.Terminator.js',
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});