# Test Log

## Stable 02 / MVP 0.5D

Summary:

- Indoor test: stable OSD and link.
- Outdoor test: stable OSD and link up to around 80 meters.
- Repeated morning-to-midday test runs: stable.
- Continuous CH2 use: stable.
- Second same-type receiver: stable after Craft Name and Binding Phrase were
  changed through WiFi Configurator.

Radio configuration used for these field tests:

- RadioMaster Boxer with internal 2.4GHz ELRS transmitter
- Packet rate: `150Hz`
- Maximum TX power: `1000mW`
- Dynamic Power: enabled

Observed RSSI:

- Indoor close range: around `-30` to `-40`
- Outdoor around 60 meters: around `-60` to `-70`
- Outdoor around 80 meters: `-80` with `100%` Link Quality in the captured
  frame.

These values are field observations, not calibrated lab measurements.

## Field Evidence

- [Night adventure](images/field-tests/night-adventure.png): night driving
  capture with the rover OSD active.
- [Approximately 80-meter range test](images/field-tests/80-meter-distance.png):
  daytime range capture showing `-80` RSSI and `100%` Link Quality.
- [Extended full-throttle use](images/field-tests/extended-full-throttle.png):
  capture showing `100%` gas and `100%` Link Quality.
- [ENGINE START OSD](images/field-tests/engine-start-osd.png): capture of the
  arming/start transition rendered by the receiver-side OSD.

## Earlier Development Notes

- MVP 0.2 displayed full OSD but caused repeated link instability.
- MVP 0.3 restored link stability but OSD did not display.
- MVP 0.4A displayed static test OSD with stable link.
- MVP 0.4C displayed Craft Name and arming state with stable link.
- MVP 0.5 displayed full OSD but broke binding/runtime option persistence.
- MVP 0.5A fixed binding/runtime option handling and became the first stable
  baseline.
- MVP 0.5D adds refined layout and RSSI while preserving stable link behavior.

