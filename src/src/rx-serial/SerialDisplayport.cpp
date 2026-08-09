/************************************************************************************
Credits:
  This software is based on and uses software published by Richard Amiss 2023,
  QLiteOSD, which is based on work by Paul Kurucz (pkuruz):opentelem_to_bst_bridge 
  as well as software from d3ngit : djihdfpv_mavlink_to_msp_V2 and 
  crashsalot : VOT_to_DJIFPV

THIS SOFTWARE IS PROVIDED IN AN "AS IS" CONDITION. NO WARRANTIES, WHETHER EXPRESS, 
IMPLIED OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF 
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. THE 
COMPANY SHALL NOT, IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL OR 
CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.
************************************************************************************/

#if defined(TARGET_RX)

#include "SerialDisplayport.h"
#include "CRSFRouter.h"
#include "devAnalogVbat.h"
#include "OTA.h"
#include "config.h"
#include "options.h"

static constexpr uint8_t MSP_DP_HEARTBEAT = 0;
static constexpr uint8_t MSP_DP_CLEAR_SCREEN = 2;
static constexpr uint8_t MSP_DP_WRITE_STRING = 3;
static constexpr uint8_t MSP_DP_DRAW_SCREEN = 4;

static constexpr uint8_t OSD_COLUMNS = 53;
static constexpr uint32_t OSD_UPDATE_INTERVAL_MS = 100;
static constexpr uint8_t OSD_CENTER_ROW = 10;
static constexpr uint32_t FAILSAFE_BLINK_INTERVAL_MS = 250;
static constexpr uint32_t ENGINE_START_BLINK_INTERVAL_MS = 250;
static constexpr uint32_t ENGINE_START_BLINK_DURATION_MS = 1500;
static constexpr uint32_t LOW_BATTERY_BLINK_INTERVAL_MS = 500;
static constexpr uint16_t LOW_BATTERY_HYSTERESIS_CENTIVOLTS = 10;
static constexpr uint32_t LOW_BATTERY_RECOVERY_MS = 2000;
static constexpr char OSD_ARROW_DOWN = 0x60;
static constexpr char OSD_ARROW_RIGHT = 0x64;
static constexpr char OSD_ARROW_UP = 0x68;
static constexpr char OSD_ARROW_LEFT = 0x6C;
static constexpr char OSD_RSSI = 0x01;
static constexpr char OSD_LINK_QUALITY = 0x7B;
static constexpr char OSD_BATTERY = static_cast<char>(0x90);

struct msp_analog_t
{
    uint8_t legacyVoltageDecivolts;
    uint16_t mAhDrawn;
    uint16_t rssi;
    int16_t currentCentiamps;
    uint16_t voltageCentivolts;
} __attribute__ ((packed));

struct msp_battery_state_t
{
    uint8_t cellCount;
    uint16_t capacityMah;
    uint8_t legacyVoltageDecivolts;
    uint16_t mAhDrawn;
    int16_t currentCentiamps;
    uint8_t batteryState;
    uint16_t voltageCentivolts;
} __attribute__ ((packed));

static uint8_t centerColumn(const char *text)
{
    const size_t length = strlen(text);
    return length >= OSD_COLUMNS ? 0 : (OSD_COLUMNS - length) / 2;
}

static uint8_t rightColumn(const char *text)
{
    const size_t length = strlen(text);
    return length >= OSD_COLUMNS ? 0 : OSD_COLUMNS - length;
}

static int8_t channelPercent(uint32_t value)
{
    if (value == CRSF_CHANNEL_VALUE_UNSET)
        return 0;

    int32_t percent;
    if (value >= CRSF_CHANNEL_VALUE_MID)
    {
        percent = (static_cast<int32_t>(value) - CRSF_CHANNEL_VALUE_MID) * 100 /
                  (CRSF_CHANNEL_VALUE_2000 - CRSF_CHANNEL_VALUE_MID);
    }
    else
    {
        percent = -((CRSF_CHANNEL_VALUE_MID - static_cast<int32_t>(value)) * 100 /
                    (CRSF_CHANNEL_VALUE_MID - CRSF_CHANNEL_VALUE_1000));
    }

    percent = constrain(percent, -100, 100);
    return (percent >= -1 && percent <= 1) ? 0 : static_cast<int8_t>(percent);
}

