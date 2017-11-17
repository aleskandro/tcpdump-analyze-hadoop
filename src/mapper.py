#!/usr/bin/python

import sys
import os

def toSecs(timestamp):
    return (int(timestamp[0]) * 3600 + int(timestamp[1]) * 60 + int(timestamp[2]))

def map():
    actualTimestamp = None
    packetsCount    = 0
    eTimestamps     = os.environ['timestamps'] == '1'

    for line in sys.stdin:
        line = line.strip()
        arr = line.split(' ')
        src = ".".join(arr[2].split('.')[0:4])
        dst = ".".join(arr[4].split('.')[0:4])
        pckLength = arr[7]

        if eTimestamps:
            timestamp = arr[0].split('.')[0].split(':')
            if actualTimestamp is None:
                actualTimestamp = timestamp

            if toSecs(timestamp) - toSecs(actualTimestamp) > 300:
                print 'timestamp\t%s %d' % (':'.join(actualTimestamp), packetsCount)
                packetsCount = 0
                actualTimestamp = timestamp
            else:
                packetsCount = packetsCount + 1

        print ('packet\t%s %s %s' % (src, dst, pckLength))

if __name__ == '__main__':
    map()

