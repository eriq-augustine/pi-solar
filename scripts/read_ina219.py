#!/usr/bin/env python3

import math
import time

import ina219

SHUNT_RESISTANCE_OHMS = 0.1
MAX_EXPECTED_CURRENT_AMPS = 1.5

SLEEP_TIME_SEC = 3

# Return: (Bus Voltage (V), Bus Current (A), Power (W), Shunt Voltage (V)).
def read(ina):
    voltage = ina.voltage()

    current = None
    power = None
    shuntVoltage = None

    try:
        current = ina.current()
        if (not math.isclose(0.0, current)):
            current /= 1000.0

        power = ina.power()
        if (not math.isclose(0.0, power)):
            power /= 1000.0

        shuntVoltage = ina.shunt_voltage()
        if (not math.isclose(0.0, shuntVoltage)):
            shuntVoltage /= 1000.0
    except ina219.DeviceRangeError as ex:
        # Current out of device range with specified shunt resistor.
        print("Error reading current: %s" % (ex))

    return (voltage, current, power, shuntVoltage)

def main():
    ina = ina219.INA219(SHUNT_RESISTANCE_OHMS, MAX_EXPECTED_CURRENT_AMPS)
    ina.configure(
            voltage_range = ina219.INA219.RANGE_32V,
            bus_adc = ina219.INA219.ADC_16SAMP,
            shunt_adc = ina219.INA219.ADC_16SAMP)

    while True:
        voltage, current, power, shuntVoltage = read(ina)
        print("Voltage: %f V, Current: %f A, Power: %f W" % (voltage, current, power))
        time.sleep(SLEEP_TIME_SEC)

if __name__ == "__main__":
    main()
