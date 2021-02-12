# pi-top[4] GPS via Serial
Displaying GPS data from an Adafruit Ultimate GPS Breakout V3 to the pi-top[4]

![pi-top GPS Miniscreen](https://forum.pi-top.com/uploads/default/original/1X/1a10807314cee3aa8ac309f5e55d9750830013ed.jpeg "pi-top GPS Miniscreen")

## Hardware Requirements
* [pi-top[4]](https://shop.pi-top.com/collections/pi-top-4/products/pi-top-4-complete) or [pi-top[4] DIY kit](https://shop.pi-top.com/collections/pi-top-4/products/pi-top-4-diy-edition)
* (Raspberry Pi 4}[https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-4-model-b] (only if using DIY kit)
* (Adafruit Ultimate GPS Breakout v3)[https://thepihut.com/products/adafruit-ultimate-gps-breakout-66-channel-w-10-hz-updates]
* Some jumper wires

Please note that this will worth with other GPS devices, however, not all NMEA sentences may be available. by default the Adafruit Ultimate GPS Breakout v3 does not show GPZDA by default, which is dame and date sentence but can be enabled with doing a serial write

## Software 
* `pip3 install pySerial `
*  `sudo apt install libatlas-base-dev -y` (if using virtualenv)

