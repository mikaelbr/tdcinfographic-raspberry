#!/usr/bin/python
#-*- coding: UTF-8 -*-
import sys
from scale import reader, reader_stub
from socketIO_client import SocketIO, SocketIOPacketError, SocketIOError
from time import sleep
import os

env = os.getenv('PYTHON_ENV', 'production')

# DYMO M5
VENDOR_ID = 0x0922
PRODUCT_ID = 0x8005

reattempt_in = 10
max_total_attempt_seconds = 60
            
interval_ms = 100

def get_read():
    obj = reader if env is 'production' else reader_stub
    return obj.establish(VENDOR_ID, PRODUCT_ID)

def send():
    global reattempt_in
    read = get_read()
    try:
        print "Trying to connect to ws://%s:%s" % (server, port)
        with SocketIO(server, port) as socketIO:
            reattempt_in = 10
            print "Connected. Starting emitting."
            try:
                while True:
                    grams = read()
                    print "Emitting data (%s grams)" % grams
                    socketIO.emit('weight', {'grams': grams})
                    sleep(float(interval_ms) / 1000)
            except SocketIOPacketError as e:
                resend()
    except SocketIOError as e:
        resend()

def resend():
    global reattempt_in

    if reattempt_in <= max_total_attempt_seconds:
        print "Disconnected or could not connect to the WS. Trying to reconnect in %s seconds" % reattempt_in
        sleep(reattempt_in)
        reattempt_in += 10
        send()
    else:
        print "No more attempts. Please reconnect manually"

if __name__ == "__main__":
    argv = sys.argv
    num_args = len(argv)

    server = 'localhost' if num_args < 2 else argv[1]
    port = 3000 if num_args < 3 else argv[2]
    send()