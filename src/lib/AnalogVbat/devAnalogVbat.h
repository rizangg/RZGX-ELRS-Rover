#pragma once

#include "common.h"
#include "device.h"

void Vbat_enableSlowUpdate(bool enable);
bool Vbat_getVoltage(uint16_t &centivolts);

extern device_t AnalogVbat_device;
