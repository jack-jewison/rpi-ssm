import cv2
import time
import threading
from datetime import datetime

from config import (
    CAM_INDEX, FRAME_W, FRAME_H, FPS,
    OSD_FONT_SCALE, OSD_THICKNESS,
    CAPTURE_DIR, CAPTURE_JPEG_QUALITY,
)

class FrameProducer:
    def __init__(self, gpio_state, capture_enabled=True):
        self.gpio = gpio_state
        self.cap = None
        self.frame = None
        self.lock = threading.Lock()
        self.stop_evt = threading.Event()
        self.capture_enabled = capture_enabled

    def start(self):
        self.cap = cv2.VideoCapture(CAM_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)
        self.cap.set(cv2.CAP_PROP_FPS, FPS)
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()

    def stop(self):
        self.stop_evt.set()
        if self.cap:
            self.cap.release()

    def _draw_osd(self, img):
        spm = self.gpio.spm()
        last_age = self.gpio.last_pulse_age()
        twine = self.gpio.twine_tripped()
        moist = self.gpio.moisture_wet()

        osd = [
            f"SPM: {spm:5.1f}",
            f"Last pulse: {'—' if last_age is None else f'{last_age:.1f}s ago'}",
            f"Twine: {'TRIPPED' if twine else 'OK'}",
            f"Moisture: {'WET' if moist else 'DRY'}"
        ]
        y = 30
        for line in osd:
            # outline
            cv2.putText(img, line, (18, y), cv2.FONT_HERSHEY_SIMPLEX, OSD_FONT_SCALE,
                        (0,0,0), OSD_THICKNESS+2, cv2.LINE_AA)
            # text
            cv2.putText(img, line, (16, y-2), cv2.FONT_HERSHEY_SIMPLEX, OSD_FONT_SCALE,
                        (255,255,255), OSD_THICKNESS, cv2.LINE_AA)
            y += 28

        if twine:
            badge = "TWINE BREAK"
            (w, h), _ = cv2.getTextSize(badge, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
            x = img.shape[1] - w - 20
            cv2.rectangle(img, (x-10, 20-h-10), (x+w+10, 20+10), (0,0,255), -1)
            cv2.putText(img, badge, (x, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2, cv2.LINE_AA)

    def _save_jpeg(self, bgr):
        ts = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        path = (CAPTURE_DIR / f"cap_{ts}.jpg").as_posix()
        cv2.imwrite(path, bgr, [int(cv2.IMWRITE_JPEG_QUALITY), CAPTURE_JPEG_QUALITY])
        return path

    def _loop(self):
        last = time.time()
        while not self.stop_evt.is_set():
            ok, frame = self.cap.read()
            if not ok:
                time.sleep(0.05)
                continue

            # Handle scheduled capture from segment trigger
            trig_ts = self.gpio.pop_capture_request()
            if trig_ts is not None and self.capture_enabled:
                delay = max(0.0, trig_ts + 1.0 - time.time())
                if delay > 0:
                    time.sleep(delay)
                self._save_jpeg(frame)

            self._draw_osd(frame)
            with self.lock:
                self.frame = frame

            dt = time.time() - last
            last = time.time()
            wait = max(0.0, (1.0/ FPS) - dt)
            if wait > 0:
                time.sleep(wait)

    def get_jpeg(self):
        with self.lock:
            if self.frame is None:
                return None
            ret, buf = cv2.imencode('.jpg', self.frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ret:
            return None
        return bytes(buf)
