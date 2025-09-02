#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "[1/6] Installing OS packages…"
sudo apt update
sudo apt install -y python3-venv python3-pip pigpio python3-pigpio python3-opencv

echo "[2/6] Enabling pigpio daemon…"
sudo systemctl enable pigpiod --now

echo "[3/6] Creating venv and installing Python deps…"
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip wheel
# Use the apt-opencv requirements (faster on Pi)
pip install -r requirements-apt-opencv.txt

echo "[4/6] Creating captures dir…"
mkdir -p "$HOME/spm_captures"

echo "[5/6] Installing systemd service…"
SERVICE_PATH="/etc/systemd/system/raspi-spm.service"
sudo tee "$SERVICE_PATH" >/dev/null <<EOF
[Unit]
Description=Raspberry Pi SPM Tracker
After=network-online.target pigpiod.service
Wants=network-online.target

[Service]
User=${SUDO_USER:-$USER}
WorkingDirectory=$DIR
ExecStart=$DIR/.venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

echo "[6/6] Enabling service…"
sudo systemctl daemon-reload
sudo systemctl enable raspi-spm --now

echo "Done. Open: http://<pi-ip>:8000/"
