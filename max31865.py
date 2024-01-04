from micropython import const

import machine
import time
import math

_MAX31865_CONFIGURATION_REG = const(0x00)
_MAX31865_RTD_MSB_REG = const(0x01)
_MAX31865_RTD_LSB_REG = const(0x02)
_MAX31865_HIGH_FAULT_THRESHOLD_MSB_REG = const(0x03)
_MAX31865_HIGH_FAULT_THRESHOLD_LSB_REG = const(0x04)
_MAX31865_LOW_FAULT_THRESHOLD_MSB_REG = const(0x05)
_MAX31865_LOW_FAULT_THRESHOLD_LSB_REG = const(0x06)
_MAX31865_FAULT_STATUS_REG = const(0x07)

# hidden constants
_REFERENCE_RESISTOR = const(430.0)
_RTD_0 = const(100) # RTD resistance at 0degC
_RTD_A = const(3.9083e-3)
_RTD_B = (-5.775e-7)


class MAX31865:
    """
    MAX31865 thermocouple amplifier driver for the PT100 (2-wire)

    :param spi: SPI device, maximum baudrate is 5.0 MHz
    :param cs: chip select
    
    usage:
    from machine import Pin, SPI
    from max31865 import MAX31865
    
    spi = SPI(0, baudrate=5000000, sck=2, mosi=3, miso=4)
    cs = Pin(5)
    
    sensor = MAX31865(spi, cs)
    temp = sensor.temperature
    """
    def __init__(self, spi, cs, baudrate=5000000):
        if cs is None:
            raise ValueError("CS parameter must be provided")
        
        # initalize SPI bus and set CS pin high
        self.spi = spi
        cs.init(mode=machine.Pin.OUT, value=1)
        self.cs = cs
        
        self.configure(0x00)
        
    """"
    Configuration Register Definition
    D7: Vbias (1 = ON, 0 = OFF)
    D6: Conversion mode (1 = Auto, 0 = Normally off)
    D5: 1-shot (1 = 1-shot (auto-clear))
    D4: 3-wire (1 = 3-wire RTD, 0 = 2-wire or 4-wire)
    D3-D2: Fault Detection Cycle Control
    D1: Fault Status Clear (1 = Clear (auto-clear))
    D0: 50/60Hz filter select (1 = 50 Hz, 0 = 60 Hz)
    """
    def configure(self, config):
        self.write(_MAX31865_CONFIGURATION_REG, config)
        time.sleep(0.065)

    def read(self, register, number_of_bytes = 1):
        # registers are accessed using the 0Xh addresses for reads
        try:
            self.cs.value(0)
            self.spi.write(bytearray([register & 0x7F]))
            return self.spi.read(number_of_bytes)
        except Exception as e:
            raise OSError(f"MAX31865: SPI Error: {e}")
        finally:
            self.cs.value(1)
    
    def write(self, register, data):
        # registers are accessed using the 8Xh addresses for writes
        try:
            self.cs.value(0)
            self.spi.write(bytearray([(register | 0x80) & 0xFF, data & 0xFF]))
        except Exception as e:
            raise OSError(f"MAX31865: SPI Error: {e}")
        finally:
            self.cs.value(1)
        
    # read the raw value of the thermocouple
    def read_rtd(self):
        self.configure(0xA0)
        rtd = self.read(_MAX31865_RTD_MSB_REG, 2)
        rtd = (rtd[0] << 8) | rtd[1]
        rtd >>= 1
        return rtd
        
    # read the resistance of the PT100 in Ohms
    @property
    def resistance(self):
        resistance = self.read_rtd()
        resistance /= 32768
        resistance *= _REFERENCE_RESISTOR
        return resistance
    
    # read the temperature of the PT100 in degrees (math: https://www.analog.com/media/en/technical-documentation/application-notes/AN709_0.pdf) 
    @property
    def temperature(self):
        raw = self.resistance
        Z1 = -_RTD_A
        Z2 = _RTD_A * _RTD_A - (4 * _RTD_B)
        Z3 = (4 * _RTD_B) / _RTD_0
        Z4 = 2 * _RTD_B
        
        temp = Z2 + (Z3 * raw)
        temp = (math.sqrt(temp) + Z1) / Z4
        
        if temp >= 0:
            return temp
        
        raw /= _RTD_0
        raw *= 100 # normalize to 100 ohms )
        
        rpoly = raw
        temp = -242.02
        temp += 2.2228 * rpoly
        rpoly *= raw  # square
        temp += 2.5859e-3 * rpoly
        rpoly *= raw  # ^3
        temp -= 4.8260e-6 * rpoly
        rpoly *= raw  # ^4
        temp -= 2.8183e-8 * rpoly
        rpoly *= raw  # ^5
        temp += 1.5243e-10 * rpoly
        
        return temp


