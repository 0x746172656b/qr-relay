import logging
import time

import cv2
import numpy as np
import pyautogui
import pyscreenshot as ImageGrab

from config import (
    FAST_CHECK_INTERVAL,
    MATCH_THRESHOLD,
    PAUSE_AFTER_CLICK,
    SLOW_CHECK_INTERVAL,
    TEMPLATE_PATH,
    TIMER_DURATION,
)

logger = logging.getLogger(__name__)


def run(mirror):
    """
    Watches for a button template on screen and clicks it when found.
    Signals the mirror so the UI can show a countdown timer.
    """
    tpl = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
    if tpl is None:
        logger.error("Button template not found: %s", TEMPLATE_PATH)
        return

    th, tw = tpl.shape

    while True:
        with mirror.lock:
            waiting = mirror.last_scan_time is not None and not mirror.timer_active
        interval = FAST_CHECK_INTERVAL if waiting else SLOW_CHECK_INTERVAL
        time.sleep(interval)

        try:
            gray = cv2.cvtColor(
                np.array(ImageGrab.grab(backend="pil")), cv2.COLOR_BGR2GRAY
            )
            res = cv2.matchTemplate(gray, tpl, cv2.TM_CCOEFF_NORMED)
            _, score, _, loc = cv2.minMaxLoc(res)

            if score >= MATCH_THRESHOLD:
                cx = loc[0] + tw // 2
                cy = loc[1] + th // 2
                logger.info("Button matched (score %.2f) — clicking (%d, %d)", score, cx, cy)

                with mirror.lock:
                    mirror.timer_active = True
                    mirror.timer_notified = False

                pyautogui.click(cx, cy)
                time.sleep(PAUSE_AFTER_CLICK)

        except Exception:
            logger.exception("Error in auto-clicker loop")
