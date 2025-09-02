# Raspberry Pi SPM Tracker (USB webcam + GPIO pulse counter)

FastAPI web app for counting strokes per minute (SPM) on a Raspberry Pi using pigpio + a USB webcam for live MJPEG and snapshots. Parity with ESP32 sketch: A (strokes), B (segment→delayed capture), T1/T2 (twine), optional digital moisture.

## Quick start (one-liner setup)
```bash
# after you unzip to ~/raspi-spm
cd ~/raspi-spm && bash scripts/install.sh
```
- Installs OS deps (`pigpio`, `python3-opencv`, etc.)
- Creates a Python venv & installs requirements
- Writes a systemd unit pointing at your current folder & venv
- Enables `pigpiod` and `raspi-spm` at boot

Then open: `http://<pi-ip>:8000/`

## Repo layout
```
app.py            # FastAPI app (status endpoints + MJPEG stream)
camera.py         # USB webcam capture + OSD + delayed snapshot
counter.py        # pigpio-based pulse counting + SPM
config.py         # pins, timing, camera + web config
static/index.html # Web UI
scripts/          # install/uninstall/dev/restart/push scripts
systemd/*.example # sample unit files (install.sh writes a real one)
requirements*.txt # pip dependencies (choose apt-opencv variant on Pi)
VERSION.txt
```

## GPIO (BCM numbering)
- A (strokes): **GPIO21**
- B (segment trigger): **GPIO20**
- T1: **GPIO16** (LOW at boot disables camera per safe-boot)
- T2: **GPIO12**
- Moisture (LOW=WET): **GPIO26**

Change in `config.py`, then:
```bash
sudo systemctl restart raspi-spm
```

## Notes
- **Pi GPIO is 3.3 V only.** If using 6–36 V proximity sensors (e.g., many LJ12A3 variants), use proper level shifting/optocoupler. Share ground.
- For faster installs on Pi, we use `python3-opencv` via `apt` and the `requirements-apt-opencv.txt` file.

## Dev (foreground)
```bash
bash scripts/dev-run.sh
# then open http://<pi-ip>:8000/
```

## Push to GitHub
```bash
# pass your repo URL
bash scripts/push.sh https://github.com/<user>/<repo>.git
```

## Uninstall
```bash
bash scripts/uninstall.sh
```
