FROM sequenceiq/hadoop-docker:2.7.0
RUN yum -y install python-argparse
RUN mkdir /code
ENV PATH="/usr/local/hadoop/bin:${PATH}"

CMD [ "/etc/bootstrap.sh", "-d" ]
