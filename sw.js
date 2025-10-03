const CACHE_NAME = 'buddy-finanzas-v1';
const BASE_PATH = '/buddy-finanzas-app';
const urlsToCache = [
  `${BASE_PATH}/`,
  `${BASE_PATH}/1.html`,
  `${BASE_PATH}/2.html`,
  `${BASE_PATH}/3.html`,
  `${BASE_PATH}/4.html`,
  `${BASE_PATH}/manifest.json`,
  `${BASE_PATH}/firebase-config.js`,
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap'
];

// Install event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        // Cache only local resources, skip external ones that might have CORS issues
        const localUrls = urlsToCache.filter(url => !url.startsWith('http'));
        return cache.addAll(localUrls);
      })
      .catch(error => {
        console.log('Cache installation failed:', error);
      })
  );
});

// Fetch event
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      }
    )
  );
});

// Activate event
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
