## Code challenge: analyzing big tcpdump logs

The code runs as a standalone python script, or with hadoop.

To run the code without hadoop:

```
    $ cd src/
    $ ./start.py </PATH/TO/TCPDUMP.LOG> [-flagsToSelectStatistics]

```

It will take a lot of time for large files

### Hadoop

    To get a faster way to quickly analyze the log it could be used hadoop as a distributed framework to process large data sets.

    The use of libraries as pandas could not permit, alone, to get Gigabytes (or hundred of GB) processed in a distributed way.

    So, considering the manipulation to be done simple (so no needs for pandas) but huge in terms of a huge dataset to analyze, this example was implemented with hadoop and python, using hadoop streaming APIs. Alternatives could be to use pandas, a db as prestoDb and the needed connectors in python to make the import of the data set and the manipulation: this was not considered as fast as hadoop and MapReduce way, in designing and development as first thing.

    The code was tested in a Docker container derived from 'sequenceiq/hadoop-docker' hub.docker.com, using a single node hadoop server.

    To build and run the container (take care of permissions and SELinux):
    ```
        $ docker build -t myhadoop .
        $ docker run -v /ABSPATH/TO/THIS/REPO/src/:/code -it myhadoop /etc/bootstrap.sh -bash
    ```

    In the container, to run the analyzer:
    ```
        # cd /code/
        # ./start.py -H /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.0.jar </PATH/TO/TCPDUMP.LOG> [-flagsToSelectStatistics]
    ```

### Dependencies

    * python-argparse
    * start python packages (threading, sys, os...)
    * linux-coreutils: (cat, less, sort... )
    * [Optional] Hadoop

### Usage

usage: start.py [-h] [-s] [-c] [-C] [-p] [-t] [-H HADOOP] logFile

Process tcpdump log files

positional arguments:
  
  logFile

optional arguments:

  -h, --help            show this help message and exit

  -s, --serversTopTen   Get a top ten of servers ordered by count of received

                        packets

  -c, --clientsTopTen   Get a top ten of clients ordered by sent bytes

  -C, --clientsTopTenByServers

                        Take a top ten of clients sending packets to servers,

                        for each server

  -p, --generalStatistics

                        Counts total packets and large or small packets as

                        percentage (large > 500b)

  -t, --timestamps      Enable stats on number of packets logged in a period

                        of 5 minutes

  -H HADOOP, --hadoop HADOOP

                        Enable hadoop mapreduce (take the hadoop streaming

                        .jar path as argument)

