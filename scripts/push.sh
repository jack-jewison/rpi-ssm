#!/usr/bin/env bash
set -euo pipefail
if [ $# -ne 1 ]; then
  echo "Usage: $0 https://github.com/<user>/<repo>.git"
  exit 1
fi
REPO="$1"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
if [ ! -d .git ]; then
  git init
  git add .
  git commit -m "Initial commit: Raspberry Pi SPM Tracker"
  git branch -M main
fi
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO"
git push -u origin main