void SerialDisplayport::send(uint8_t messageID, const void *payload, uint8_t size)
{
    _outputPort->write('$');
    _outputPort->write('M');
    _outputPort->write('>');
    _outputPort->write(size);
    _outputPort->write(messageID);
    uint8_t checksum = size ^ messageID;
    const uint8_t *payloadPtr = static_cast<const uint8_t *>(payload);
    for (uint8_t i = 0; i < size; ++i)
    {
        checksum ^= payloadPtr[i];
    }
    _outputPort->write(payloadPtr, size);
    _outputPort->write(checksum);
}

void SerialDisplayport::sendDisplayPort(uint8_t command)
{
    send(MSP_DISPLAYPORT, &command, 1);
}

void SerialDisplayport::sendDisplayPortString(uint8_t row, uint8_t col, const char *text)
{
    uint8_t payload[34];
    uint8_t size = 0;
    payload[size++] = MSP_DP_WRITE_STRING;
    payload[size++] = row;
    payload[size++] = col;
    payload[size++] = 0;
    while (*text != '\0' && size < sizeof(payload))
        payload[size++] = static_cast<uint8_t>(*text++);
    send(MSP_DISPLAYPORT, payload, size);
}

void SerialDisplayport::sendBatteryTelemetry()
{
    uint16_t voltageCentivolts;
    if (!Vbat_getVoltage(voltageCentivolts))
        return;

    const uint8_t legacyVoltageDecivolts = static_cast<uint8_t>(min(
        static_cast<uint16_t>((voltageCentivolts + 5U) / 10U),
        static_cast<uint16_t>(UINT8_MAX)));

    const msp_analog_t analog = {
        legacyVoltageDecivolts,
        0,
        0,
        0,
        voltageCentivolts
    };
    send(MSP_ANALOG, &analog, sizeof(analog));

    const msp_battery_state_t battery = {
        static_cast<uint8_t>(max(config.GetRoverCellCount(), static_cast<uint8_t>(1))),
        0,
        legacyVoltageDecivolts,
        0,
        0,
        0,
        voltageCentivolts
    };
    send(MSP_BATTERY_STATE, &battery, sizeof(battery));
}

void SerialDisplayport::resetLowBatteryWarning()
{
    m_lowBatteryStartedAt = 0;
    m_lowBatteryRecoveryStartedAt = 0;
    m_lowBatteryPending = false;
    m_lowBatteryRecovering = false;
    m_lowBatteryWarningActive = false;
}

bool SerialDisplayport::updateLowBatteryWarning(uint32_t now, bool voltageValid, uint16_t displayedCentivolts)
{
    if (!config.GetRoverLowBatteryEnabled() || config.GetRoverCellCount() == 0 ||
        !voltageValid || displayedCentivolts == 0)
    {
        resetLowBatteryWarning();
        return false;
    }

    const uint16_t threshold = config.GetRoverLowBatteryThresholdCentivolts();
    if (!m_lowBatteryWarningActive)
    {
        m_lowBatteryRecovering = false;
        m_lowBatteryRecoveryStartedAt = 0;
        if (displayedCentivolts < threshold)
        {
            const uint16_t delayMs = config.GetRoverLowBatteryDelayMs();
            if (delayMs == 0)
            {
                m_lowBatteryWarningActive = true;
                m_lowBatteryPending = false;
            }
            else if (!m_lowBatteryPending)
            {
                m_lowBatteryPending = true;
                m_lowBatteryStartedAt = now;
            }
            else if (now - m_lowBatteryStartedAt >= delayMs)
            {
                m_lowBatteryWarningActive = true;
                m_lowBatteryPending = false;
            }
        }
        else
        {
            m_lowBatteryPending = false;
            m_lowBatteryStartedAt = 0;
        }
    }
    else
    {
        m_lowBatteryPending = false;
        m_lowBatteryStartedAt = 0;
        const uint16_t recoveryThreshold = threshold + LOW_BATTERY_HYSTERESIS_CENTIVOLTS;
        if (displayedCentivolts >= recoveryThreshold)
        {
            if (!m_lowBatteryRecovering)
            {
                m_lowBatteryRecovering = true;
                m_lowBatteryRecoveryStartedAt = now;
            }
            else if (now - m_lowBatteryRecoveryStartedAt >= LOW_BATTERY_RECOVERY_MS)
            {
                resetLowBatteryWarning();
            }
        }
        else
        {
            m_lowBatteryRecovering = false;
            m_lowBatteryRecoveryStartedAt = 0;
        }
    }

    return m_lowBatteryWarningActive;
}

