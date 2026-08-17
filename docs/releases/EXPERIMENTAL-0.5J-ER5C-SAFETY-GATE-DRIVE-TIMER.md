# RZGX Rover ELRS 0.5J - ER5C experimental test build

## Scope

This build is prepared for field testing on the RadioMaster ER5C V2. RadioMaster publishes ER5A V2 and ER5C V2 under the same official ExpressLRS target identity and hardware layout, so the packaged identity remains `RadioMaster ER5A/C V2 2.4GHz PWM RX`.

No 0.5J BetaFPV PWM artifact is produced. The complete 0.5I source, documentation, and binaries remain preserved separately.

## Changes from 0.5I

- WiFi Configurator label `Voltage Mode` is renamed to `Voltage Sensing Mode`.
- The existing voltage wiring notice and Rover OSD icon are unchanged.
- Logical CH2 GAS receives an ER5-only safety gate. The gate follows the configured CH2 input even when it is assigned to a different physical PWM output.
- While disarmed, the CH2 GAS pulse output is stopped. Raw CH2 movement remains visible on the GAS OSD.
- Moving GAS while disarmed displays blinking `START FIRST`.
- After arming, GAS output remains stopped until the input is centered between 1450 and 1550 microseconds. Until then, the OSD displays `GAS TO CENTER`.
- Once centered, the gate latches open until the next disarm. `ENGINE START` begins when the gate opens, rather than expiring behind the neutral warning.
- A cumulative Drive Timer is displayed right-aligned on the battery row in `MM:SS` format.

## Safety and notification behavior

The safety gate is enabled only when the packaged runtime product identity is exactly `RadioMaster ER5A/C V2 2.4GHz PWM RX`. Other Unified receiver identities do not activate this 0.5J gate.

The gate stops output pulses only for servo-capable output modes mapped to logical CH2. Serial and I2C pin modes are not modified. Capturing the current PWM position as a failsafe value bypasses the safety gate, and the existing configured failsafe path remains responsible for applying its tested neutral position.

OSD notification priority is:

1. `FAILSAFE`
2. `START FIRST` or `GAS TO CENTER`
3. `RETURN NOW`
4. `STANDBY` or `ENGINE START`

## Drive Timer definition

- Starts when the actual receiver arming state becomes armed.
- Pauses on disarm and resumes from the accumulated value on the next arm.
- Continues during a link failsafe if the last received arming state remains armed.
- Resets only when the receiver is power-cycled.
- Updates its numeric value at 1 Hz while the rest of the OSD continues its existing refresh cadence.
- Saturates at `99:59`.

## Build and packaging audit

- Firmware marker: `4.0.1.5J`, exactly once.
- Platform: ESP8285.
- Firmware family: `Unified_ESP8285_2400_RX`.
- Product: `RadioMaster ER5A/C V2 2.4GHz PWM RX`.
- Lua name: `RM ER5A/C V2`.
- Official analog VBAT calibration range: 4000-35000 mV.
- Binding UID and target options: copied from and verified equal to the supplied original ER5 V2 4.0.1 firmware; sensitive values are not printed in this document.
- Prior-target marker: absent.
- BetaFPV product, Lua-name, and `DIY_2400_RX_PWMP` markers: absent.
- Embedded WebUI: rebuilt for SX128x RX ESP8285 and contains the new `Voltage Sensing Mode` label.
- Existing Rover OSD icon sources match 0.5I byte-for-byte.
- PlatformIO build: successful for `Unified_ESP8285_2400_RX_via_WIFI`.
- ELF size change from 0.5I: text +728 bytes, data unchanged, BSS -8 bytes.

## Test checklist before driving

Perform the first test with the vehicle lifted so the driven wheels cannot reach the ground.

1. Power on while disarmed and move GAS in both directions. Confirm the ESC receives no usable GAS signal and `START FIRST` blinks.
2. Hold GAS away from center and arm. Confirm the ESC still receives no usable GAS signal and `GAS TO CENTER` is displayed.
3. Return GAS to center. Confirm the gate opens, `ENGINE START` appears, and normal forward/reverse control becomes available.
4. Disarm while applying GAS. Confirm output is stopped immediately.
5. Confirm STR remains available while disarmed; only logical CH2 GAS is gated.
6. Confirm the timer runs only while armed, pauses on disarm, resumes on rearm, and resets after a receiver power cycle.
7. Repeat the established transmitter-off failsafe test and verify steering and ESC return to their configured neutral positions.
8. Repeat the low-battery test and confirm safety messages take priority over `RETURN NOW`.

This is an experimental test build until the ER5C bench and drive checks above are completed.
