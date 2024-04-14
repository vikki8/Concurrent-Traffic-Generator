# Real-Life-Traffic-Generator

## Project Description
This project focuses on generating real-life network traffic scenarios using labeled network traffic flows dataset obtained from [Kaggle](https://www.kaggle.com/datasets/jsrojas/labeled-network-traffic-flows-114-applications/data). <br>
By leveraging tools like Scapy, iperf, and DITG, this project aims to simulate and analyze network traffic patterns from Docker hosts in the Mininet environment. <br>

To adapt to the Mininet environment, the IP source and destination of the dataset are changed to the 10.0.0.0/24 range (the last octet is unaltered and the rest of the octet is changed to match the 10.0.0.0/24 range). <br>

**Dataset description** <br>
There are 4 datasets supporting from 5 to 20 hosts. <br>
Dataset naming follows as per the number of hosts <br>
**Ex: 5host.csv** (5 hosts IP & MAC) - 10.0.0.1 to 10.0.0.5 | 00:00:00:00:00:01 - 00:00:00:00:00:05

**Traffic Generator description** <br>
popen.py - uses Scapy <br>
popen2.py - uses iperf <br>
popen3.py - uses DITG <br>

## Usage
### Step 1: Build Ubuntu Image with traffic generator
```
cd ubuntu-docker
sudo docker build -t ubuntu .
```

### Step 2: Setup Containernet topology and connect to ONOS
Refer to my other repository [here](https://github.com/vikki8/SDN_clos_topology_generator), to create a containernet CLOS topology with docker hosts and connect it to the ONOS controller.

### Step 3: Install supporting ONOS application
Activate the default reactive forwarding & OpenFlow app to enable Southbound communication from ONOS to OvS. <br>
Use the command `app activate org.onosproject.openflow` `app activate fwd` in ONOS CLI <br>

You may also refer to my other repository [here](https://github.com/vikki8/onos_traffic_reroute_app/tree/main), to implement an optimized traffic forwarding & rerouting application replacing the default reactive forwarding app.

### Step 4: Install Python dependencies
```
pip install pandas paramiko
```

### Step 5: Generate the traffic!
```
cd bot-python
sudo python3 popen.py
```
**Note:** <br>
You may need to edit the Python script to change the dataset which supports different numbers of hosts 

