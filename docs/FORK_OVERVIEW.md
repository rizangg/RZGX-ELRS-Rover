# Fork Overview

RZGX Rover-ELRS Controller is a rover-focused ExpressLRS fork.

The goal is not to turn an ELRS receiver into a full flight controller. The goal
is to keep the receiver simple:

- Keep PWM vehicle control working.
- Use selected UART-capable receiver pins for DJI MSP DisplayPort.
- Render a small OSD directly from receiver runtime data.

## Why A Fork

This use case is narrow and practical:

- RC ground vehicle
- PWM receiver
- DJI O3/O4 Air Unit
- No flight controller
- Minimal OSD

That makes it more suitable as an applied fork than as a broad upstream feature.

## Difference From Generic DisplayPort Support

Generic upstream DisplayPort support should ideally be reusable across many
vehicle types and receiver targets.

RZGX Rover-ELRS Controller is opinionated:

- Rover wording: `STR`, `GAS`, `STANDBY`, `ENGINE START`
- Fixed field-tested layout
- BETAFPV PWM receiver target focus
- Ground vehicle testing

## Design Rule

The radio link comes first.

OSD rendering must stay lightweight. If an OSD feature risks destabilizing the
receiver link, it should be simplified or removed.

