# RadioMaster ER5C V2 VBAT Sense Wiring

This note documents the field-tested voltage-sense arrangement used with the
RadioMaster ER5C V2 and RZGX Rover ELRS 0.5H, 0.5I, and 0.5K. RadioMaster specifies automatic
selection between external battery voltage and receiver/ESC-BEC voltage, with
an external telemetry detection range of `4.0-35 V`.

Official receiver reference:
[RadioMaster ER5C V2 2.4GHz ELRS PWM Receiver](https://www.radiomasterrc.com/products/er5c-v2-2-4ghz-elrs-pwm-receiver)

## Tested One-Wire Connection

The ER5C V2 voltage telemetry port was connected with one insulated sensing
lead. A male Dupont contact on the other end was connected to the verified
whole-pack positive terminal of the selected LiPo balance connector.

Only the positive sense lead was moved. No additional ground lead was installed
because the tested vehicle already had a common ground between the receiver,
ESC/BEC, PWM connections, and the separately powered DJI Air Unit. This
one-wire arrangement is valid only when the battery negative and receiver ground
are already electrically common.

| Voltage to monitor | Voltage telemetry lead connection |
| --- | --- |
| RC drive battery, whole pack | Verified pack-positive terminal of the RC battery balance connector |
| Separate DJI Air Unit battery, whole pack | Verified pack-positive terminal of the Air Unit battery balance connector |
| Receiver supply from the ESC BEC | Leave the external voltage telemetry lead disconnected; the ER5C V2 automatically falls back to receiver/BEC voltage telemetry |

This makes source selection simple in the tested installation: the same
positive sense lead can be moved between the two external batteries, or left
disconnected to monitor the receiver supply.

## Stable 05 / MVP 0.5K Voltage Sensing Mode

| WebUI mode | Required physical arrangement | Display behavior |
| --- | --- | --- |
| `RX` | Leave the external sensing lead disconnected | Receiver/BEC voltage is shown unchanged in both OSD fields |
| `1S`-`8S` | Connect to verified whole-pack positive and select the actual series cell count | Native DJI shows whole pack; Rover OSD shows average per cell |

Voltage Sensing Mode does not electrically switch the source. Moving or disconnecting
the sensing lead remains a physical user action. Selecting `RX` automatically
disables the low-battery warning. In `1S`-`8S` modes, the optional warning uses
the displayed average-per-cell voltage, configured threshold, and delay.

## Safety Notes

- Identify the actual whole-pack positive terminal from the battery or balance
  connector diagram, or confirm it with a multimeter. Do not rely only on which
  end of the connector appears to be the outermost pin.
- Connect only to the dedicated voltage telemetry input. Never connect pack
  voltage to a PWM signal pin, receiver supply pin, or UART pin.
- Do not use an intermediate cell tap when whole-pack voltage is intended.
- Confirm common ground before attaching a one-wire positive sense lead. If the
  grounds are isolated, stop and correct the grounding arrangement first.
- Keep the measured voltage inside the receiver's official `4.0-35 V` range.
  For external LiPo sensing, the RZGX configurator supports `1S-8S` cell-count
  values. Select the actual series count of the physically connected battery.
- A loose Dupont contact can bridge adjacent balance pins. An insulated,
  strain-relieved adapter or JST-XH breakout is safer than an exposed probe.
- Powering down before moving the lead is the safest practice. If it is moved
  while powered, prevent the contact from touching any adjacent pin or chassis
  conductor.
