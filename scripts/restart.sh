#!/usr/bin/env bash
set -euo pipefail
sudo systemctl restart raspi-spm
sudo systemctl status raspi-spm --no-pager -l
