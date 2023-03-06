import subprocess
import easysnmp
import re


def get_ipv4_addresses(hostname, community):
    session = easysnmp.Session(hostname=hostname, community=community, version=2)

    results = session.walk(['ipAdEntIfIndex', 'ipAdEntAddr'])

    ip_dict = {}
    for result in results:
        if result.oid == 'ipAdEntIfIndex':
            current_index = result.value
        elif result.oid == 'ipAdEntAddr':
            ip_dict[current_index] = result.value
    return ip_dict


def get_ipv6_value(hostname, community):
    command = ["snmpwalk", "-v", "2c", "-c", community, hostname, ".1.3.6.1.2.1.4.34.1.3.2"]
    output = subprocess.check_output(command).decode("utf-8")
    # Extract the IPv6 value from the output
    index = output.split(" ")[-1].strip('"')
    regex = r'ipv6\."([^"]+)"'
    match = re.search(regex, output)
    if match:
        ipv6 = match.group(1)
        return ipv6, index


def get_interface_name(index):
    if index == '4':
        return 'FastEthernet 1/1'
    elif index == '3':
        return 'FastEthernet 1/0'
    elif index == '2':
        return 'FastEthernet 0/1'
    elif index == '1':
        return 'FastEthernet 0/0'
    else:
        return 'Unknown'


ip_addresses = ['198.51.101.22', '198.51.101.33', '198.51.102.1', '198.51.100.1', '198.51.102.1']
community = 'netman'

for ip_address in ip_addresses:
    ipv6_address, index = get_ipv6_value(ip_address, community)
    if ipv6_address and index:
        interface_name = get_interface_name(index)
        print("{}: {}".format(interface_name, ipv6_address))
    else:
        print("Failed to get IPv6 address for {}".format(ip_address))

    ipv4_addresses = get_ipv4_addresses(ip_address, community)
    print("IPv4 Addresses for {}: ".format(ip_address))
    for index, ip in ipv4_addresses.items():
        interface_name = get_interface_name(index)
        print("{}: {}".format(interface_name, ip))
