# Hardware Requirements

## Tested / recommended
- Raspberry Pi: Pi 4B (2–8 GB) or Pi 3B+ (lower FPS)
- OS: Raspberry Pi OS **Lite (64-bit)**
- Webcam: Any UVC-compliant USB camera (appears as `/dev/video0`)
- Power: Stable 5V supply (≥ 3A recommended for Pi 4)

## Sensors (logic levels!)
- Pi GPIO is **3.3 V only**. Do **not** feed 5–24 V logic directly into GPIO.
- For typical LJ12A3 proximity sensors (often 6–36 V, NPN or PNP):
  - Use a proper interface: pull-up to 3.3 V, resistor divider, or an **optocoupler**.
  - Common ground between sensor interface and Pi.
- If you have a true 3.3 V output sensor, verify with a multimeter before wiring.

## Performance tips
- Set GPU memory to **64 MB** via `raspi-config` (enough for MJPEG overlays).
- Reduce capture `FRAME_W/FRAME_H` or `FPS` in `config.py` for low-power Pis.
