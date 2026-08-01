# Test Log

## RadioMaster ER5C V2 / MVP 0.5H

Test date: `2026-08-01`

Test setup:

- RadioMaster ER5C V2 receiver running RZGX `4.0.1.5H`
- RadioMaster Boxer with internal 2.4GHz ELRS transmitter
- DJI Air Unit with MSP DisplayPort OSD
- Receiver analog VBAT input calibrated before the test
- Output 2 assigned to Serial TX and Output 3 assigned to Serial RX
- RadioMaster Boxer stock T antenna unavailable; an LHCP antenna with the same
  SMA connection was used instead

Test duration and conditions:

- Two daytime vehicle runs longer than five minutes each
- One night vehicle run longer than ten minutes
- Indoor and outdoor operation
- Distance observation around 60 m with concrete walls, metal fencing, and
  neighboring structures obstructing clean line of sight

Results:

- Flashing to 0.5H completed normally.
- Arming and PWM steering/throttle control behaved as intended.
- Turning off the transmitter triggered the FAILSAFE indication.
- Steering and ESC outputs returned to their configured neutral positions on
  failsafe.
- STR and GAS OSD fields retained the last valid received values during
  failsafe; this is display behavior and did not reflect the neutral PWM output.
- Custom Rover OSD battery voltage displayed filtered average-per-cell voltage.
- Native DJI battery voltage displayed whole-pack voltage.
- At approximately 60 m with physical obstructions, Telemetry Lost followed by
  Telemetry Recovered occurred without FAILSAFE. Observed LQ varied around
  `76-90%` during that condition.
- No performance failure or unexpected behavior was observed during the three
  runs.

Field evidence:

- [Approximately 60 m with physical obstructions](assets/er5c-5h/field-test-60m-nlos.png):
  timer `08:33`, custom battery `3.57 V` per cell, native battery `7.1 V`
  whole pack, RSSI `-90`, and LQ `100%` in the captured frame.
- [Approximately 5 m](assets/er5c-5h/field-test-5m.png): timer `00:38`, custom
  battery `3.71 V` per cell, native battery `7.4 V` whole pack, RSSI `-71`, and
  LQ `100%` in the captured frame.
- [PWM and serial routing](assets/er5c-5h/webui-pwm-serial-routing.jpg)
- [Rover OSD menu](assets/er5c-5h/webui-rover-osd-menu.jpg)
- [Rover OSD settings and two-cell configuration](assets/er5c-5h/webui-rover-osd-settings.jpg)
- [DisplayPort serial selection](assets/er5c-5h/webui-displayport-serial.jpg)

The distance and signal observations are field evidence, not calibrated range
measurements. The replacement transmitter antenna and obstructed path prevent a
direct comparison with controlled stock-antenna line-of-sight tests.

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

