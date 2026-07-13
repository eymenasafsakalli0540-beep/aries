// ARIES AI - Basit Servis Çalışanı (PWA'nın "kurulabilir" olması için gerekli)
const CACHE_NAME = "aries-ai-cache-v1";

self.addEventListener("install", (event) => {
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(self.clients.claim());
});

// Basit ağ-öncelikli strateji: /ask gibi dinamik istekleri asla önbellekleme,
// sadece sayfa çevrimdışı açılırsa diye ana sayfayı hafifçe önbellekle.
self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;
    const url = new URL(event.request.url);
    if (url.pathname.startsWith("/ask") || url.pathname.startsWith("/api/")) return;

    event.respondWith(
        fetch(event.request).catch(() =>
            caches.match(event.request).then((cached) => cached || caches.match("/"))
        )
    );
});
