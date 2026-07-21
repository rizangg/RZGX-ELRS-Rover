# Test Log

## Stable 02 / MVP 0.5D

Summary:

- Indoor test: stable OSD and link.
- Outdoor test: stable OSD and link up to around 60 meters.
- Repeated morning-to-midday test runs: stable.
- Continuous CH2 use: stable.
- Second same-type receiver: stable after Craft Name and Binding Phrase were
  changed through WiFi Configurator.

Observed RSSI:

- Indoor close range: around `-30` to `-40`
- Outdoor around 60 meters: around `-60` to `-70`

These values are field observations, not calibrated lab measurements.

## Earlier Development Notes

- MVP 0.2 displayed full OSD but caused repeated link instability.
- MVP 0.3 restored link stability but OSD did not display.
- MVP 0.4A displayed static test OSD with stable link.
- MVP 0.4C displayed Craft Name and arming state with stable link.
- MVP 0.5 displayed full OSD but broke binding/runtime option persistence.
- MVP 0.5A fixed binding/runtime option handling and became the first stable
  baseline.
- MVP 0.5D adds refined layout and RSSI while preserving stable link behavior.

