# Test Log

## RadioMaster ER5C V2 / MVP 0.5K

Validation period ending `2026-08-17`.

Test setup:

- RadioMaster ER5C V2 receiver running RZGX `4.0.1.5K`
- RadioMaster MT12 with internal 2.4 GHz ELRS transmitter
- Dynamic Power enabled with a `250 mW` maximum
- Integrated MT12 antenna rotated upright, perpendicular to the transmitter's
  top face
- DJI O3 Air Unit with MSP DisplayPort OSD
- Calibrated receiver analog VBAT sensing

Test duration and conditions:

- Multiple outdoor validation runs, including one longer than 17 minutes
- Final continuous outdoor run longer than 20 minutes
- Operation out to approximately 300 m with typical city-park obstructions
- Trees, walls, parked vehicles, and non-ideal positioning rather than a clean
  front-facing line of sight

Functional results:

- The disarmed CH2 gate blocked ESC output while GAS movement remained visible
  and `START FIRST` behaved as designed.
- Arming with non-neutral GAS displayed `GAS TO CENTER` and kept CH2 blocked
  until the input entered the neutral window.
- Repeated intentional failsafe tests with forward GAS held stopped the
  vehicle. After transmitter reconnection, CH2 remained blocked and displayed
  `GAS TO CENTER` until GAS returned to neutral.
- `FAILSAFE` blinked with RSSI/LQ, `START FIRST` and `GAS TO CENTER` blinked with
  GAS, and `RETURN NOW` blinked with battery voltage.
- Notification priority behaved as designed when warning states overlapped.
- Voltage Sensing Mode was physically checked in RX, 2S, 3S, and 4S modes.
- Native DJI displayed whole-pack voltage and Rover OSD displayed the intended
  receiver or average-per-cell voltage.
- Low-battery delay and Drive Timer behavior were confirmed.
- No unintended failsafe, control anomaly, or performance failure occurred.

Link observations:

- One or two Telemetry Lost / Telemetry Recovered notifications occurred in
  the final test without failsafe or a control-quality anomaly.
- This was substantially less frequent than earlier observations, despite the
  longer route and heavier obstruction. Antenna orientation may have
  contributed, but no controlled A/B comparison was performed.
- The DJI video link became unusable before the ELRS control link in the final
  route while observed ELRS LQ remained `99-100%`.
- These are installation-specific field observations, not calibrated range or
  RF-performance specifications.

Uncovered physical samples:

- Held reverse GAS reconnect was not intentionally sampled; held forward GAS
  reconnect was repeated successfully.
- The invalid-voltage fallback was not deliberately triggered.
- Physical battery testing covered RX, 2S, 3S, and 4S, not every 5S-8S option.

Field evidence:

- [Approximately 300 m with physical obstructions](assets/er5c-5k/field-test-300m-obstructed.png)
- [Intentional failsafe](assets/er5c-5k/osd-intentional-failsafe.png)
- [GAS TO CENTER after reconnect](assets/er5c-5k/osd-gas-to-center.png)
- [RETURN NOW warning](assets/er5c-5k/osd-return-now.png)
- [Firmware Information with Binding UID redacted](assets/er5c-5k/webui-firmware-information-redacted.jpg)
- [PWM and serial routing](assets/er5c-5k/webui-pwm-serial-routing.jpg)
- [DisplayPort serial selection](assets/er5c-5k/webui-displayport-serial.jpg)
- [Voltage sensing and warning settings](assets/er5c-5k/webui-voltage-sensing.jpg)
- [Rover OSD source summary](assets/er5c-5k/webui-rover-osd-sources.jpg)

Based on this validation, the exact ER5C V2 0.5K artifact is promoted as
Stable 05. ER5A V2 remains target-compatible but physically untested, and no
BETAFPV 0.5K artifact is produced.

## RadioMaster ER5C V2 / MVP 0.5I

Validation period ending `2026-08-09`.

Test setup:

- RadioMaster ER5C V2 receiver running RZGX `4.0.1.5I`
- RadioMaster MT12 with internal 2.4GHz ELRS transmitter
- Dynamic Power enabled with a `250 mW` maximum
- DJI Air Unit with MSP DisplayPort OSD
- Calibrated receiver analog VBAT sensing
- LiPo 2S and LiPo 4S packs

Test duration and conditions:

