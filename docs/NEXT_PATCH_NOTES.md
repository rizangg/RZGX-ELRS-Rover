# Next Patch Notes - Experimental 0.5J

This document records the agreed scope for the ER5C-only 0.5J test build.
Stable 04 / MVP 0.5I remains the current stable ER5C release until the new
behavior has completed physical testing. The preserved 0.5H and 0.5I source,
documentation, and firmware artifacts must not be replaced.

## WebUI

- Keep the current Rover OSD icon for this iteration.
- Rename `Voltage Mode` to `Voltage Sensing Mode` without changing its RX and
  1S-8S behavior or its physical-sensing-lead notice.

## CH2 Gas Safety Gate

The safety gate applies only to the logical CH2 gas signal on the ER5A/C V2
target. Steering remains available while disarmed.

- While CH5 is disarmed, CH2 gas may still move on the OSD, but the receiver
  must not send active gas pulses to the ESC.
- Moving gas while disarmed shows a flashing `START FIRST` message.
- After arming, gas output remains locked until the input has entered the
  neutral window of 1450-1550 microseconds. Until then, show flashing
  `GAS TO CENTER`.
- Once neutral has been seen, gas output is enabled and remains enabled until
  the next disarm.

Notification priority is:

1. `FAILSAFE`
2. `START FIRST` or `GAS TO CENTER`
3. `RETURN NOW`
4. normal `STANDBY` or `ENGINE START`

## Drive Timer

- Display `MM:SS`, right-aligned on the same row as battery voltage.
- Refresh at 1 Hz.
- Accumulate time only while armed, pause while disarmed, and continue after
  re-arming.
- Reset on receiver reboot or power cycle.
- Continue counting during failsafe if the receiver was armed immediately
  before the link loss.
- Cap the display at `99:59`.

## Validation Required

Before 0.5J can replace Stable 04 / 0.5I:

- verify no CH2 output while disarmed and no premature output immediately after
  arming;
- verify the neutral latch across disarm, re-arm, Wi-Fi mode, and power cycle;
- verify FAILSAFE remains the highest-priority message and neutralizes the
  vehicle;
- verify the timer pauses, resumes, resets, rolls over correctly, and remains
  visually aligned;
- repeat indoor and obstructed outdoor link tests on the physical ER5C V2.

Known audit item: if failsafe clears after the neutral latch was already open,
the present design may resume gas output from the live transmitter value. This
must be explicitly exercised during physical testing before promotion.
