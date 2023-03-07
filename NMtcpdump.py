from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import Ether
from scapy.all import *

def run_NMtcpdump():
    def ipv62mac(ipv6):
        # remove subnet info if given
        subnetIndex = ipv6.find("/")
        if subnetIndex != -1:
            ipv6 = ipv6[:subnetIndex]

        ipv6Parts = ipv6.split(":")
        macParts = []
        for ipv6Part in ipv6Parts[-4:]:
            while len(ipv6Part) < 4:
                ipv6Part = "0" + ipv6Part
            macParts.append(ipv6Part[:2])
            macParts.append(ipv6Part[-2:])

        # modify parts to match MAC value
        macParts[0] = "%02x" % (int(macParts[0], 16) ^ 2)
        del macParts[4]
        del macParts[3]
        return ":".join(macParts)

    def get_mac():
        # Read the pcap file and store packets in a list
        packets = rdpcap("t1.pcapng")

        # Initialize variables to store MAC addresses
        r2_mac = None
        r3_mac = None
        r4_mac = None

        # Set to store unique source and destination IP address pairs
        unique_pairs = set()

        # Loop through the packets
        for packet in packets:
            # Check if the packet is IPv6 and starts with "1111"
            if IPv6 in packet and packet[IPv6].src.startswith("1111") and packet[IPv6].dst.startswith("1111"):
                # Get the source and destination IP addresses
                src_ip = packet[IPv6].src
                dst_ip = packet[IPv6].dst
                # Check if this pair has already been seen
                if (src_ip, dst_ip) not in unique_pairs:
                    # Add the pair to the set of unique pairs
                    unique_pairs.add((src_ip, dst_ip))
                    # Print the IP addresses and corresponding MAC addresses
                    print("Source IP: {0} MAC Address: {1}".format(src_ip, ipv62mac(src_ip)))
                    print("Destination IP: {0} MAC Address: {1}".format(dst_ip, ipv62mac(dst_ip)))
                    if ipv62mac(src_ip) == "ca:02:49:e5:00:08":
                        r4_mac = ipv62mac(src_ip)
                    elif ipv62mac(dst_ip) == "ca:02:49:e5:00:08":
                        r2_mac = ipv62mac(dst_ip)
                    elif ipv62mac(dst_ip) == "ca:03:47:59:00:08":
                        r3_mac = ipv62mac(dst_ip)
                    else:
                        print("Unknown")

        # Print the MAC addresses for R2, R3, and R4
        print("R2 MAC Address: {0}".format(r2_mac))
        print("R3 MAC Address: {0}".format(r3_mac))
        print("R4 MAC Address: {0}".format(r4_mac))
        return r2_mac, r3_mac, r4_mac
    get_mac()


def main():
    # compare_files()
    run_NMtcpdump()

if __name__ == "__main__":
    main()