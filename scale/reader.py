import os, time
import usb.core
import usb.util
from sys import exit

def __connect(idVendor, idProduct):
    # find the USB device
    dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
    if dev is None:
        return dev
    else:
        devmanufacturer = usb.util.get_string(dev, 256, 1)
        devname = usb.util.get_string(dev, 256, 2)

        interface = 0
        if dev.is_kernel_driver_active(interface) is True:
            dev.detach_kernel_driver(interface)
            dev.set_configuration()
            usb.util.claim_interface(dev, interface)
    return dev

def __disconnect(dev):
    interface = 0
    usb.util.release_interface(dev, interface)
          
def __analyzeData(data):
    DATA_MODE_GRAMS = 2
    DATA_MODE_OUNCES = 11
    grams = 0
    
    if data != None:
        raw_weight = data[4] + data[5] * 256

    if raw_weight > 0:
        if data[2] == DATA_MODE_OUNCES:
            ounces = raw_weight * 0.1
            grams = round(ounces * 28.3495, 2)
        elif data[2] == DATA_MODE_GRAMS:
            grams = raw_weight

        return grams

    return 0


def __grabData(dev):
    # first endpoint
    endpoint = dev[0][(0,0)][0]

    # read a data packet
    attempts = 10
    data = None
    while data is None and attempts > 0:
        try:
            data = dev.read(endpoint.bEndpointAddress,
                               endpoint.wMaxPacketSize)
            
        except usb.core.USBError as e:
            data = None
            if e.args == ('Operation timed out',):
                attempts -= 1
                # print "timed out... trying again"
                continue

    return data


def establish(idVendor, idProduct):
    def read():
        dev = __connect(idVendor, idProduct)
        if dev is not None:
            data = __analyzeData(__grabData(dev))
            __disconnect(dev)
            return data
    return read