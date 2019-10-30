#!/usr/bin/env python

import ZeroSeg.led as led
import time
from datetime import datetime

# constants
base = 100 # number of frames per second
nrefresh = 0.4 # refresh n times per frame
utcplus = +0 # timezone/bst adjustment
# make forwards compatible with Python 3
try:
    # Python 2
    xrange
except NameError:
    # Python 3, xrange is now named range
    xrange = range

def clock(device, deviceId, seconds):
    for _ in xrange(seconds):
        now = datetime.now()
        hour = (now.hour + 1) % 24
        minute = now.minute
        second = now.second
        micro = now.microsecond
        frame = int((micro - second) * base / 1000000)
        seq = [
               [int(hour / 10),0], [hour % 10, 1],
               [int(minute / 10),0], [minute % 10, 1],
               [int(second / 10),0], [second % 10, 1],
               [int(frame / 10),0], [frame % 10, 0]
              ]
        # layout right-to-left
        for pos in xrange(0, len(seq)):
            device.letter(deviceId, 8 - pos, seq[pos][0], seq[pos][1])
        time.sleep(1/(nrefresh * base))

device = led.sevensegment()
while True:
    clock(device, 0, seconds=10)
