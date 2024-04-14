# Real-Life-Traffic-Generator

## Project Description
This project focuses on generating real-life network traffic scenarios using labeled network traffic flows dataset obtained from [Kaggle](https://www.kaggle.com/datasets/jsrojas/labeled-network-traffic-flows-114-applications/data). <br>
By leveraging tools like Scapy, iperf, and DITG, this project aims to simulate and analyze network traffic patterns from Docker hosts in the Mininet environment. <br>
The dataset is modified such as IP source and destination to adapt to the Mininet environment, ensuring compatibility with the network emulation framework.

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

### Step 4: Generate the traffic!


