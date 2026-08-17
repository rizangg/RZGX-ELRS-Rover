# RZGX Roadmap

## Near Term

- Continue ER5C development without replacing the preserved 0.5H, 0.5I, 0.5J,
  and 0.5K
  source, documentation, or artifacts.
- Evaluate the transmit-power OSD candidate in
  [Next Patch Notes](NEXT_PATCH_NOTES.md) without changing Stable 05.
- Preserve Stable 02 / MVP 0.5D for BETAFPV and Stable 05 / MVP 0.5K for the
  physically tested RadioMaster ER5C V2.
- Avoid large OSD additions unless link stability remains proven.
- Test more receiver samples of the same target.
- Document exact wiring photos and target configuration screenshots.

## Possible Future Work

- Cleaner release packaging.
- More receiver target validation.
- Optional RSSI/LQ layout variants.
- Upstream rebase if generic DisplayPort support lands in ExpressLRS.
- Consider a separate rover-focused branch for each supported hardware target.

## Out Of Scope For This Lightweight Fork

These belong in the full ESP32-based RZGX Rover Controller instead:

- GPS
- IMU
- Battery ADC
- Home point
- Trip stats
- Drive modes
- Complex channel assignment
- Servo pan/tilt control
