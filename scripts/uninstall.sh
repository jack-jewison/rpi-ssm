#!/usr/bin/env bash
set -euo pipefail

echo "Stopping and disabling raspi-spm…"
sudo systemctl disable --now raspi-spm || true
sudo rm -f /etc/systemd/system/raspi-spm.service
sudo systemctl daemon-reload
echo "Removed systemd unit."
