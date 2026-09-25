/* خدمة عامل لتطبيق Streamlit نفسه على http://localhost:8508.
   بلا تخزين للقشرة — وجود مستمع fetch يكفي لتأهيل التثبيت كـ PWA،
   ولا نعترض أي طلب حتى لا نكسر اتصال WebSocket أو الفحص الصحي. */
const VERSION = "macro2026-app-v1";

self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  // نترك الاستجابات للشبكة مباشرة (تجاوز كامل)؛ مجرد وجود المستمع يكفي.
  void event;
});