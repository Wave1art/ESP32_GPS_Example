# Process for upgrading ESP 32 to latest version

Download latest firmware for ESP32 board from micropython.org. In this case the latest version is here:
https://micropython.org/download/esp32/

## 2. Find the port
In terminal run ```ls /dev/tty* ``` the port is the one which appears when you plug in the usb device

## 3. Flash the firmware
Since the ESP32 board from WEMOS automatically 

Run the command: ```esptool.py --chip esp32 --port /dev/tty.usbserial-1460 --baud 460800 write_flash -z 0x1000 esp32-20220618-v1.19.1.bin```

