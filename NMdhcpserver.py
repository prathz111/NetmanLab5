import json
import string
from NMtcpdump import *
from netmiko import ConnectHandler

def run_NMdhcpserver():
    # Define the device to connect to using netmiko
    r4_device = {
        'device_type': 'cisco_ios',
        'ip': '198.51.100.1',
        'username': 'prathz',
        'password': 'prathz',
        "secret": "netman",
    }

    def mac_to_clent_id(mac):

        # Removing colons from MAC address
        mac_without_colons = mac.replace(":", "")
        print(mac_without_colons)

        # Adding prefix "01" to the MAC address
        mac_with_prefix = "01" + mac_without_colons

        # Separating the MAC address into 4-digit chunks with dots
        client_id = ".".join([mac_with_prefix[i:i + 4] for i in range(0, len(mac_with_prefix), 4)])

        print(client_id)
        return mac_without_colons, client_id
        # Adding prefix "01" to MAC address and inserting dots after every 4 characters

        # print(client_id)
    # Establish SSH connection to the device
    with ConnectHandler(**r4_device) as net_connect:
        # Send the "show cdp neighbors detail" command and capture the output
        output = net_connect.send_command("show cdp neighbors detail")

        # Initialize an empty dictionary to store neighbor data for R5
        neighbor_data = {}

        # Parse the output to extract relevant data for R5
        for line in output.splitlines():
            if "Device ID: " in line and "R5" in line:
                neighbor_data["R5"] = {"device_id": line.split(": ")[-1]}
            elif "IP address: " in line and "R5" in neighbor_data:
                neighbor_data["R5"]["ip_address"] = line.split(": ")[-1]
            elif "Platform: " in line and "R5" in neighbor_data:
                neighbor_data["R5"]["platform"] = line.split(": ")[-1]
            elif "Interface: " in line and "R5" in neighbor_data:
                neighbor_data["R5"]["interface"] = line.split(": ")[-1]
            elif "IPv6 address: " in line and "R5" in neighbor_data:
                ipv6_address = line.split(": ")[-1]
                if "global unicast" in line:
                    neighbor_data["R5"]["ipv6_global_unicast"] = ipv6_address
                elif "link-local" in line:
                    neighbor_data["R5"]["ipv6_link_local"] = ipv6_address

        # Store the neighbor data in a JSON file
        with open("r5_neighbor_data.json", "w") as f:
            json.dump(neighbor_data, f, indent=4)

        print("Neighbor data for R5 has been saved in 'r5_neighbor_data.json' file.")

        # Read the neighbor data from the JSON file
        with open("r5_neighbor_data.json", "r") as f:
            neighbor_data = json.load(f)

        # Extract the IPv6 address for R5
        r5_ipv6_add = neighbor_data["R5"]["ipv6_global_unicast"]
        r5_ipv6_address = r5_ipv6_add.replace("(global unicast)", "").strip()
        print(r5_ipv6_address)
        # Define the device to connect to using netmiko
        r5_device = {
            'device_type': 'cisco_ios',
            'ip': r5_ipv6_address,
            'username': 'prathz',
            'password': 'prathz',
            "secret": "netman",
        }

        # Establish SSH connection to R4
        r2_mac, r3_mac, r4_mac = get_mac()
        r2_mac_ad,r2_client_id=mac_to_clent_id(r2_mac)
        r3_mac_ad,r3_client_id=mac_to_clent_id(r3_mac)
        r4_mac_ad,r4_client_id=mac_to_clent_id(r4_mac)
        print(r2_mac_ad,r2_client_id)
        print(r3_mac_ad,r3_client_id)
        print(r4_mac_ad,r4_client_id)
        with ConnectHandler(**r4_device) as r4_connect:
            # # Fetch R5's IPv6 address from JSON file
            # with open('r5_neighbor_data.json') as f:
            #     r5_data = json.load(f)
            # r5_ipv6_address = r5_data['R5']['ipv6_addresses']['global_unicast']

            # Use R4 to login to R5
            r5_device['ip'] = r5_ipv6_address
            with ConnectHandler(**r5_device) as r5_connect:
                # Run a show command on R5
                commands=[
                    "ip dhcp pool r2",
                    "host 198.51.101.22 255.255.255.0",
                    "hardware-address {}".format(r2_mac_ad),
                    "client-identifier {}".format(r2_client_id),
                ]
                output = r5_connect.send_config_set(commands)
                print(output)
            with ConnectHandler(**r5_device) as r5_connect:
                # Run a show command on R5
                commands=[
                    "ip dhcp pool r3",
                    "host 198.51.101.33 255.255.255.0",
                    "client-identifier {}".format(r3_client_id),
                ]
                output = r5_connect.send_config_set(commands)
                print(output)

            with ConnectHandler(**r5_device) as r5_connect:
                # Run a show command on R5
                commands = [
                            "ip dhcp pool r4",
                            "network 198.51.101.0 255.255.255.0",
                            "default-router 198.51.101.1"
                            "dns-server 8.8.8.8"
                ]
                output = r5_connect.send_config_set(commands)
                print(output)



def main():
    # compare_files()
    run_NMdhcpserver()

if __name__ == "__main__":
    main()
