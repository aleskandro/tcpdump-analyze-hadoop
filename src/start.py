#!/usr/bin/python

import argparse
import os
import mapper
logFile=''
actions={'pCounters': '0', 'topTenServers': '0', 'topTenClients': '0', 'topTenClientsByServers': '0', 'timestamps': '0'}

def setEnv():
    for action, enabled in actions.iteritems():
        os.environ[action] = enabled

parser = argparse.ArgumentParser(description='Process tcpdump log files')
parser.add_argument('logFile', nargs=1)
parser.add_argument('-s', '--serversTopTen',     action='append_const', dest='actions', const='topTenServers')
parser.add_argument('-c', '--clientsTopTen',     action='append_const', dest='actions', const='topTenClients')
parser.add_argument('-C', '--clientsTopTenByServers',     action='append_const', dest='actions', const='topTenClientsByServers')
parser.add_argument('-p', '--generalStatistics', action='append_const', dest='actions', const='pCounters')
parser.add_argument('-t', '--timestamps', action='append_const', dest='actions', const='timestamps')

parser.add_argument('-H', '--hadoop', type=str, help='Enable hadoop mapreduce (take the hadoop streaming .jar path as argument)')

if __name__ == '__main__':
    args = parser.parse_args()
    logFile=args.logFile[0]
    if not args.actions:
        for action in actions:
            actions[action] = '1'
    else:
        for arg in args.actions:
            actions[arg] = '1'

    if args.hadoop:
        os.system('hdfs dfs -rm -r -f %s' % (logFile))
        os.system('hdfs dfs -copyFromLocal %s %s' % (logFile, logFile))
        os.system('hdfs dfs -rm -r -f log.log')
        theCommand = 'hadoop jar %s \
            -file ./mapper.py    -mapper ./mapper.py \
            -file ./reducer.py   -reducer ./reducer.py \
            -input %s -output log.log ' % (args.hadoop, logFile)
        for action, enabled in actions.iteritems():
            theCommand += '-cmdenv %s=%s ' % (action, enabled)
        os.system(theCommand)
        os.system('hdfs dfs -cat log.log/part* | less')
    else:
        setEnv()
        os.system('cat %s | ./mapper.py | sort | ./reducer.py | less' % logFile)

