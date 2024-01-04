import machine
import time
from max31865 import MAX31865

# Configure SPI
spi = machine.SPI(0, baudrate=5000000, phase=1, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4))
cs = machine.Pin(machine.Pin.board.GP5) # no communication (active LOW)

sensor = MAX31865(spi, cs)

while True:
    print("Temperature: {:.2f} °C".format(sensor.temperature))
    time.sleep(1)
