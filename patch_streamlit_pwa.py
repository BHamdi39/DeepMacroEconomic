"""اجعل http://localhost:8508 نفسه قابلاً للتثبيت كـ PWA.

يبثّث ملفات الـ web app manifest وخطوط الأيقونات و service worker
داخل مجلد static الخاص بـ Streamlit المحلي، ويحقن روابطها في index.html.
العملية تكرّرة (idempotent) — أعد تشغيلها بعد كل ترقية لـ Streamlit.
"""
from __future__ import annotations

import pathlib
import shutil

import streamlit

STATIC = pathlib.Path(streamlit.__file__).resolve().parent / "static"
PWA = pathlib.Path(__file__).resolve().parent / "pwa"

HEAD_MANIFEST = '<link rel="manifest" href="./manifest.webmanifest" />'
HEAD_THEME = '<meta name="theme-color" content="#0E1117" />'
FOOT_SW = (
    '<script>'
    'if ("serviceWorker" in navigator) {'
    '  window.addEventListener("load", function () {'
    '    navigator.serviceWorker.register("./sw.js").catch(function () {});'
    '  });'
    '}'
    "</script>"
)


def main() -> None:
    for src, dst in (
        ("manifest.webmanifest", "manifest.webmanifest"),
        ("icon-192.png", "icon-192.png"),
        ("icon-512.png", "icon-512.png"),
        ("maskable-512.png", "maskable-512.png"),
        ("sw-app.js", "sw.js"),
    ):
        shutil.copyfile(PWA / src, STATIC / dst)
        print("copied", src, "->", dst)

    idx = STATIC / "index.html"
    html = idx.read_text(encoding="utf-8")

    if HEAD_THEME not in html:
        html = html.replace('<meta charset="UTF-8" />',
                            '<meta charset="UTF-8" />\n    ' + HEAD_THEME, 1)

    if HEAD_MANIFEST not in html:
        html = html.replace('<link rel="shortcut icon" href="./favicon.png" />',
                            '<link rel="shortcut icon" href="./favicon.png" />\n    '
                            + HEAD_MANIFEST, 1)

    if FOOT_SW not in html:
        html = html.replace("</body>", "    " + FOOT_SW + "\n  </body>", 1)

    idx.write_text(html, encoding="utf-8")
    print("index.html patched")


if __name__ == "__main__":
    main()