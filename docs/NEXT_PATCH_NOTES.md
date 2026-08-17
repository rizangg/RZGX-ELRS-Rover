# Next Patch Notes - After Stable 05 / MVP 0.5K

Stable 05 / MVP 0.5K is the current stable ER5C release. Any next patch must
remain a new experimental version and must not replace the preserved 0.5H,
0.5I, 0.5J, or 0.5K source, documentation, and firmware artifacts.

## Candidate: Transmit Power OSD

The receiver already receives the transmitter's current selected power level
as `linkStats.uplink_TX_Power`. A future Rover OSD item can convert that CRSF
power enum to `10`, `25`, `50`, `100`, `250`, `500`, `1000`, or `2000 mW`.

- Label the value as current selected TX power, not measured RF output.
- Show an unavailable placeholder until the first valid power sample arrives.
- Do not present a stale value as current during failsafe; blank it, replace it
  with a placeholder, or include it in the failsafe blink behavior.
- Preserve the existing safety-notification priority and keep the field compact.
- Verify update latency in the ELRS switch modes that transmit power in a
  round-robin slot, especially with Dynamic Power enabled.

## Implemented 0.5J/0.5K Design Record

The sections below preserve the design that began in experimental 0.5J and was
completed by the failsafe reconnect correction in 0.5K.

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

The following checks were used before 0.5K replaced Stable 04 / 0.5I:

- verify no CH2 output while disarmed and no premature output immediately after
  arming;
- verify the neutral latch across disarm, re-arm, Wi-Fi mode, and power cycle;
- verify FAILSAFE remains the highest-priority message and neutralizes the
  vehicle;
- verify the timer pauses, resumes, resets, rolls over correctly, and remains
  visually aligned;
- repeat indoor and obstructed outdoor link tests on the physical ER5C V2.

Resolved in 0.5K: entering failsafe closes the neutral latch. Reconnection with
forward GAS held was exercised repeatedly; CH2 remained blocked and displayed
`GAS TO CENTER` until the input returned to neutral.
