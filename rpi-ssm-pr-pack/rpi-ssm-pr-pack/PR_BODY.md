### What’s in this PR
- MIT `LICENSE` so reuse terms are clear
- CI via GitHub Actions (`.github/workflows/ci.yml`) to lint and syntax-check on every push/PR
- New docs:
  - `docs/HARDWARE.md` – supported Pi models, webcam notes, sensor interfacing
  - `docs/WIRING.md` – BCM pin table + safety notes
  - `docs/TROUBLESHOOTING.md` – pigpio, /dev/video0, CPU usage, service status
- README: CI badge + links to the above docs; explicit License section

### Why
- Clear legal terms (MIT)
- Baseline quality checks on every change (lint + import check)
- Faster onboarding: hardware expectations, wiring details, and quick fixes

### Follow-ups (separate PRs welcome)
- Add a wiring PNG/SVG diagram to `docs/assets/` and link it in WIRING.md
- Optionally add auth / bind host toggle for networks you don’t fully trust
- Tag a `v0.1.0` release for a stable baseline
