import time, machine, os

def mount_sd(mount_dir):
    """
    SD Mounting code for Wemos Lolin D32 PRO
    :param mount_dir: path string, e.g.: /sd
    :return:
    """
    print('setting SDCard pins')
    try:
        sd = machine.SDCard(slot=2, sck=18, mosi=23, miso=19, cs=4)
    except OSError as e:
        if e.errno == -259:
            print('error: -259, SPI already in use')  # Happens sometimes on soft reboot
            print('resetting')
            machine.reset()
    print('Mounting sd...')
    os.mount(sd, mount_dir, readonly=False)
    print('sd mounted')
    return sd