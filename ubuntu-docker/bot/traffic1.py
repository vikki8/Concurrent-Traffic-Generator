import argparse
import pathlib
from scapy.all import *
from scapy.layers.inet import IP, ICMP, Ether, TCP, UDP


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
    parser.add_argument('-p', '--protocol', type=int, required=True,
                        help="Specify the protocol")
    parser.add_argument('-c', '--count', type=int, metavar='', required=False, default=1,
                        help="Specify ping count")
    parser.add_argument('-if', '--interface', type=str, metavar='', required=False, default="h1-eth0",
                        help="Specify interface")
    parser.add_argument('-py', '--payload', type=str, metavar='', required=False, default="XXX",
                        help="Payload of the Packet (NOT MORE THAN 1300 bytes)")
    parser.add_argument('-pps', '--packetpsec', type=int, required=False, default=50,
                        help="Specify packets per second")
    parser.add_argument('-mbits', '--mbitspsec', type=float, required=False, default=0.5,
                        help="Specify MBits per second")

    args = parser.parse_args()

    protocol = None
    protocolName = ""

    # with args.payload.open('r') as f:
    #    payload = f.read()

    if args.protocol == 1:
        protocol = ICMP()
        protocolName = "ICMP"
    if args.protocol == 6:
        protocol = TCP()
        protocolName = "TCP"
    if args.protocol == 17:
        protocol = UDP()
        protocolName = "UDP"

    sendpfast(Ether(src=args.srcmac, dst=args.dstmac) / IP(src=args.srcip, dst=args.dstip) / protocol / args.payload,
          loop=args.count, iface=args.interface, pps=args.packetpsec, mbps=args.mbitspsec, parse_results=1)

    print(f"\n{protocolName} Packet from {args.srcmac} {args.srcip} to {args.dstmac} {args.dstip}\n")
    print(f"{args.packetpsec} pps {args.mbitspsec} MBits")
    print("The size of the payload is: " + str(len(args.payload.encode('utf-8'))) + " bytes")


if __name__ == '__main__':
    main()
