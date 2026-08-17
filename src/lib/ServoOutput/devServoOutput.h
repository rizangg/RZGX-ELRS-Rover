#pragma once
#if defined(TARGET_RX)

#include "device.h"
#include "common.h"

#if defined(PLATFORM_ESP32)
#include "DShotRMT.h"
#endif

extern device_t ServoOut_device;

// Notify this unit that new channel data has arrived
void servoNewChannelsAvailable();
// Copy the current output values to the config's failsafe values
void servoCurrentToFailsafeConfig();
// ER5 rover safety gate state used by the OSD and PWM output path
bool roverGasSafetyGateEnabled();
bool roverGasSafetyGateSatisfied();

#endif
