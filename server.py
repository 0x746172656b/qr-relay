import asyncio
import logging
import os

from aiohttp import web

from config import SCAN_DURATION, TIMER_DURATION

logger = logging.getLogger(__name__)

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def _render_index():
    path = os.path.join(TEMPLATE_DIR, "index.html")
    with open(path) as f:
        html = f.read()
    html = html.replace("{{SCAN_DURATION_MS}}", str(SCAN_DURATION * 1000))
    html = html.replace("{{TIMER_DURATION_S}}", str(TIMER_DURATION))
    return html


async def index(request):
    return web.Response(text=_render_index(), content_type="text/html")


def _make_qr_handler(mirror):
    async def handler(request):
        img_bytes = mirror.get_qr_image()
        return web.Response(
            body=img_bytes,
            headers={
                "Content-Type": "image/png",
                "Cache-Control": "no-cache, no-store, must-revalidate",
            },
        )
    return handler


def _make_ws_handler(mirror):
    async def handler(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        last_count = 0
        try:
            while True:
                await asyncio.sleep(0.02)
                with mirror.lock:
                    if mirror.update_counter != last_count:
                        last_count = mirror.update_counter
                        await ws.send_str(f"update:{mirror.last_qr_time}")
                    if mirror.timer_active and not mirror.timer_notified:
                        await ws.send_str("timer")
                        mirror.timer_notified = True
        finally:
            await ws.close()
        return ws
    return handler


def _make_start_handler(mirror):
    async def handler(request):
        mirror.start_scan()
        return web.Response(text="scanning started", status=200)
    return handler


def build_app(mirror):
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/qr.png", _make_qr_handler(mirror))
    app.router.add_get("/ws", _make_ws_handler(mirror))
    app.router.add_post("/start", _make_start_handler(mirror))
    return app
