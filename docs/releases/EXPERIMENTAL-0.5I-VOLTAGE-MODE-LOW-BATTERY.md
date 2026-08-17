# Experimental 0.5I - Voltage Mode and Low-Battery Warning

## Status

MVP 0.5I is a new experimental build for the BETAFPV PWM 2.4GHz receiver and
the shared RadioMaster ER5A/ER5C V2 target. Its source, embedded WebUI, ESP8285
build, target metadata, deterministic gzip files, and SHA256 hashes have been
validated. It has not yet been flashed or driven on either physical receiver.

This build does not replace Stable 02 / BETAFPV 0.5D or Stable 03 / ER5C V2
0.5H. All prior source, documentation, and firmware artifacts remain separate.

## Changes From 0.5H

- Replaces the numeric battery-cell input with `Voltage Mode`: `RX`, `1S` through
  `8S`.
- `RX` shows the filtered receiver/BEC voltage unchanged in both the custom Rover
  OSD and native DJI battery field.
- `1S` through `8S` keep native DJI at whole-pack voltage and show average
  per-cell voltage in the custom Rover OSD.
- Adds an opt-in `Enable Low-Battery Warning` setting for `1S` through `8S`.
- Adds a user threshold from `2.50` through `4.50 V/cell` in `0.01 V` steps;
  default `3.50 V/cell`.
- Adds continuous warning delays of Immediate, 1, 3, 5, or 10 seconds; default
  3 seconds.
- Displays blinking `RETURN NOW` after a valid filtered sample stays below the
  threshold for the selected delay.
- Clears the warning only after voltage stays at least `0.10 V/cell` above the
  threshold for 2 continuous seconds.
- Keeps display priority `FAILSAFE` above `RETURN NOW`, then normal arming text.
- Replaces the generic Rover OSD menu symbol with the project goggles/OSD icon.

## Physical Voltage Source Warning

`Voltage Mode` only changes how firmware interprets and displays the analog
reading. It cannot switch the electrical voltage source.

- Choose `RX` only when the external VBAT sensing lead is disconnected and the
  receiver is reading its BEC supply.
- For `1S` through `8S`, connect the sensing lead to the verified positive
  whole-pack terminal of the battery to be monitored and select its actual
  series cell count.
- The vehicle must retain its already-verified common ground arrangement.
- Wrong wiring, voltage mode, or cell count produces a misleading display and
  may make the warning trigger too early, too late, or not when expected.

The same warning is embedded directly in the Rover OSD WebUI. Selecting `RX`
automatically turns off and locks the low-battery warning because a regulated
BEC voltage is not representative of battery state of charge.

## Configuration Migration

Upgrading from receiver configuration V13 / firmware 0.5H to V14 / 0.5I keeps
the existing UID/binding, PWM and UART mapping, failsafe positions, VBAT
calibration, Rover OSD enable state, craft name, and cell count. The new warning
defaults to disabled, `3.50 V/cell`, and 3 seconds.

Downgrading from 0.5I to a firmware that only understands V13, including 0.5H,
causes ExpressLRS to reset receiver configuration to defaults because the stored
version is newer. Record the binding, PWM/UART, failsafe, and VBAT calibration
settings before testing 0.5I if a downgrade may be required.

## Targets and Artifacts

### BETAFPV PWM 2.4GHz RX

- Target: `betafpv.rx_2400.pwmp`
- Platform: `ESP8285`
- Official target VBAT calibration range: `5000..9000 mV`
- `RZGX-Rover-ELRS-MVP-0.5I-BETAFPV-PWM-2G4RX.bin`
- `RZGX-Rover-ELRS-MVP-0.5I-BETAFPV-PWM-2G4RX.bin.gz`

### RadioMaster ER5A/ER5C V2

- Target: `radiomaster.rx_2400.er5-v2`
- Platform: `ESP8285`
- Official target VBAT calibration range: `4000..35000 mV`
- `RZGX-Rover-ELRS-MVP-0.5I-RADIOMASTER-ER5A-ER5C-V2.bin`
- `RZGX-Rover-ELRS-MVP-0.5I-RADIOMASTER-ER5A-ER5C-V2.bin.gz`

Both artifacts contain embedded Rover version `4.0.1.5I`. The RadioMaster
artifact preserves the audited options and binding UID from the supplied
original ER5 V2 firmware reference; the UID is intentionally not printed here.

SHA256 values are stored in `work/builds/SHA256SUMS-0.5I.txt`.

## Required Hardware Validation

Before promotion, verify Wi-Fi flashing, boot, binding, arming, PWM/UART mapping,
failsafe neutral positions, Rover OSD, native DJI voltage, and WebUI persistence
on each receiver target being claimed. Test `RX` with the external sensing lead
physically disconnected, test the applicable `1S` through `8S` mode with a
trusted voltmeter, and verify warning delay, recovery hysteresis, FAILSAFE
priority, and the no-valid-sample behavior. A stationary bench test should
precede any driven test.
