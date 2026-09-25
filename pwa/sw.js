/* خدمة العامل: قشرة أولية + سقوط للصفحة الأساسية. الخطوط محزّمة محليًا. */
const VERSION = "macro2026-v3";
const SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./maskable-512.png",
  "./offline.html",
  "./fonts.css",
  // خطوط IBM Plex Sans Arabic (عربي + لاتيني-غير كامل للواجهة)
  "./fonts/plex-arabic-400.woff2",
  "./fonts/plex-arabic-500.woff2",
  "./fonts/plex-arabic-600.woff2",
  "./fonts/plex-arabic-700.woff2",
  "./fonts/plex-latin-400.woff2",
  "./fonts/plex-latin-500.woff2",
  "./fonts/plex-latin-600.woff2",
  "./fonts/plex-latin-700.woff2",
  // Inter (أرقام لاتينية)
  "./fonts/inter-latin-400.woff2",
  "./fonts/inter-latin-500.woff2",
  "./fonts/inter-latin-600.woff2",
  "./fonts/inter-latin-700.woff2",
  // JetBrains Mono (نتائج/جداول)
  "./fonts/jbmono-latin-400.woff2",
  "./fonts/jbmono-latin-500.woff2",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(VERSION).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // لا نعترض طلب فحص الحالة الصحية حتى يفشل فعلًا عند انقطاع الشبكة،
  // ولا يخدعنا خادم العامل بصفحة السقوط.
  if (url.pathname.endsWith("_stcore/health")) return;

  // نعمّر طلبات الـ streamlit من الشبكة (نسخة شبكية أولاً)؛ وعند العطب نعرض صفحة السقوط.
  if (url.hostname !== location.hostname || url.port !== location.port) {
    event.respondWith(
      fetch(request).catch(() => caches.match("./offline.html"))
    );
    return;
  }

  // نفس الأصل: شبكة أولاً لقشرة السببيبي، مع احتياط للكاشه.
  event.respondWith(
    fetch(request)
      .then((response) => {
        if (url.pathname.endsWith("/")) {
          const copy = response.clone();
          caches.open(VERSION).then((c) => c.put(request, copy));
        }
        return response;
      })
      .catch(() => caches.match(request).then((c) => c || caches.match("./offline.html")))
  );
});