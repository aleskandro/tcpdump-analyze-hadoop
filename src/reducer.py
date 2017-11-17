#!/usr/bin/python

import sys
import os
import threading


def _envToBool(key):
    if os.environ.has_key(key):
        return os.environ[key] == '1'
    else:
        return False

def topTenSorted(toSort, message, rets):
    i = 0
    ret = '%s\n' % (message)

    for key, value in sorted(toSort.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        ret += "%s\t%s\n" % (key, value)
        i = i + 1
        if i >= 9:
            break
    if not rets is None:
        rets.append(ret)
    return ret

def printTopTenClientsByServers(dictionary, message, rets):
    ret = message + '\n'
    for key, value in dictionary.iteritems():
        ret += topTenSorted(value, key, None)
    if not rets is None:
        rets.append(ret)
    return ret

def addValueHelper(key, value, dictionary):
    if not dictionary.has_key(key):
        dictionary[key] = value
    else:
        dictionary[key] = dictionary[key] + value

def reduce():
    eTopTenClients          = _envToBool('topTenClients')
    ePCounters              = _envToBool('pCounters')
    eTopTenServers          = _envToBool('topTenServers')
    eTopTenClientsByServers = _envToBool('topTenClientsByServers')
    currentKey = None
    key = None
    totalPackets = 0
    largePackets = 0
    pLargePackets= 0
    topTenClients = {}
    topTenServers = {}
    topTenClientsByServers = {}
    timestamps = {}
    rets = []
    threads = []

    for line in sys.stdin:
        line = line.strip()
        key, value = line.split('\t', 1)
        if key == 'packet':
            try:
                src, dst, length = value.split(' ')
                length = int(length)
            except ValueError:
                continue
            if eTopTenClients:
                addValueHelper(src, length, topTenClients)
            if eTopTenServers:
                addValueHelper(dst, 1, topTenServers)
            if ePCounters:
                totalPackets = totalPackets + 1
                if length > 512:
                    largePackets = largePackets + 1
            if eTopTenClientsByServers:
                if not topTenClientsByServers.has_key(dst):
                    topTenClientsByServers[dst] = {}
                addValueHelper(src, length, topTenClientsByServers[dst])
            continue
        if key == 'timestamp':
            try:
                ts, pc = value.split(' ')
                pc = int(pc)
            except ValueError:
                continue
            addValueHelper(ts, pc, timestamps)

    if ePCounters:
        pLargePackets = float(largePackets) / totalPackets * 100
        print('Total packets: %d - Large packets: %0.2f - Small Packets: %0.2f' % (totalPackets, pLargePackets, 100 - pLargePackets))


    if eTopTenClients:
        threads.append(threading.Thread(target=topTenSorted, args=(topTenClients, 'Top Ten Clients', rets)))

    if eTopTenServers:
        threads.append(threading.Thread(target=topTenSorted, args=(topTenServers, 'Top Ten Servers', rets)))

    if eTopTenClientsByServers:
        threads.append(threading.Thread(target=printTopTenClientsByServers, args=(topTenClientsByServers, 'Top Ten clients by servers', rets)))

    for thread in threads:
        thread.start()

    for key, value in timestamps.iteritems():
        print "%s => %s" % (key, value)

    for thread in threads:
        thread.join()

    print '\n'.join(rets)

if __name__ == '__main__':
    reduce()
