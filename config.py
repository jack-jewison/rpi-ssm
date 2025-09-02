from pathlib import Path

# GPIO pins (BCM)
PIN_A = 21           # strokes
PIN_B = 20           # segment trigger → schedule capture
PIN_T1 = 16          # twine sense 1 (LOW = TRIPPED)
PIN_T2 = 12          # twine sense 2 (LOW = TRIPPED)
PIN_MOIST = 26       # moisture digital (LOW = WET)

# Debounce & SPM
DEBOUNCE_MS = 12     # ignore edges within this many ms
SPM_WINDOW_SEC = 15  # rolling window to compute strokes per minute
MIN_VALID_INTERVAL_MS = 60  # reject pulses faster than this (anti-bounce)

# Camera
CAM_INDEX = 0            # /dev/video0
FRAME_W = 1280
FRAME_H = 720
FPS = 20
OSD_FONT_SCALE = 0.7
OSD_THICKNESS = 2

# Capture
CAPTURE_ENABLED_AT_BOOT = True
SAFEBOOT_CAMERA_DISABLE_ON_T1_LOW = True
CAPTURE_DIR = Path.home() / "spm_captures"
CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
CAPTURE_JPEG_QUALITY = 90
CAPTURE_DELAY_SEC = 1.0   # after B trigger

# Web
HOST = "0.0.0.0"
PORT = 8000
