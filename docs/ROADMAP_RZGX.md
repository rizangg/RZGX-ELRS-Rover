# RZGX Roadmap

## Near Term

- Continue ER5C development without replacing the preserved 0.5H and 0.5I
  source, documentation, or artifacts.
- Validate the ER5C-only 0.5J scope in [Next Patch Notes](NEXT_PATCH_NOTES.md)
  without describing it as stable before physical testing.
- Preserve Stable 02 / MVP 0.5D for BETAFPV and Stable 04 / MVP 0.5I for the
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
