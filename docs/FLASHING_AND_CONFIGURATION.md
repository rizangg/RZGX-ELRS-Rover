# Flashing And Configuration

## Safe Flashing Path

Use the standard receiver WiFi update page.

1. Power the receiver.
2. Put the receiver into WiFi mode.
3. Connect to the receiver WiFi network.
4. Open the receiver WiFi Configurator.
5. Open **Update**.
6. Upload the correct `firmware.bin.gz`.
7. Wait until the update finishes.
8. Reboot the receiver.

## Target Warning

Only flash firmware built for the exact receiver target:

| Tested receiver | Required firmware identity | Current stable build |
| --- | --- | --- |
| BETAFPV PWM 2.4GHz RX | `BETAFPV PWM 2.4GHz RX` | Stable 02 / MVP 0.5D |
| RadioMaster ER5C V2 | `RadioMaster ER5A/C V2 2.4GHz PWM RX` | Stable 04 / MVP 0.5I |

ER5A V2 shares the ER5A/C V2 firmware identity but has not been physically
validated by this project.

Flashing the wrong target can make the receiver fail to boot and may require
USB-to-UART recovery.

## USB-to-UART Recovery

The following USB-to-UART procedure was physically tested only on the BETAFPV
PWM receiver. If its WiFi mode is unavailable after a bad flash, use a 3.3V
USB-to-UART adapter such as a CP2102 and the exact
`BETAFPV PWM 2.4GHz RX` target.

Field-tested wiring:

| CP2102 Pin | Receiver Pin |
| --- | --- |
| TX | RX |
| RX | TX |
| GND | GND |

Field-tested bootloader sequence:

1. Connect the USB-to-UART adapter.
2. Hold the receiver BOOT button.
3. Start flashing.
4. Keep holding BOOT until flashing finishes.

In the tested recovery case, USB power was enough and a separate external 5V
supply was not required.

Do not apply the BETAFPV target or boot sequence to an ER5C. For ER5C recovery,
use the official `RadioMaster ER5A/C V2 2.4GHz PWM RX` target and RadioMaster's
documented bootloader procedure.

## Binding

Use the normal ExpressLRS Binding page.

Recommended:

- Set Binding Phrase or Binding UID in WiFi Configurator.
- Save.
- Reboot.
- Confirm the receiver connects to the transmitter.

Avoid direct binary binding edits unless you know the ExpressLRS firmware
options block. A bad binary patch can break binding or option persistence.

## Output Mapping

For the tested BETAFPV and ER5C setups:

| Output | Setting |
| --- | --- |
| Output 1 | `ch1` / steering |
| Output 2 | `TX` |
| Output 3 | `RX` |
| Output 4 | `ch2` / gas |
| Output 5 | `ch3` |

Then set the serial protocol to DisplayPort/MSP DisplayPort and enable Rover
OSD.

## ER5C Stable 04 Voltage Configuration

The ER5C V2 Stable 04 WebUI provides these `Voltage Mode` choices:

| Mode | Physical sensing lead | Custom Rover OSD | Native DJI battery field |
| --- | --- | --- | --- |
| `RX` | External sensing lead disconnected | Receiver/ESC-BEC voltage | Same receiver/ESC-BEC voltage |
| `1S`-`8S` | Connected to verified whole-pack positive | Average voltage per cell | Whole-pack voltage |

The menu changes only how firmware interprets the analog reading. It cannot
select or switch the electrical voltage source. Choosing the wrong mode, cell
count, or physical connection produces misleading voltage information.

The optional low-battery warning is available only in `1S`-`8S` modes. It uses
the configured average-per-cell threshold and continuous delay. Selecting `RX`
automatically disables the warning because regulated BEC voltage is not a
reliable battery-state indicator.

See [ER5C V2 VBAT Sense Wiring](ER5C_VBAT_WIRING.md) before connecting the
external sensing lead.

## DJI Wiring

The tested setup uses separate power sources:

- the ELRS PWM receiver is powered by the vehicle receiver/ESC 5V rail;
- the DJI Air Unit is powered by an external LiPo/BEC supply;
- both systems must share ground.

Receiver side wiring:

| Receiver Pin | Connects To | Notes |
| --- | --- | --- |
| Output 2 `S` / TX | DJI Air Unit RX | UART signal |
| Output 2 `V` | Not connected | Do not power the Air Unit from this pin |
| Output 2 `G` | DJI Air Unit GND | Common ground |
| Output 3 `S` / RX | DJI Air Unit TX | UART signal |
| Output 3 `V` | Not connected | Not used |
| Output 3 `G` | Optional / not required | Ground is already shared through Output 2 |

DJI Air Unit side wiring:

| DJI Air Unit Pin | Connects To |
| --- | --- |
| VCC | External Air Unit power positive |
| GND | External Air Unit power negative and receiver ground |
| RX | Receiver Output 2 `S` / TX |
| TX | Receiver Output 3 `S` / RX |
| SBUS | Not used |
| SBUS GND | Not used |

TX/RX must be crossed. Receiver TX goes to Air Unit RX, and Air Unit TX goes to
receiver RX.

Never connect the receiver output `V` pin directly to the DJI Air Unit power
pin.
