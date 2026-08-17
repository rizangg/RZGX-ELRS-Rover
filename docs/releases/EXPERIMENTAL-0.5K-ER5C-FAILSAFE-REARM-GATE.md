# RZGX Rover ELRS 0.5K - ER5C experimental test build

## Scope

This build is prepared for field testing on the RadioMaster ER5C V2. RadioMaster publishes ER5A V2 and ER5C V2 under the same official ExpressLRS target identity and hardware layout, so the packaged identity remains `RadioMaster ER5A/C V2 2.4GHz PWM RX`.

No 0.5K BetaFPV PWM artifact is produced. The complete 0.5J source, documentation, and binaries remain preserved separately.

## Changes from 0.5J

- Entering receiver output failsafe immediately closes the ER5 logical CH2 GAS neutral latch.
- After the radio link recovers, CH2 GAS remains no-pulse while the last arming state is still armed and GAS is outside 1450-1550 microseconds.
- Returning GAS to that neutral range opens the latch again; disarm/rearm is not required.
- During `FAILSAFE`, the center warning, RSSI, and LQ blink together.
- During `START FIRST`, the center warning and GAS value blink together.
- During `GAS TO CENTER`, the center warning and GAS value blink together.
- During `RETURN NOW`, the center warning and battery voltage blink together.
- Warning priority remains `FAILSAFE` > `START FIRST` / `GAS TO CENTER` > `RETURN NOW` > normal state, so lower-priority fields do not blink during a higher-priority warning.

All other 0.5J functions, including voltage sensing, low-battery logic, arming gate, Drive Timer, target metadata, and embedded WebUI, are unchanged.

## Safety behavior

The safety gate is enabled only when the packaged runtime product identity is exactly `RadioMaster ER5A/C V2 2.4GHz PWM RX`. Other Unified receiver identities do not activate this gate.

The gate stops output pulses only for servo-capable output modes mapped to logical CH2. The configured failsafe path remains responsible for applying the tested neutral position while the link is in failsafe. The added latch reset prevents a held non-neutral GAS command from resuming immediately after reconnection.

## Test checklist before driving

Perform the first test with the vehicle lifted or restrained so the driven wheels cannot reach the ground.

1. Arm, center GAS to open the gate, and verify normal forward/reverse output.
2. Hold GAS away from center and turn the transmitter off. Confirm `FAILSAFE`, RSSI, and LQ blink together and the vehicle stops.
3. Keep GAS held away from center and turn the transmitter back on. Confirm CH2 remains no-pulse and `GAS TO CENTER` plus GAS blink together.
4. Return GAS to center. Confirm the gate opens and normal GAS output becomes available without disarm/rearm.
5. Repeat the reconnect test in both forward and reverse directions.
6. While disarmed, move GAS and confirm `START FIRST` plus GAS blink together while CH2 remains no-pulse.
7. Trigger the configured low-battery warning and confirm `RETURN NOW` plus battery voltage blink together.
8. While `RETURN NOW` is active, trigger failsafe and confirm only the higher-priority failsafe group blinks.

This remains an experimental build until the ER5C bench and drive checks above are completed.

## Build and packaging audit

- Firmware marker: `4.0.1.5K`, exactly once.
- Internal ExpressLRS build label: `rover-0.5k`.
- Platform: ESP8285.
- Firmware family: `Unified_ESP8285_2400_RX`.
- Product: `RadioMaster ER5A/C V2 2.4GHz PWM RX`.
- Lua name: `RM ER5A/C V2`.
- Official analog VBAT calibration range: 4000-35000 mV.
- Binding UID and target options must be copied from and verified equal to the supplied original ER5 V2 4.0.1 firmware during packaging.
- BetaFPV product, Lua-name, and `DIY_2400_RX_PWMP` markers must be absent.
- Embedded WebUI matches 0.5J byte-for-byte.
- PlatformIO build succeeds for `Unified_ESP8285_2400_RX_via_WIFI`.
- ELF change from 0.5J: text +144 bytes; data and BSS unchanged.
- Packaged BIN and deterministic GZ pass metadata validation and gzip round-trip verification.
