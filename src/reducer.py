#!/usr/bin/python

import sys
import os
import threading


# Transform the environment variable key to a bool (false by default)
def _envToBool(key):
    if os.environ.has_key(key):
        return os.environ[key] == '1'
    return False

# Return a string to be printed, the same is saved, if it is referenced in a string array (rets), to provide a better way when used in threading
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

# Return a string to be printed, the same is saved, if it is referenced in a string array (rets), to provide a better way when used in threading
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
    # get environment to set what stats to produce

    eTopTenClients          = _envToBool('topTenClients')
    ePCounters              = _envToBool('pCounters')
    eTopTenServers          = _envToBool('topTenServers')
    eTopTenClientsByServers = _envToBool('topTenClientsByServers')

    currentKey = None
    key = None

    # small/large packets stats variables
    totalPackets = 0
    largePackets = 0
    pLargePackets= 0

    # Dicts for the others stats
    topTenClients = {}
    topTenServers = {}
    topTenClientsByServers = {}

    # 5-minutes interval packets variables
    timestamps = {}

    # threading helper variables
    rets = []
    threads = []

    for line in sys.stdin:
        line = line.strip()
        key, value = line.split('\t', 1)
        if key == 'packet':
            # Default packet manipulation
            try:
                src, dst, length = value.split(' ')
                length = int(length)
            except ValueError:
                continue

            # Make the stats
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

        # 5-minutes  interval stats
        if key == 'timestamp':
            try:
                ts, pc = value.split(' ')
                pc = int(pc)
            except ValueError:
                continue
            addValueHelper(ts, pc, timestamps)

    # Final printing
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
