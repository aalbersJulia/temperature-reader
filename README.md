<a name="readme-top"></a>

<!-- PROJECT INTRO -->
<br>
<div align="center">
  <a href="https://github.com/aalbersJulia/temperature-reader">
    <img src="img/logo.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">Temperature Reader</h3>
  <p align="center">
    Raspberry Pi Pico MicroPython interface for the MAX31865 thermocouple amplifier <br/>
  </p>
</div>

<!-- GETTING STARTED -->
## Getting Started
To get started with the MAX31865 driver on a MicroPython system, follow these simple steps.

### Installation
1. Download the `max31865.py` file from the [repository](https://github.com/aalbersJulia/temperature-reader).
2. Copy the `max31865.py` file to your MicroPython device. You can use tools like `ampy` or a file transfer method suitable for your device. 

<!-- USAGE EXAMPLES -->
## Usage
1. Connect the MAX31865 thermocouple amplifier to your Raspberry Pi Pico or any other MicroPython-supported board.
2. Include the `max31865.py` module in your MicroPython script together with the `machine` module for configuring the SPI bus and chip select pin:
```python
import machine
from max31865 import MAX31865
```
3. Configure the SPI bus and chip select pin:
```python
# Define SPI bus and chip select pin
spi = machine.SPI(0, baudrate=5000000, phase=1, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4))
cs = machine.Pin(machine.Pin.board.GP5)
```
4. Create an instance of the `MAX31865` class:
```python
sensor = MAX31865(spi, cs)
```
5. The current temperature can by retrieved by accessing the `temperature` attribute of the sensor instance: 
```python
temperature = sensor.temperature
print(f"Current Temperature: {temperature} °C")
```

<!-- LICENSE -->
<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
