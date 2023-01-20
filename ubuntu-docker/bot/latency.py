import statistics
import os
import subprocess
import argparse
from scapy.all import *
from scapy.layers.inet import IP, ICMP, Ether

"""
if os.geteuid() > 0:
    raise OSError("This script must run as root")

ping_rtt_list = list()


def ping_addr(count=10):
    packet = Ether(src="00:00:00:00:00:01", dst="00:00:00:00:00:02") / IP(src="10.0.0.1", dst="10.0.0.2") / ICMP()
    t = 0.0
    for x in range(count):
        x += 1  # Start with x = 1 (not zero)
        ans, unans = srp(packet, iface="s1-eth1", filter='icmp', verbose=0)
        rx = ans[0][1]
        tx = ans[0][0]
        delta = rx.time - tx.sent_time
        print("ping #{0} rtt: {1} second".format(x, round(abs(delta), 6)))
        ping_rtt_list.append(round(delta, 6))
    return ping_rtt_list


if __name__ == "__main__":
    ping_rtt_list = ping_addr()
    rtt_avg = round(statistics.mean(ping_rtt_list), 6)
    print("Avg ping rtt (seconds):", rtt_avg)
"""


# sudo python3 latency.py -s 10.0.0.1 -d 10.0.0.2 -smac 00:00:00:00:00:01 -dmac 00:00:00:00:00:02 -c 5 -i h1-eth0
def main():
    parser = argparse.ArgumentParser(description="Real Traffic Accuracy Verification Bot using Latency")
    parser.add_argument('-s', '--srcip', type=str, metavar='', required=True,
                        help="Specify source IP")
    parser.add_argument('-d', '--dstip', type=str, metavar='', required=True,
                        help="Specify destination IP")
    parser.add_argument('-smac', '--srcmac', type=str, metavar='', required=True,
                        help="Specify source MAC address")
    parser.add_argument('-dmac', '--dstmac', type=str, metavar='', required=True,
                        help="Specify destination MAC address")
    parser.add_argument('-c', '--count', type=int, metavar='', required=False, default=1,
                        help="Specify ping count")
    parser.add_argument('-i', '--interface', type=str, metavar='', required=False, default="s1-eth1",
                        help="Specify interface")
    args = parser.parse_args()

    pkt = []
    botping = []
    for i in range(args.count):
        a = Ether(src=args.srcmac, dst=args.dstmac) / IP(src=args.srcip, dst=args.dstip) / ICMP()
        pkt.append(a)

    ans, unans = srp(pkt, iface=args.interface, filter="host {0}".format("10.0.0.2"), inter=0, timeout=1, verbose=0)

    # print("scapy version: {}".format(conf.version))

    for pkt in ans:
        sent = pkt[0]
        received = pkt[1]
        res = (received.time - sent.sent_time)
        res_update = "{:.6f}".format(abs(res))
        botping.append(float(res_update))
    # print(botping)

    count = args.count
    ping = []
    p1 = subprocess.run(['ping', '-c', str(count), args.dstip], capture_output=True)
    split = str(p1.stdout).split('\\n')
    for i in range(1, 1 + int(count)):
        time = split[i].split(" ")
        latency = time[6].replace("time=", "")
        ping.append(float(latency))
    # print(ping)

    for j in range(len(ping)):
        print("Bot Traffic Latency (using Scapy): " + str(botping[j]))
        print("Real Traffic Latency (using Ping): " + str(ping[j]))
        print("Accuracy: " + str(botping[j] / ping[j] * 100))


if __name__ == '__main__':
    main()
