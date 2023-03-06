# import easysnmp
#
# session = easysnmp.Session(hostname='198.51.101.22', community='netman', version=2)
#
# results = session.walk(['ipAdEntIfIndex', 'ipAdEntAddr'])
#
# ip_dict = {}
# for result in results:
#     if result.oid == 'ipAdEntIfIndex':
#         current_index = result.value
#     elif result.oid == 'ipAdEntAddr':
#         ip_dict[current_index] = result.value
#
# for index, ip in ip_dict.items():
#     if index=='4':
#         index='FastEtherent 1/1'
#     elif index == '3':
#         index = 'FastEtherent 1/0'
#     elif index == '2':
#         index = 'FastEtherent 0/1'
#     elif index == '1':
#         index = 'FastEtherent 0/0'
#     print("{}: {}".format(index,ip))
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
    print(ip_dict)
    return ip_dict

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
ipv6_address,index=get_ipv6_value()
if index == '4':
    index = 'FastEthernet 1/1'
elif index == '3':
    index = 'FastEthernet 1/0'
elif index == '2':
    index = 'FastEthernet 0/1'
elif index == '1':
    index = 'FastEthernet 0/0'
print("{}: {}".format(index, ipv6_address))

ipv4_addresses = get_ipv4_addresses('198.51.101.22', 'netman')
print("IPv4 Addresses:")
for index, ip in ipv4_addresses.items():
    if index == '4':
        index = 'FastEthernet 1/1'
    elif index == '3':
        index = 'FastEthernet 1/0'
    elif index == '2':
        index = 'FastEthernet 0/1'
    elif index == '1':
        index = 'FastEthernet 0/0'
    print("{}: {}".format(index, ip))



