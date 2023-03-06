# import easysnmp
#
# session = easysnmp.Session(
#     hostname="198.51.101.22",
#     community="netman",
#     version=2
# )
#
# oid = ".1.3.6.1.2.1.4.34.1.3.2"
#
# result = session.get(oid)
# print(result)
# for item in result:
#     print(item.oid, "=", item.value)
import subprocess
import re


import subprocess

def get_ipv6_value():
    command = ["snmpwalk", "-v", "2c", "-c", "netman", "198.51.101.22", ".1.3.6.1.2.1.4.34.1.3.2"]
    output = subprocess.check_output(command).decode("utf-8")
    # Extract the IPv6 value from the output
    index = output.split(" ")[-1].strip('"')
    regex = r'ipv6\."([^"]+)"'
    match = re.search(regex, output)
    if match:
        ipv6 = match.group(1)
        return ipv6, index
l,n=get_ipv6_value()


# import re
#
# def extract_ipv6(line):
#     regex = r'ipv6\."([^"]+)"'
#     match = re.search(regex, line)
#     if match:
#         ipv6 = match.group(1)
#         print("ipv6=" + ipv6)
#
# line = 'IP-MIB::ipAddressIfIndex.ipv6."11:11:11:11:00:00:00:00:c8:02:49:ff:fe:e5:00:08" = INTEGER: 1'
# extract_ipv6(line)