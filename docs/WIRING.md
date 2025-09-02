# Wiring (BCM numbering)

| Function             | Pin (BCM) | Notes                                   |
|---------------------|-----------|-----------------------------------------|
| A (strokes)         | GPIO21    | Falling edge count + debounce           |
| B (segment trigger) | GPIO20    | Schedules a capture +1.0 s              |
| T1 (twine sense)    | GPIO16    | LOW = TRIPPED; also safe-boot camera off|
| T2 (twine sense)    | GPIO12    | LOW = TRIPPED                           |
| Moisture (digital)  | GPIO26    | LOW = WET                               |

**All inputs use internal pull-ups.**  
Ensure sensors present **3.3 V logic**. Use level shifting/optocoupler as needed.

Quick checks:
- `raspi-gpio get 21` (etc.) to inspect levels.
- `pigpio` daemon must be running: `sudo systemctl status pigpiod`.
