import logging
import threading
import time

import cv2
import numpy as np
import pyscreenshot as ImageGrab

from config import (
    DEBOUNCE_TIME,
    NO_QR_TIMEOUT,
    SCAN_DURATION,
    TIMER_DURATION,
)

logger = logging.getLogger(__name__)


class QRMirror:
    def __init__(self):
        self.current_qr_bytes = None
        self.update_counter = 0
        self.last_qr_time = 0
        self.last_detected_data = None
        self.last_valid_detection_time = 0
        self.last_scan_time = None

        self.scan_event = threading.Event()
        self.lock = threading.Lock()
        self.detector = cv2.QRCodeDetector()

        self.timer_active = False
        self.timer_notified = False

    # ------------------------------------------------------------------
    # Screen capture
    # ------------------------------------------------------------------

    def capture_screen(self):
        try:
            img_pil = ImageGrab.grab(backend="pil")
            return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        except Exception:
            logger.exception("Screen capture failed")
            return None

    # ------------------------------------------------------------------
    # Placeholder image
    # ------------------------------------------------------------------

    def generate_placeholder(self):
        img = 255 * np.ones((300, 300, 3), dtype=np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = "No QR Code"
        ts = cv2.getTextSize(text, font, 1, 2)[0]
        pos = ((img.shape[1] - ts[0]) // 2, (img.shape[0] + ts[1]) // 2)
        cv2.putText(img, text, pos, font, 1, (0, 0, 0), 2)
        _, buf = cv2.imencode(".png", img)
        return buf.tobytes()

    # ------------------------------------------------------------------
    # Scan loop (runs in a background thread)
    # ------------------------------------------------------------------

    def scan_loop(self):
        while True:
            self.scan_event.wait()
            start = time.time()
            while time.time() - start < SCAN_DURATION:
                img = self.capture_screen()
                if img is None:
                    time.sleep(0.01)
                    continue

                data, bbox, _ = self.detector.detectAndDecode(img)
                now = time.time()

                with self.lock:
                    if bbox is not None and data:
                        if data != self.last_detected_data:
                            self.last_detected_data = data
                            self.last_valid_detection_time = now
                        elif now - self.last_valid_detection_time >= DEBOUNCE_TIME:
                            pts = bbox.reshape(-1, 2)
                            x, y, w, h = cv2.boundingRect(pts)
                            crop = img[y : y + h, x : x + w]
                            _, buf = cv2.imencode(".png", crop)
                            qr_bytes = buf.tobytes()
                            if qr_bytes != self.current_qr_bytes:
                                self.current_qr_bytes = qr_bytes
                                self.update_counter += 1
                                self.last_qr_time = now
                                logger.info("QR updated (#%d)", self.update_counter)
                    else:
                        self.last_detected_data = None
                        self.last_valid_detection_time = 0

                time.sleep(0.01)

            with self.lock:
                self.timer_active = False
            self.scan_event.clear()
            time.sleep(0.1)

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def start_scan(self):
        with self.lock:
            self.last_scan_time = time.time()
            self.timer_active = False
            self.timer_notified = False
        self.scan_event.set()

    def get_qr_image(self):
        with self.lock:
            stale = self.current_qr_bytes is None or (
                time.time() - self.last_qr_time > NO_QR_TIMEOUT
            )
            return self.generate_placeholder() if stale else self.current_qr_bytes
