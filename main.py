import logging
import threading

from aiohttp import web

import auto_clicker
from config import PORT
from scanner import QRMirror
from server import build_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)

if __name__ == "__main__":
    mirror = QRMirror()

    threading.Thread(target=mirror.scan_loop, daemon=True).start()
    threading.Thread(target=auto_clicker.run, args=(mirror,), daemon=True).start()

    app = build_app(mirror)
    web.run_app(app, host="0.0.0.0", port=PORT)