- More than five vehicle runs over approximately one week
- Individual runs between approximately 5 and 15 minutes
- Obstructed outdoor operation out to approximately 150 m
- Repeated operation around trees, benches, sidewalks, and buildings

Results:

- Voltage Mode behaved as designed in RX, 2S, and 4S configurations.
- Custom Rover OSD showed filtered average-per-cell voltage for cell-count
  modes, while the native DJI battery field showed whole-pack voltage.
- The optional low-battery warning, threshold, delay, recovery behavior, and
  WebUI persistence behaved as designed.
- `FAILSAFE` remained the highest-priority OSD notification when warning states
  overlapped.
- Arming, PWM steering/throttle control, UART DisplayPort, Wi-Fi configuration,
  and failsafe neutral positions retained the validated 0.5H behavior.
- No unintended failsafe or performance failure occurred during the recorded
  runs. A deliberate failsafe test confirmed that `FAILSAFE` overrides the
  low-battery `RETURN NOW` warning.
- Link quality remained stable at the farthest observed distance.

Telemetry observations:

- Telemetry Lost / Telemetry Recovered occurred above approximately 100 m with
  physical obstructions. A companion vehicle using original ExpressLRS 3.3.1
  also produced the notification under the same conditions.
- Repeated Telemetry Lost / Telemetry Recovered was observed at approximately
  50 m behind the transmitter with physical obstructions, while the companion
  receiver did not reproduce it there.
- These telemetry notifications did not produce failsafe or a control-quality
  anomaly. They remain a field observation, not proof of a firmware cause.

Based on these repeated physical tests, the exact ER5C V2 0.5I artifact is
promoted as Stable 04. ER5A V2 target compatibility and BETAFPV 0.5I behavior
remain outside this stable hardware claim.

## RadioMaster ER5C V2 / MVP 0.5H

Test dates: `2026-08-01` and `2026-08-02`

Test setup:

- RadioMaster ER5C V2 receiver running RZGX `4.0.1.5H`
- RadioMaster Boxer with internal 2.4GHz ELRS transmitter
- DJI Air Unit with MSP DisplayPort OSD
- Receiver analog VBAT input calibrated before the test
- Output 2 assigned to Serial TX and Output 3 assigned to Serial RX
- Initial tests used an LHCP replacement antenna with the same SMA connection
  because the RadioMaster Boxer stock T antenna was temporarily unavailable
- Follow-up testing used the recovered RadioMaster Boxer stock T antenna

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

Stock-antenna follow-up on `2026-08-02`:

- One continuous 15-minute vehicle run completed with consistent performance
  from start to finish.
- The vehicle repeatedly crossed the same approximately 60 m physically
  obstructed area that had produced Telemetry Lost / Telemetry Recovered with
  the replacement LHCP antenna.
- No Telemetry Lost / Telemetry Recovered audio notification occurred during
  the follow-up run.
- LQ remained above `90%` in that area, compared with the earlier observed
  `75-80%` dips using the replacement antenna.
- No failsafe, control anomaly, OSD anomaly, or other performance failure was
  observed.

Field evidence:

- [Approximately 60 m with physical obstructions](assets/er5c-5h/field-test-60m-nlos.png):
  timer `08:33`, custom battery `3.57 V` per cell, native battery `7.1 V`
  whole pack, RSSI `-90`, and LQ `100%` in the captured frame.
- [Approximately 5 m](assets/er5c-5h/field-test-5m.png): timer `00:38`, custom
  battery `3.71 V` per cell, native battery `7.4 V` whole pack, RSSI `-71`, and
  LQ `100%` in the captured frame.
- [Firmware Information page with Binding UID redacted](assets/er5c-5h/webui-firmware-information-redacted.jpg):
  confirms the RadioMaster ER5A/C V2 target and embedded RZGX build `4.0.1.5H`.
- [PWM and serial routing](assets/er5c-5h/webui-pwm-serial-routing.jpg)
- [Rover OSD menu](assets/er5c-5h/webui-rover-osd-menu.jpg)
- [Rover OSD settings and two-cell configuration](assets/er5c-5h/webui-rover-osd-settings.jpg)
- [DisplayPort serial selection](assets/er5c-5h/webui-displayport-serial.jpg)

The distance and signal observations are field evidence, not calibrated range
measurements. The improvement with the stock transmitter antenna is consistent
with an antenna, orientation, or installation effect, but does not establish a
controlled range specification.

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