void SerialDisplayport::renderRoverOsd(bool armed, const uint32_t *channelData)
{
    const uint32_t now = millis();
    const char *craftName = config.GetRoverCraftName();
    const int8_t steeringPercent = channelPercent(channelData[0]);
    const int8_t gasPercent = channelPercent(channelData[1]);
    const char steeringDirection = steeringPercent == 0 ? '-' :
        (steeringPercent < 0 ? OSD_ARROW_LEFT : OSD_ARROW_RIGHT);
    const char gasDirection = gasPercent == 0 ? '-' :
        (gasPercent < 0 ? OSD_ARROW_DOWN : OSD_ARROW_UP);

    if (armed && !m_lastArmedState)
        m_engineStartBlinkStartedAt = now;
    else if (!armed)
        m_engineStartBlinkStartedAt = 0;
    m_lastArmedState = armed;

    char steeringText[16];
    char gasText[16];
    char rssiText[10];
    char lqText[12];
    char batteryText[12];
    uint16_t voltageCentivolts = 0;
    const bool voltageValid = Vbat_getVoltage(voltageCentivolts);
    uint16_t displayedCentivolts = voltageCentivolts;
    batteryText[0] = OSD_BATTERY;
    if (voltageValid && voltageCentivolts > 0)
    {
        const uint8_t cellCount = config.GetRoverCellCount();
        displayedCentivolts = cellCount == 0
            ? voltageCentivolts
            : (voltageCentivolts + cellCount / 2U) / cellCount;
        snprintf(batteryText + 1, sizeof(batteryText) - 1, " %u.%02uV",
                 static_cast<unsigned>(displayedCentivolts / 100U),
                 static_cast<unsigned>(displayedCentivolts % 100U));
    }
    else
    {
        strncpy(batteryText + 1, " -V", sizeof(batteryText) - 1);
        batteryText[sizeof(batteryText) - 1] = '\0';
    }
    const bool lowBatteryWarning = updateLowBatteryWarning(now, voltageValid, displayedCentivolts);
    const char *stateText = nullptr;
    if (failsafe)
    {
        if ((now / FAILSAFE_BLINK_INTERVAL_MS) % 2 == 0)
            stateText = "FAILSAFE";
    }
    else if (lowBatteryWarning)
    {
        if ((now / LOW_BATTERY_BLINK_INTERVAL_MS) % 2 == 0)
            stateText = "RETURN NOW";
    }
    else if (!armed)
    {
        stateText = "STANDBY";
    }
    else if (m_engineStartBlinkStartedAt != 0)
    {
        const uint32_t blinkElapsed = now - m_engineStartBlinkStartedAt;
        if (blinkElapsed < ENGINE_START_BLINK_DURATION_MS &&
            (blinkElapsed / ENGINE_START_BLINK_INTERVAL_MS) % 2 == 0)
        {
            stateText = "ENGINE START";
        }
    }
    const uint8_t rssiMagnitude = linkStats.active_antenna != 0 && linkStats.uplink_RSSI_2 != 0
        ? linkStats.uplink_RSSI_2
        : linkStats.uplink_RSSI_1;
    snprintf(steeringText, sizeof(steeringText), "STR %c %d%%", steeringDirection, abs(static_cast<int>(steeringPercent)));
    snprintf(gasText, sizeof(gasText), "GAS %c %d%%", gasDirection, abs(static_cast<int>(gasPercent)));
    snprintf(rssiText, sizeof(rssiText), "%c -%u", OSD_RSSI, static_cast<unsigned>(rssiMagnitude));
    snprintf(lqText, sizeof(lqText), "%c %u%%", OSD_LINK_QUALITY,
             static_cast<unsigned>(constrain(linkStats.uplink_Link_quality, 0, 100)));

    sendDisplayPort(MSP_DP_HEARTBEAT);
    sendDisplayPort(MSP_DP_CLEAR_SCREEN);
    sendDisplayPortString(0, centerColumn(craftName), craftName);
    if (stateText != nullptr)
        sendDisplayPortString(OSD_CENTER_ROW, centerColumn(stateText), stateText);
    sendDisplayPortString(13, 1, batteryText);
    sendDisplayPortString(15, 1, steeringText);
    sendDisplayPortString(16, 1, gasText);
    sendDisplayPortString(15, rightColumn(rssiText), rssiText);
    sendDisplayPortString(16, rightColumn(lqText), lqText);
    sendDisplayPort(MSP_DP_DRAW_SCREEN);
}

