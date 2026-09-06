const CACHE_NAME = "vm-cache-v6";
const STATIC_ASSETS = [
  "./",
  "./index.html",
  "./monitor.html",
  "./style.css",
  "./script.js",
  "./monitor.js",
  "./manifest.json",
  "./favicon.svg",
  "./ccf-logo.png"
];

// URLs to cache dynamically (CDNs)
const DYNAMIC_URLS = [
  "cdn.tailwindcss.com",
  "unpkg.com/html5-qrcode",
  "cdn.jsdelivr.net",
  "fonts.googleapis.com",
  "fonts.gstatic.com",
  "www.gstatic.com/firebasejs"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("Service Worker: Pre-caching static assets");
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log("Service Worker: Clearing old cache", cache);
            return caches.delete(cache);
          }
        })
      );
    })
  );
  return self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // Exclude Firebase API and Google Sheets API from caching
  if (url.hostname.includes("firebasedatabase.app") || 
      url.hostname.includes("googleapis.com") && url.pathname.includes("/v4/spreadsheets") ||
      url.hostname.includes("script.google.com")) {
    return; // Let the browser handle these normally
  }

  // Check if it's a dynamic CDN asset
  const isDynamic = DYNAMIC_URLS.some((domain) => url.hostname.includes(domain));

  if (isDynamic) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(event.request).then((networkResponse) => {
          if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== "basic" && networkResponse.type !== "cors") {
            return networkResponse;
          }
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
          return networkResponse;
        });
      })
    );
  } else {
    // Static assets (Cache-first strategy)
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  }
});
