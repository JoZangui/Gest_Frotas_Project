const CACHE_NAME = 'frotas-app-v1';
const urlsToCache = [
  '/',
  '/mapa/',
  '/static/js/geolocation.js',
  '/static/js/manifest.json'
];

// Event: Install
self.addEventListener('install', event => {
  console.log('[Service Worker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[Service Worker] Caching app shell');
      return cache.addAll(urlsToCache).catch(err => {
        console.log('[Service Worker] Cache addAll error:', err);
      });
    })
  );
  self.skipWaiting();
});

// Event: Activate
self.addEventListener('activate', event => {
  console.log('[Service Worker] Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Event: Fetch
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip cross-origin requests
  if (url.origin !== location.origin) {
    return;
  }

  event.respondWith(
    caches.match(request).then(response => {
      if (response) {
        return response;
      }
      return fetch(request).then(response => {
        // Cache successful responses
        if (response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(request, responseToCache);
          });
        }
        return response;
      }).catch(() => {
        console.log('[Service Worker] Fetch failed for:', request.url);
      });
    })
  );
});

// Event: Background Sync for location tracking
self.addEventListener('sync', event => {
  console.log('[Service Worker] Background Sync:', event.tag);
  if (event.tag === 'sync-location') {
    event.waitUntil(syncLocation());
  }
});

async function syncLocation() {
  try {
    // Get pending locations from IndexedDB
    const pendingLocations = await getFromDB('pendingLocations');
    if (pendingLocations && pendingLocations.length > 0) {
      for (const location of pendingLocations) {
        await fetch('/api/localizacao/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(location)
        }).then(() => {
          removeFromDB('pendingLocations', location.id);
        });
      }
    }
  } catch (error) {
    console.error('[Service Worker] Sync failed:', error);
    throw error;
  }
}

// Simple DB helper (optional)
function getFromDB(storeName) {
  return new Promise((resolve) => {
    const request = indexedDB.open('frotasDB', 1);
    request.onsuccess = () => {
      resolve([]);
    };
  });
}

function removeFromDB(storeName, id) {
  return Promise.resolve();
}
