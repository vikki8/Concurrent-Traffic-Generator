FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y openvswitch-switch
RUN apt-get -y install net-tools
RUN apt-get -y install iputils-ping
RUN apt-get -y install isc-dhcp-client
RUN apt-get install iperf
RUN apt-get -y install d-itg
RUN apt-get -y install python3-pip
RUN apt-get -y install tcpreplay
RUN pip install scapy

# change password root
RUN echo "root:root"|chpasswd

# SSH
RUN apt-get -y install openssh-server
RUN apt-get -y install nano

# authorize SSH connection with root account
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

WORKDIR /bot
COPY /bot ./
