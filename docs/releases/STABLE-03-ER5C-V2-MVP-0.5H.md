# Stable 03 - RadioMaster ER5C V2 - MVP 0.5H

## Status

Stable 03 promotes the exact RZGX Rover ELRS 0.5H binary that was repeatedly
field-tested on physical RadioMaster ER5C V2 hardware. No source or firmware
artifact was rebuilt for this promotion.

The RadioMaster ER5A V2 uses the same official ExpressLRS target, layout, and
firmware identity. It has not been physically tested by this project and is
therefore target-compatible but not described as stable.

Stable 03 does not replace Stable 02 / MVP 0.5D for the BETAFPV PWM 2.4GHz RX.
Each stable release remains specific to its receiver target.

## Target

- ExpressLRS target: `radiomaster.rx_2400.er5-v2`
- Product identity: `RadioMaster ER5A/C V2 2.4GHz PWM RX`
- Physically validated receiver: `RadioMaster ER5C V2`
- Platform: `ESP8285`
- Build environment: `Unified_ESP8285_2400_RX_via_WIFI`
- RZGX release label: `0.5H`
- Embedded Rover firmware version: `4.0.1.5H`
- Official target VBAT calibration range: `4000..35000 mV`

## Included Behavior

- Receiver-side DJI MSP DisplayPort OSD without an external flight controller.
- Rover arming, steering, gas, RSSI, LQ, and FAILSAFE indications.
- Neutral steering and ESC PWM failsafe positions as configured in the
  ExpressLRS WebUI.
- Whole-pack VBAT in the native DJI battery field.
- Filtered average-per-cell voltage in the custom Rover OSD.
- User-configurable battery cell count from 1S through 8S, default 2S.
- Standard ExpressLRS binding, Wi-Fi update, PWM mapping, and UART
  configuration behavior.

## Expected Output Mapping

| Receiver output | Function |
| --- | --- |
| Output 1 | CH1 / steering PWM |
| Output 2 | Serial TX to DJI Air Unit RX |
| Output 3 | Serial RX from DJI Air Unit TX |
| Output 4 | CH2 / gas PWM |
| Output 5 | CH3 PWM |

The field-tested voltage-sense arrangements are documented in the
[ER5C V2 VBAT wiring and safety note](../ER5C_VBAT_WIRING.md).

## Artifacts

- `RZGX-Rover-ELRS-MVP-0.5H-RADIOMASTER-ER5A-ER5C-V2.bin`
- `RZGX-Rover-ELRS-MVP-0.5H-RADIOMASTER-ER5A-ER5C-V2.bin.gz`

SHA256:

```text
983f639eb97a8ef41951c208fd70211cc3360454161a7155aed89441843a8dbe  RZGX-Rover-ELRS-MVP-0.5H-RADIOMASTER-ER5A-ER5C-V2.bin
b9a54624b5e63ac0fd8add19bd6dd45f5a84892a819f49dc5ca256b38e63f4f7  RZGX-Rover-ELRS-MVP-0.5H-RADIOMASTER-ER5A-ER5C-V2.bin.gz
```

## Field Validation

Testing on `2026-08-01` included two daytime runs longer than five minutes and
one night run longer than ten minutes. Flashing, startup, binding, arming, PWM
control, DisplayPort, battery telemetry, and configured failsafe behavior all
operated as intended. No performance failure was observed.

The initial approximately 60 m physically obstructed run used an LHCP
replacement antenna on the RadioMaster Boxer. It produced one Telemetry Lost /
Telemetry Recovered event without failsafe, with observed LQ dips around
`75-80%` in the affected area.

A follow-up run on `2026-08-02` used the recovered RadioMaster Boxer stock T
antenna. The vehicle ran continuously for 15 minutes and repeatedly crossed the
same obstructed area. No Telemetry Lost / Telemetry Recovered notification,
failsafe, control anomaly, or OSD anomaly occurred, and LQ remained above
`90%` there.

These observations support stable operation in the tested installation. They
are field evidence rather than a calibrated range specification, and the
antenna comparison was not a controlled laboratory measurement.

Supporting captures, WebUI screenshots, and the complete observations are
listed in [`docs/TEST_LOG.md`](../TEST_LOG.md#radiomaster-er5c-v2--mvp-05h).

## Release Boundary

- Only the exact hashes above are promoted as Stable 03.
- Do not flash this artifact to a receiver outside the official ER5A/C V2
  target.
- ER5A V2 remains physically untested by this project.
- Future low-battery warning, timing, or WebUI-icon changes require a new
  version and a new validation cycle; they do not modify this release.
