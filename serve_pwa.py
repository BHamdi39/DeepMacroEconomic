"""خادم ثابت بسيط لقشرة PWA (يخدم pwa/ على المنفذ 8000).

MIME صحيح لـ .webmanifest و .js حتى يعمل service worker دون nosniff.
"""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os

EXTRA_MIME = {
    ".webmanifest": "application/manifest+json",
    ".js": "text/javascript; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".png": "image/png",
    ".json": "application/json; charset=utf-8",
}


def make_handler(base_dir: str):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=base_dir, **kwargs)

        def end_headers(self):
            self.send_header("Service-Worker-Allowed", "/")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            super().end_headers()

        def guess_type(self, path):
            ext = Path(path).suffix.lower()
            return EXTRA_MIME.get(ext, super().guess_type(path))

        def log_message(self, fmt, *args):  # هادئ
            pass

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--dir", default="pwa")
    args = parser.parse_args()
    base = os.path.abspath(args.dir)
    os.chdir(base)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(base))
    print(f"قشرة PWA تُخدم على http://localhost:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()