# Stable 02 / MVP 0.5D

Stable 02 / MVP 0.5D is the current stable baseline for the physically tested
BETAFPV PWM 2.4GHz RX target. ER5C uses a separate target-specific stable build.

## Firmware

- ExpressLRS base: `4.0.1`
- RZGX label: `4.0.1.5D`
- Target: `BETAFPV PWM 2.4GHz RX`
- Binary: `work/builds/RZGX-Rover-ELRS-MVP-0.5D-BETAFPV-PWM-2G4RX.bin.gz`
- SHA-256: `d2ad3cfca4d72dda705390a1160650404338547fe5259649825b6da0022246ba`

## Field Result

This baseline was selected after repeated test runs from morning to midday.

Observed result:

- Link remained stable.
- OSD displayed and updated correctly.
- No repeated link drop was observed.
- Continuous CH2 use was stable.
- Tested on two receivers of the same hardware target.
- Craft Name and Binding Phrase changes through WiFi Configurator worked.

One reported "OSD missing" case was traced to the vehicle receiver not being
powered on yet, not to a firmware issue.

## OSD Layout

MVP 0.5D displays:

- Craft Name
- STANDBY
- ENGINE START arming transition
- STR percentage with direction glyph
- GAS percentage with direction glyph
- RSSI value
- Link Quality value

At neutral steering/gas, the direction marker is shown as `-`.

## Required Mapping

| Receiver Output | Role |
| --- | --- |
| Output 1 | Steering PWM |
| Output 2 | Serial TX to DJI RX |
| Output 3 | Serial RX from DJI TX |
| Output 4 | Gas PWM |
| Output 5 | CH3 PWM |

## Tested DJI Wiring

The stable test setup used separate power sources for the receiver and DJI Air
Unit. The Air Unit was powered from an external LiPo/BEC supply, while the
receiver stayed powered from the vehicle receiver/ESC 5V rail.

Required wiring:

| Receiver Pin | DJI Air Unit Pin |
| --- | --- |
| Output 2 `S` / TX | RX |
| Output 2 `G` | GND |
| Output 3 `S` / RX | TX |

Do not connect Output 2/3 `V` to the Air Unit. The Air Unit VCC must use its
own suitable power source.

The Air Unit power ground and receiver ground must be connected together.
SBUS and SBUS GND are not used by this MVP firmware.

## Known Limits

- This has only been field-validated on the BETAFPV PWM 2.4GHz RX target.
- The OSD is intentionally minimal and rover-specific.
- GPS, battery sensing, IMU, trip stats, and navigation are not part of this
  lightweight ELRS receiver firmware.
- The firmware is not an upstream generic ExpressLRS feature.
- Wrong target flashing may require USB-to-UART recovery.
