# Attribution

RZGX Rover-ELRS Controller is maintained by **Rizangg / RZGX**.

## Upstream

This project is based on ExpressLRS:

- https://github.com/ExpressLRS/ExpressLRS

ExpressLRS provides the radio link firmware, receiver runtime, PWM output
system, WiFi configuration system, target definitions, and build tooling.

## Related MSP DisplayPort Work

Special thanks to **Renaldy FPV / aldyduino**.

References:

- https://github.com/aldyduino/ESP32MSPDisplayPort
- https://github.com/ExpressLRS/ExpressLRS/pull/3703

Renaldy's work helped validate receiver-side DJI MSP DisplayPort as a practical
direction.

## RZGX Layer

The RZGX fork focuses on:

- RC ground vehicle use
- BETAFPV PWM receiver target testing
- Rover-specific OSD layout
- STR/GAS display
- STANDBY/ENGINE START display behavior
- RSSI/LQ rover OSD field validation

## AI Assistance

OpenAI Codex / ChatGPT was used as an implementation, debugging, documentation,
and iteration assistant. Final hardware testing and project direction remain
with the maintainer.

