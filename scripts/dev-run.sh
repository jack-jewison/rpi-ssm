#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-apt-opencv.txt
python app.py
