# Stable 05 - RadioMaster ER5C V2 - MVP 0.5K

## Status

Stable 05 promotes the exact RZGX Rover ELRS 0.5K binary repeatedly field-tested
on physical RadioMaster ER5C V2 hardware. It preserves Stable 04 / MVP 0.5I and
all earlier source, documentation, and firmware artifacts.

RadioMaster ER5A V2 shares the official ExpressLRS target identity and hardware
layout, but it has not been physically tested by this project. The stable
hardware claim therefore applies only to ER5C V2.

No BETAFPV PWM 2.4GHz RX 0.5K artifact is produced. Its stable release remains
Stable 02 / MVP 0.5D.

## Firmware Identity

- Physically validated receiver: `RadioMaster ER5C V2`
- Packaged target: `RadioMaster ER5A/C V2 2.4GHz PWM RX`
- Firmware family: `Unified_ESP8285_2400_RX`
- Platform: `ESP8285`
- ExpressLRS base: `4.0.1`
- RZGX release label: `0.5K`
- Embedded Rover firmware version: `4.0.1.5K`

## Changes From Stable 04 / MVP 0.5I

- Renames `Voltage Mode` to `Voltage Sensing Mode` without changing the
  physical sensing-source warning.
- Adds an ER5-only logical CH2 GAS safety gate. While disarmed, raw GAS remains
  visible in the OSD but the receiver sends no active GAS pulse to the ESC.
- Requires GAS to enter the `1450-1550 us` neutral window after arming before
  output is enabled.
- Displays blinking `START FIRST` while GAS is moved before arming and blinking
  `GAS TO CENTER` while the armed safety gate is waiting for neutral.
- Adds a cumulative `MM:SS` Drive Timer that runs while armed, pauses while
  disarmed, resumes on re-arm, and resets on receiver power cycle.
- Closes the GAS latch immediately on receiver failsafe. After reconnection,
  held non-neutral GAS remains blocked until the input returns to neutral.
- Coordinates warning blinking: `FAILSAFE` with RSSI/LQ, `START FIRST` and
  `GAS TO CENTER` with GAS, and `RETURN NOW` with battery voltage.
- Retains notification priority: `FAILSAFE`, arming/gas safety, low battery,
  then normal state.

The configured PWM failsafe remains authoritative while the link is lost. The
tested Output 4 / logical CH2 setup used `Set Position` at `1500 us`; users must
verify their own steering and ESC neutral failsafe positions before driving.

## Physical Validation

Repeated outdoor tests culminated in a final continuous run longer than 20
minutes over an area extending to approximately 300 m. The city-park route
included trees, walls, parked vehicles, and non-ideal transmitter orientation
relative to the rover.

The transmitter was a RadioMaster MT12 with its internal 2.4 GHz ELRS module,
Dynamic Power enabled, and a maximum transmit power of `250 mW`. The integrated
antenna was rotated upright, perpendicular to the top face of the transmitter.
This is a recorded test condition, not a controlled antenna comparison.

The following behavior was physically confirmed:

- disarmed GAS blocking and `START FIRST`;
- neutral-before-output arming behavior and `GAS TO CENTER`;
- repeated intentional failsafe and reconnect while forward GAS remained held;
- no resumed ESC output until GAS returned to neutral;
- warning priority and coordinated blinking;
- Drive Timer start, pause, resume, and power-cycle reset behavior;
- RX, 2S, 3S, and 4S Voltage Sensing Mode behavior;
- native DJI whole-pack and custom Rover OSD average-per-cell voltage;
- configurable low-battery threshold and delay;
- stable PWM control, UART DisplayPort, and Wi-Fi configuration.

No unintended failsafe or performance failure occurred. One or two Telemetry
Lost / Telemetry Recovered notifications occurred without a control anomaly or
failsafe. In the final run, the DJI video link became unusable before the ELRS
control link, while the observed ELRS LQ remained `99-100%`. These are field
observations, not calibrated range or RF-performance specifications.

Physical sampling did not intentionally cover held reverse GAS reconnect, the
invalid-voltage fallback, or every 5S-8S pack. Those paths remain supported by
the audited implementation but are outside the specific physical-test claim.

## Field Evidence

- [Approximately 300 m with physical obstructions](../assets/er5c-5k/field-test-300m-obstructed.png)
- [Intentional failsafe](../assets/er5c-5k/osd-intentional-failsafe.png)
- [GAS TO CENTER after reconnect](../assets/er5c-5k/osd-gas-to-center.png)
- [RETURN NOW low-battery warning](../assets/er5c-5k/osd-return-now.png)
- [Firmware Information with Binding UID redacted](../assets/er5c-5k/webui-firmware-information-redacted.jpg)
- [PWM and serial routing](../assets/er5c-5k/webui-pwm-serial-routing.jpg)
- [DisplayPort serial selection](../assets/er5c-5k/webui-displayport-serial.jpg)
- [Voltage sensing and warning settings](../assets/er5c-5k/webui-voltage-sensing.jpg)
- [Rover OSD source summary](../assets/er5c-5k/webui-rover-osd-sources.jpg)

## Build Provenance

The exact field-tested binary embeds Git hash `026304`, because it was built
from the complete 0.5K working tree before that source was committed. Rebuilding
only to change the embedded hash would create a different, untested artifact.

Distribution integrity is therefore defined by the SHA-256 values below. The
source, packaging script, audit record, and Stable 05 documentation are
committed without rebuilding or replacing the tested binary.

## Stable Artifacts

- `RZGX-Rover-ELRS-MVP-0.5K-RADIOMASTER-ER5A-ER5C-V2.bin`
- `RZGX-Rover-ELRS-MVP-0.5K-RADIOMASTER-ER5A-ER5C-V2.bin.gz`

SHA-256:

```text
2afeaa5fdd9974a5d73b73a47bcc1c3ca6e1dd1d6983750593f0e93ad79332b2  RZGX-Rover-ELRS-MVP-0.5K-RADIOMASTER-ER5A-ER5C-V2.bin
ad4416222c7bcf4b2885b510bf4e794ca0dbf79c39bce3a2432d65aa2489d6c4  RZGX-Rover-ELRS-MVP-0.5K-RADIOMASTER-ER5A-ER5C-V2.bin.gz
```

Only files matching these hashes are promoted as Stable 05.

## Configuration Compatibility

Stable 05 retains receiver configuration version V14 from 0.5I. Existing
binding, PWM/UART mapping, failsafe positions, VBAT calibration, Rover OSD
settings, voltage mode, and low-battery settings are preserved when upgrading
from 0.5I, subject to normal ExpressLRS configuration behavior.

Downgrading to a V13 firmware can reset receiver configuration to defaults.
Record binding, output mapping, failsafe, and VBAT calibration settings before
downgrading.

## Scope of the Stable Claim

Stable means the exact binary above performed consistently on the tested ER5C
V2 installation. It is not a generic stability claim for other ExpressLRS
receivers, ER5A hardware, batteries, ESCs, wiring arrangements, antennas, or RF
environments.
