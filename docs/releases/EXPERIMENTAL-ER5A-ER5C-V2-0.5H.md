# Experimental RadioMaster ER5A/ER5C V2 - MVP 0.5H

## Status

Field-tested pre-release firmware for RadioMaster ER5A V2 and ER5C V2. The
complete 0.5H feature set, including the battery display and native DJI battery
telemetry, has been tested on physical ER5C V2 hardware in an RC vehicle.

ER5A V2 uses the same official target and firmware identity, but has not been
physically tested by this project. Its compatibility remains target-based until
a separate hardware test is completed.

This release is separate from and does not replace the archived 0.5G.1 port.

## Target

- ExpressLRS target: `radiomaster.rx_2400.er5-v2`
- Product: `RadioMaster ER5A/C V2 2.4GHz PWM RX`
- Platform: `ESP8285`
- Build environment: `Unified_ESP8285_2400_RX_via_WIFI`
- RZGX release label: `0.5H`
- Embedded Rover firmware version: `4.0.1.5H`
- Official target VBAT calibration range: `4000..35000 mV`

ER5A V2 and ER5C V2 use the same official ExpressLRS target and firmware
identity. Their PWM header orientation differs, but their target configuration
does not.

## Changes From 0.5G.1

- Sends whole-pack VBAT to the DJI Air Unit with `MSP_ANALOG` and
  `MSP_BATTERY_STATE` once per second.
- Adds a filtered average-per-cell voltage line at OSD row 13.
- Keeps row 14 blank before `STR` at row 15.
- Uses one battery glyph instead of the text `CELL`.
- Shows battery glyph plus `-V` until a valid filtered sample is available.
- Adds a Wi-Fi configurator cell-count field with default `2`, minimum `1`,
  and maximum `8`.
- Migrates the 0.5G/0.5G.1 receiver configuration, including binding,
  PWM/UART mapping, Rover OSD settings, and VBAT scale/offset calibration.

The native DJI value is whole-pack voltage. The custom Rover OSD value is the
same filtered whole-pack sample divided by the configured cell count. Current,
consumed capacity, and remaining-capacity values stay zero because this target
does not provide those measurements.

## Expected Output Mapping

| Receiver output | Function |
| --- | --- |
| Output 1 | CH1 / steering PWM |
| Output 2 | Serial TX to DJI Air Unit RX |
| Output 3 | Serial RX from DJI Air Unit TX |
| Output 4 | CH2 / gas PWM |
| Output 5 | CH3 PWM |

The field-tested ER5C V2 voltage source can be selected with its single
positive telemetry sense lead. Refer to the
[ER5C V2 VBAT wiring and safety note](../ER5C_VBAT_WIRING.md) for the tested
RC-battery, external-Air-Unit-battery, and ESC-BEC arrangements.

## Artifacts

- `RZGX-Rover-ELRS-MVP-0.5H-RADIOMASTER-ER5A-ER5C-V2.bin`
- `RZGX-Rover-ELRS-MVP-0.5H-RADIOMASTER-ER5A-ER5C-V2.bin.gz`

SHA256:

```text
983f639eb97a8ef41951c208fd70211cc3360454161a7155aed89441843a8dbe  RZGX-Rover-ELRS-MVP-0.5H-RADIOMASTER-ER5A-ER5C-V2.bin
b9a54624b5e63ac0fd8add19bd6dd45f5a84892a819f49dc5ca256b38e63f4f7  RZGX-Rover-ELRS-MVP-0.5H-RADIOMASTER-ER5A-ER5C-V2.bin.gz
```

## ER5C V2 Field Validation

Testing completed on 2026-08-01 comprised two daytime runs longer than five
minutes each and one night run longer than ten minutes. Observed results:

- Wi-Fi flashing, receiver startup, binding, arming, PWM control, and
  DisplayPort operation were normal.
- Turning off the transmitter produced the expected FAILSAFE indication.
- Steering and ESC outputs returned to their configured neutral positions on
  failsafe, while STR and GAS OSD values intentionally retained the last valid
  received input.
- The custom battery OSD showed filtered average-per-cell voltage and the
  native DJI battery field showed whole-pack voltage.
- A run at approximately 60 m with concrete, metal fencing, and neighboring
  structures obstructing line of sight produced a brief Telemetry Lost /
  Telemetry Recovered event without failsafe. Observed LQ varied approximately
  76-90 percent during that condition.
- No performance failure or unexpected behavior was observed across the three
  runs.

The RadioMaster Boxer's missing stock T antenna was replaced with an LHCP
antenna using the same SMA connection during these tests. Consequently, the
distance observation is not a controlled stock-antenna range benchmark.

Supporting captures and WebUI configuration screenshots are listed in
[`docs/TEST_LOG.md`](../TEST_LOG.md#radiomaster-er5c-v2--mvp-05h).

## Remaining Boundary

MVP 0.5H is field-tested on ER5C V2 but remains a pre-release. ER5A V2 shares
the official target yet still requires its own physical hardware test before it
can be described as field-tested.
