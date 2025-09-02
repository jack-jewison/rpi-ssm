# Troubleshooting

## pigpio not running
```bash
sudo systemctl enable pigpiod --now
sudo systemctl status pigpiod --no-pager -l
```

## No video frames
- Check webcam: `dmesg | grep -i video`, confirm `/dev/video0`
- Try `CAM_INDEX = 1` in `config.py`
- Lower `FPS` or `FRAME_W/H` if CPU is pegged

## Service won’t start
```bash
sudo systemctl status raspi-spm --no-pager -l
journalctl -u raspi-spm -n 200 --no-pager
```

## High CPU
- Lower resolution/FPS in `config.py`
- Prefer `sudo apt install python3-opencv` and use `requirements-apt-opencv.txt`

## Debounce / false counts
- Increase `DEBOUNCE_MS` or `MIN_VALID_INTERVAL_MS`
- Ensure proper sensor interfacing (no 12–24 V directly into GPIO)
