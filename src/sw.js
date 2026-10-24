// Global News Shorts service worker — nav network-first, static assets stale-while-revalidate.
// Videos are never cached (large, streamed).
const CACHE = "gns-v1";
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/videos/") || url.pathname.endsWith(".mp4") || e.request.headers.has("range")) return;
  if (e.request.mode === "navigate") {
    e.respondWith(fetch(e.request).then((r) => {
      if (r.ok) { const c = r.clone(); caches.open(CACHE).then((cache) => cache.put(e.request, c)); }
      return r;
    }).catch(() => caches.match(e.request).then((m) => m || caches.match("/"))));
    return;
  }
  e.respondWith(caches.match(e.request).then((hit) => {
    const net = fetch(e.request).then((r) => {
      if (r.ok) { const c = r.clone(); caches.open(CACHE).then((cache) => cache.put(e.request, c)); }
      return r;
    }).catch(() => hit);
    return hit || net;
  }));
});
