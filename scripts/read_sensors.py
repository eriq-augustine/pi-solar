#!/usr/bin/env python3

import collections
import time

import spidev

VOLTAGE_MULTIPLIER = 0.0161446  # 3.5 V Reference
# VOLTAGE_MULTIPLIER = 0.0261097  # 5.0 V Reference

CURRENT_BASELINE = 514.5
CURRENT_MULTIPLIER = 0.0750000  # 5.0 V Reference

MAX_SAMPLING_SPEED = 1000000

VOLTAGE_CHANNEL = 0
CURRENT_CHANNEL = 1

SAMPLING_WINDOW_SIZE = 1000
SAMPLES_PER_SEC = 1000

LOG_PERIOD = SAMPLING_WINDOW_SIZE

# Read MCP3008 data.
def sampleChannel(spi, channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return int(data)

def main():
    # Start SPI connection.
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = MAX_SAMPLING_SPEED

    voltageWindow = collections.deque()
    currentWindow = collections.deque()

    numSamples = 0

    while True:
        rawVoltage = sampleChannel(spi, VOLTAGE_CHANNEL)
        rawCurrent = sampleChannel(spi, CURRENT_CHANNEL)

        # Failed read.
        # We may get bad voltages that are hard to tell, but bad currents are obvious.
        if (rawCurrent == 0):
            continue

        voltageWindow.append(rawVoltage)
        currentWindow.append(rawCurrent)

        numSamples += 1

        if (len(currentWindow) > SAMPLING_WINDOW_SIZE):
            voltageWindow.popleft()
            currentWindow.popleft()

            windowRawVoltage = sum(voltageWindow) / SAMPLING_WINDOW_SIZE
            windowRawCurrent = sum(currentWindow) / SAMPLING_WINDOW_SIZE

            windowVoltage = windowRawVoltage * VOLTAGE_MULTIPLIER
            windowCurrent = (CURRENT_BASELINE - windowRawCurrent) * CURRENT_MULTIPLIER

            if (numSamples % LOG_PERIOD == 0):
                print("Raw Voltage: %f, Voltage: %f V, Raw Current: %f, Current: %f A" % (windowRawVoltage, windowVoltage, windowRawCurrent, windowCurrent))

        time.sleep(1 / SAMPLES_PER_SEC)

if (__name__ == '__main__'):
    main()
