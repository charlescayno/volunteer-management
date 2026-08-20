import os
import codecs
import re

# 1. Create manifest.json
manifest = '''{
  "name": "Volunteer Management",
  "short_name": "Volunteers",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#171717",
  "theme_color": "#171717",
  "icons": [
    {
      "src": "icon.svg",
      "sizes": "192x192 512x512",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    }
  ]
}'''
with codecs.open('manifest.json', 'w', 'utf-8') as f:
    f.write(manifest)

# 2. Create icon.svg
icon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="100" fill="#38bdf8"/>
  <text x="256" y="320" font-family="Arial, sans-serif" font-size="220" font-weight="bold" fill="#ffffff" text-anchor="middle">VM</text>
</svg>'''
with codecs.open('icon.svg', 'w', 'utf-8') as f:
    f.write(icon)

# 3. Create sw.js
sw = '''const CACHE_NAME = 'vm-cache-v1';
const STATIC_ASSETS = [
  './',
  './index.html',
  './monitor.html',
  './register.html',
  './style.css',
  './script.js',
  './monitor.js',
  './manifest.json',
  './icon.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Skip cross-origin requests, let them pass through
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Stale-while-revalidate for static assets
        fetch(event.request).then(response => {
          if (response && response.status === 200) {
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, response.clone()));
          }
        }).catch(() => {});
        return cachedResponse;
      }
      return fetch(event.request).then(response => {
        if (response && response.status === 200) {
          const resClone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, resClone));
        }
        return response;
      }).catch(() => {
         // Offline fallback if needed
      });
    })
  );
});
'''
with codecs.open('sw.js', 'w', 'utf-8') as f:
    f.write(sw)

# 4. Patch HTML files to include manifest, theme-color, offline banner, and SW registration
html_files = ['index.html', 'monitor.html', 'register.html']
for hf in html_files:
    if os.path.exists(hf):
        with codecs.open(hf, 'r', 'utf-8') as f:
            c = f.read()
        
        # Add head tags
        if '<link rel="manifest"' not in c:
            c = c.replace('</title>', '</title>\n    <link rel="manifest" href="manifest.json">\n    <meta name="theme-color" content="#171717">')
        
        # Add offline banner
        if 'id="offline-banner"' not in c:
            banner = '<div id="offline-banner" class="hidden bg-red-600 text-white text-center text-xs py-1.5 font-bold tracking-widest uppercase sticky top-0 z-50 shadow-md">You are currently offline. Scans will be saved locally and synced later.</div>'
            c = re.sub(r'(<body[^>]*>)', r'\1\n    ' + banner, c)
            
        with codecs.open(hf, 'w', 'utf-8') as f:
            f.write(c)

# 5. Patch script.js for offline functionality
with codecs.open('script.js', 'r', 'utf-8') as f:
    s = f.read()

# Append SW registration and offline logic
offline_js = '''
// =============================
// PWA & Offline Sync Logic
// =============================
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js')
      .then(reg => console.log('Service Worker registered', reg))
      .catch(err => console.log('Service Worker registration failed', err));
  });
}

function updateOnlineStatus() {
  const banner = document.getElementById('offline-banner');
  if (banner) {
    if (navigator.onLine) {
      banner.classList.add('hidden');
      flushOfflineScans();
    } else {
      banner.classList.remove('hidden');
    }
  }
}
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);
updateOnlineStatus();

// Simple IndexedDB wrapper for offline scans
const DB_NAME = 'vm-offline-db';
const STORE_NAME = 'scans';

function getOfflineDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, 1);
    request.onupgradeneeded = (e) => e.target.result.createObjectStore(STORE_NAME, { autoIncrement: true });
    request.onsuccess = (e) => resolve(e.target.result);
    request.onerror = (e) => reject(e);
  });
}

async function saveScanOffline(scanData) {
  const db = await getOfflineDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    tx.objectStore(STORE_NAME).add(scanData);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject();
  });
}

async function flushOfflineScans() {
  const db_instance = await getOfflineDB();
  const tx = db_instance.transaction(STORE_NAME, 'readonly');
  const store = tx.objectStore(STORE_NAME);
  const req = store.getAll();
  
  req.onsuccess = async () => {
    const scans = req.result;
    if (scans && scans.length > 0) {
      showToast(`Syncing ${scans.length} offline scan(s)...`, "sync", "text-sky-400");
      let syncedCount = 0;
      for (const scan of scans) {
         try {
           // Push raw offline scan to a special queue in Firebase for admins to process, 
           // or process it directly if we have enough data.
           await db.ref('offlineQueue').push(scan);
           syncedCount++;
         } catch(e) {
           console.error("Failed to sync offline scan", e);
         }
      }
      
      if (syncedCount > 0) {
        // Clear store
        const clearTx = db_instance.transaction(STORE_NAME, 'readwrite');
        clearTx.objectStore(STORE_NAME).clear();
        showToast("Offline scans synced successfully!", "cloud_done", "text-green-400");
      }
    }
  };
}

// Hook into handleVolunteerScan for offline fallback
const originalHandleScan = handleVolunteerScan;
handleVolunteerScan = async function(id) {
  if (!navigator.onLine) {
    if (typeof playTone === "function") playTone("success");
    await saveScanOffline({ id, timestamp: Date.now(), type: 'raw_scan' });
    showStage('qr-result');
    document.getElementById('result-message').innerHTML = `<span class="text-amber-400 font-bold">OFFLINE MODE</span><br>Scan saved locally. It will sync automatically when internet is restored.`;
    document.getElementById('result-icon').textContent = "cloud_off";
    document.getElementById('result-icon').className = "material-icons-round text-amber-400 text-6xl mb-4";
    setTimeout(startQrScanner, 4000);
    return;
  }
  return originalHandleScan(id);
};
'''

if 'Service Worker registered' not in s:
    s += '\n' + offline_js
    with codecs.open('script.js', 'w', 'utf-8') as f:
        f.write(s)