uint32_t SerialDisplayport::sendRCFrame(bool frameAvailable, bool frameMissed, uint32_t *channelData)
{
    bool armed = getArmedState();

    msp_status_t status;
    status.task_delta_time = 0;
    status.i2c_error_count = 0;
    status.sensor_status = 0;
    status.flight_mode_flags = armed ? 0x1 : 0x0;
    status.pid_profile = 0;
    status.system_load = 0;
    status.gyro_cycle_time = 0;
    status.box_mode_flags = 0;
    status.arming_disable_flags_count = 1;
    status.arming_disable_flags = armed ? 0x0 : 0x1;
    status.extra_flags = 0;

    // Send status MSP
    send(MSP_STATUS, &status, sizeof(status));

    // Send extended status MSP
    send(MSP_STATUS_EX, &status, sizeof(status));

    if (m_receivedBytes >= 6 && millis() - m_lastBatteryTransaction >= MSP_BATTERY_PERIOD_MS)
    {
        sendBatteryTelemetry();
        m_lastBatteryTransaction = millis();
    }

    if (config.GetRoverOsdEnabled() && m_receivedBytes >= 6 && millis() - m_lastOsdTransaction >= OSD_UPDATE_INTERVAL_MS)
    {
        renderRoverOsd(armed, channelData);
        m_lastOsdTransaction = millis();
    }

    return MSP_MSG_PERIOD_MS;   // Send MSP msgs to DJI at 10Hz
}

void SerialDisplayport::processBytes(uint8_t *bytes, u_int16_t size)
{
    // Super-basic air-unit detection:
    // Wait for at least 6 bytes to be received (minimum MSP msg length)
    // before we decide we are connected to a DJI air unit
    if (m_receivedBytes < 6)
    {
      m_receivedBytes += size;
    }
}

bool SerialDisplayport::getArmedState()
{
    if (firmwareOptions.dji_permanently_armed)
    {
        // If we are using permanent arming then we need to make sure the air-unti is connected
        // The O3 needs to see the arm state change (i.e. false --> true) after is has fully booted
        // Wait for activity on the UART from the air-unit, then wait 10 seconds before arming

        if (m_receivedBytes >= 6)
        {
            // Start the timer if it's the first time receiving 6 or more bytes
            if (m_receivedTimestamp == 0)
            {
                m_receivedTimestamp = millis();
            }
            // Arm permanently after 10 seconds
            return millis() > m_receivedTimestamp + 10000;
        }

        return false;
    }
    else
    {
        // If we are not using permanent arming then we don't need to wait for the air-unit to be connected
        // The arm channel will provide the required state change to arm the O3
        return isArmed;
    }
}

#endif // defined(TARGET_RX)
