import time
import threading
from collections import deque

import pigpio

from config import (
    PIN_A, PIN_B, PIN_T1, PIN_T2, PIN_MOIST,
    DEBOUNCE_MS, MIN_VALID_INTERVAL_MS, SPM_WINDOW_SEC,
)

class GpioState:
    def __init__(self, pi):
        self.pi = pi
        # Input setup with pull-ups
        for pin in (PIN_A, PIN_B, PIN_T1, PIN_T2, PIN_MOIST):
            self.pi.set_mode(pin, pigpio.INPUT)
            self.pi.set_pull_up_down(pin, pigpio.PUD_UP)

        self.lock = threading.Lock()

        # Pulse timing
        self.pulse_times = deque(maxlen=1000)
        self.last_edge_time_ms = 0

        # Scheduled capture
        self.last_segment_ts = 0.0
        self.capture_requested = False

        # Callbacks
        self.cb_a = self.pi.callback(PIN_A, pigpio.FALLING_EDGE, self._on_a)
        self.cb_b = self.pi.callback(PIN_B, pigpio.FALLING_EDGE, self._on_b)

    # --- Inputs ---
    def _now_ms(self):
        return time.time() * 1000.0

    def _on_a(self, gpio, level, tick):
        now_ms = self._now_ms()
        dt = now_ms - self.last_edge_time_ms
        if dt < max(DEBOUNCE_MS, MIN_VALID_INTERVAL_MS):
            return
        with self.lock:
            self.pulse_times.append(time.time())
            self.last_edge_time_ms = now_ms

    def _on_b(self, gpio, level, tick):
        with self.lock:
            self.last_segment_ts = time.time()
            self.capture_requested = True

    # --- Public API ---
    def spm(self):
        cutoff = time.time() - SPM_WINDOW_SEC
        with self.lock:
            recent = [t for t in self.pulse_times if t >= cutoff]
        return (len(recent) / max(1e-6, SPM_WINDOW_SEC)) * 60.0

    def last_pulse_age(self):
        with self.lock:
            if not self.pulse_times:
                return None
            return time.time() - self.pulse_times[-1]

    def pop_capture_request(self):
        with self.lock:
            if self.capture_requested and (time.time() - self.last_segment_ts) >= 1e-6:
                self.capture_requested = False
                return self.last_segment_ts
            return None

    def twine_tripped(self):
        t1 = self.pi.read(PIN_T1) == 0
        t2 = self.pi.read(PIN_T2) == 0
        return t1 or t2

    def moisture_wet(self):
        return self.pi.read(PIN_MOIST) == 0

    def close(self):
        self.cb_a.cancel(); self.cb_b.cancel()
