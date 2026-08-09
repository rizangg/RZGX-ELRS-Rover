# Stable 04 - RadioMaster ER5C V2 - MVP 0.5I

## Status

Stable 04 promotes the exact RZGX Rover ELRS 0.5I binary repeatedly field-tested
on physical RadioMaster ER5C V2 hardware. It preserves Stable 03 / MVP 0.5H and
all earlier artifacts.

RadioMaster ER5A V2 shares the official ExpressLRS target identity and hardware
layout, but it has not been physically tested by this project. The ER5A claim
therefore remains target compatibility, not stable hardware validation.

The BETAFPV PWM 2.4GHz RX 0.5I artifact is not promoted by Stable 04. Its stable
release remains Stable 02 / MVP 0.5D.

## Firmware Identity

- Physically validated receiver: `RadioMaster ER5C V2`
- Packaged target: `RadioMaster ER5A/C V2 2.4GHz PWM RX`
- Firmware family: `Unified_ESP8285_2400_RX`
- Platform: `ESP8285`
- ExpressLRS base: `4.0.1`
- RZGX release label: `0.5I`
- Embedded Rover firmware version: `4.0.1.5I`

## Changes From Stable 03 / MVP 0.5H

- Adds Voltage Mode choices `RX` and `1S` through `8S`.
- `RX` displays receiver/BEC voltage unchanged in the custom and native DJI OSD.
- Cell-count modes display average-per-cell voltage in the custom Rover OSD and
  whole-pack voltage in the native DJI field.
- Adds an optional low-battery warning with a user-selected per-cell threshold
  and continuous delay.
- Displays blinking `RETURN NOW` after the configured low-voltage condition.
- Retains `FAILSAFE` as the highest-priority OSD notification.
- Adds recovery hysteresis to prevent rapid warning chatter.
- Adds the RZGX Rover OSD icon to the Wi-Fi Configurator.

Voltage Mode only interprets the measured voltage. The user must still connect
the ER5C sensing lead to the verified positive whole-pack terminal of the
battery being monitored. See [ER5C V2 VBAT Sense Wiring](../ER5C_VBAT_WIRING.md).

## Physical Validation

More than five test runs of approximately 5-15 minutes were completed over
about one week using a RadioMaster MT12 with Dynamic Power enabled up to 250 mW.
The tests covered LiPo 2S and 4S voltage interpretation, low-battery warning,
arming, control output, failsafe behavior, WebUI settings, and obstructed
outdoor operation out to approximately 150 m.

No performance failure or event triggering failsafe was observed. Telemetry
Lost / Telemetry Recovered notifications occurred in some obstructed positions
without affecting control or triggering failsafe. A companion receiver running
original ExpressLRS 3.3.1 also produced telemetry notifications at longer
obstructed range, so these observations are not attributed solely to 0.5I.

The notification-order test confirmed that `FAILSAFE` remains above the
low-battery `RETURN NOW` warning.

## Stable Artifacts

- `RZGX-Rover-ELRS-MVP-0.5I-RADIOMASTER-ER5A-ER5C-V2.bin`
- `RZGX-Rover-ELRS-MVP-0.5I-RADIOMASTER-ER5A-ER5C-V2.bin.gz`

SHA-256:

```text
db99302b0d438687402162c8adf58601e87a12d69f8a2889bc0f7d4cbf609d03  RZGX-Rover-ELRS-MVP-0.5I-RADIOMASTER-ER5A-ER5C-V2.bin
a8cce681c80826364338b8f058e9c755570f3a2093ba3a2d4ae45d9b40ecb37a  RZGX-Rover-ELRS-MVP-0.5I-RADIOMASTER-ER5A-ER5C-V2.bin.gz
```

Only files matching these hashes are promoted as Stable 04.

## Configuration Compatibility

Upgrading from configuration V13 / firmware 0.5H to V14 / firmware 0.5I keeps
the existing binding, PWM/UART mapping, failsafe positions, VBAT calibration,
Rover OSD enable state, craft name, and cell count. The new warning defaults to
disabled.

Downgrading to a V13 firmware can reset receiver configuration to defaults.
Record the binding, output mapping, failsafe, and VBAT calibration settings
before downgrading.

## Scope of the Stable Claim

Stable means the exact binary above performed consistently on the tested ER5C
V2 installation. It is not a generic stability claim for other ExpressLRS
receivers, ER5A hardware, batteries, ESCs, wiring arrangements, antennas, or RF
environments.
