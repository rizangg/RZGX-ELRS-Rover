# Next Patch Notes (Unversioned)

This document records the agreed scope for the patch after the current 0.5H
baseline. It is a planning note only: it does not assign a release label and
does not change the 0.5H source, WebUI, or firmware artifacts.

## 1. Battery Cell Count Notice

Add a visible notice beside the `Battery Cell Count` setting in the Rover OSD
page:

> Battery Cell Count is used to calculate the per-cell OSD voltage. An
> incorrect value will produce a misleading per-cell reading. Set the actual
> number of cells in series (1S-8S). If the VBAT lead is moved to a battery
> with a different cell count, update this setting. The native DJI whole-pack
> voltage is not affected.

Keep the current manual 1S-8S selection. Automatic cell-count detection is not
part of this patch. Manual selection is more predictable for the tested rover
installation, where the ER5C sense lead can be moved between batteries with
different pack configurations. A future detector may suggest a likely cell
count, but it must ask the user to confirm and must not silently overwrite the
configured value.

## 2. User-Configured Low-Battery Warning

Add a user-configurable low-battery threshold based on the same filtered
average-per-cell voltage shown by the custom Rover OSD. When the voltage stays
below that threshold for the configured trigger delay, show a flashing
`RETURN NOW` warning on the OSD.

The trigger delay must be selectable by the user and include an immediate
option plus one-second and multi-second choices. The delay is continuous: if
the filtered voltage recovers above the threshold before the delay expires,
the pending warning must be cancelled. The implementation must also include a
small recovery hysteresis so normal voltage ripple near the threshold does not
rapidly toggle the warning.

The warning must not replace or weaken the existing FAILSAFE behavior.
FAILSAFE remains the higher-priority safety indication. Whole-pack voltage sent
to the native DJI battery field remains unchanged.

The following values remain to be agreed before implementation:

- default state and default voltage threshold;
- allowed threshold range and input precision;
- exact delay choices;
- recovery hysteresis and warning-clear behavior;
- screen position and priority relative to other temporary OSD messages.

## 3. Rover OSD WebUI Icon

Replace the generic Rover OSD navigation icon, if the WebUI asset pipeline and
flash budget permit it, with a compact monochrome icon based on the supplied
[Rover OSD source artwork](assets/design/rover-osd-icon.pdf): an FPV-goggles
outline with `OSD` lettering.

The PDF is a design reference, not an embeddable WebUI asset. Before use, the
mark should be converted to a clean, tightly cropped SVG or equivalent
single-color icon, simplified and tested at the actual navigation-menu size.
It must inherit the existing menu foreground color, remain legible on desktop
and mobile layouts, and avoid adding a large raster or the full PDF to the
embedded WebUI.

An initial configurator mock found the 24 px version readable but visually
fragile, while the 32 px version was substantially clearer. The final width is
not yet fixed and must be confirmed before the firmware patch.

## Validation Required

Before publishing the patch:

- verify the new settings survive save, reboot, and Wi-Fi mode re-entry;
- test 1S and multi-cell calculations, invalid input handling, and movement of
  the VBAT lead between packs with different cell counts;
- test voltage dips shorter and longer than every available delay;
- test threshold hysteresis and warning recovery;
- confirm FAILSAFE still overrides the low-battery message;
- verify the icon at the actual drawer size on both desktop and mobile;
- rebuild and audit each supported receiver target without replacing any 0.5H
  source documentation or binary artifact.
