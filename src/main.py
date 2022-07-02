# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import time, os
from machine import Pin, UART

from utils.timeutils import strftime
from utils import logger
import mount_sd

# Start the buffer logger to capture initial logs
debug_logger = logger.DataLogger()
dlog = debug_logger.log



def initialisation():
    """ This module sets up the basic configuration """

    dlog('Starting Up. RTC not yet set, any log timestamps will be approximate.')

    dlog('Mounting SD Card.')
    sd = mount_sd.mount_sd('/sd')

    # Set up the file logger and then change the logger to use the file logger
    # this will also write previous log messages to the file
    dlog('Starting up file based logging backend')
    dlog_file = logger.LogBackendFile('/sd/debug', 'log', over_write=False)

    dlog('Swapping logging backend to file based logger')
    debug_logger.change_logger_backend(new_logger_backend= dlog_file, change_timestamp= 709943539, change_timestamp_key='datetime')



def main():

    initialisation()
    led = Pin(5, Pin.OUT)
    led.off()
    time.sleep(0.1)
    led.on()

    dlog('Booted Successfully and initialisation complete...')
    print('\n\n booted.........')

    # Now initialise the GPS
    dlog('Starting initialisation of the GPS. Setting UART2 to custom values to avoid conflicts')
    gpsModule = UART(2, baudrate = 9600, tx=32, rx=33)
    debug_logger.log_data(gpsModule)



    while True:

        dlog("Reading GPS line")

        gpsmsg = gpsModule.readline()
        debug_logger.log_data(gpsmsg)
        print(gpsmsg)

        # gpsModule.readline()
        # buff = str(gpsModule.readline())
        # dlog(buff)
        # print( buff )

        led.off()
        time.sleep(0.1)
        led.on()
        time.sleep(0.5)



    os.umount('/sd')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


