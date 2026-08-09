# Implemented 0.5I Design Notes

This archive preserves the design decisions that were formerly listed as the
next patch after 0.5H. They were implemented, physically tested on RadioMaster
ER5C V2, and promoted as Stable 04 / MVP 0.5I.

## Voltage Mode

The WebUI offers RX plus manual 1S-8S interpretation. RX shows the measured
receiver/BEC voltage without per-cell division. Selecting 1S-8S divides the
filtered whole-pack measurement for the custom per-cell OSD while leaving the
native DJI field as whole-pack voltage. The WebUI explains that this setting
does not electrically select a source: the user must move or disconnect the
physical ADC sensing lead.

## Low-Battery Warning

Low-battery warning is available only in 1S-8S modes. The defaults and limits
implemented in 0.5I are:

- threshold default: 3.50 V per cell;
- threshold range: 2.50-4.50 V in 0.01 V steps;
- delay choices: immediate, 1, 3, 5, or 10 seconds; default 3 seconds;
- recovery: threshold plus 0.10 V continuously for 2 seconds;
- warning text: flashing `RETURN NOW`;
- priority: `FAILSAFE` always overrides the low-battery warning.

Selecting RX automatically disables the warning. Native DJI whole-pack voltage
is not changed by the per-cell warning calculation.

## Rover OSD WebUI Icon

The dedicated Rover OSD navigation icon was implemented and tested in the
embedded WebUI. Physical testing found it functional but visually wider than
ideal. It is intentionally retained for the 0.5J iteration so icon redesign
does not become coupled to the safety-gate work.

## Validation Result

The settings survived save, reboot, and Wi-Fi mode re-entry. Voltage display
was tested with 2S and 4S LiPo packs; the low-battery trigger, delay, recovery,
and FAILSAFE message priority behaved as designed. More than five ER5C V2 test
runs of 5-15 minutes were completed, including an obstructed range of roughly
150 metres, without an unintended failsafe or performance failure.
