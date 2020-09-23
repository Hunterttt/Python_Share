from netmiko import Netmiko

my_device = {
    "host": "192.168.32.10",
    "username": "man",
    "password": "cisco",
    "device_type": "cisco_ios",
}

net_connect = Netmiko(**my_device)

output = net_connect.send_command("show ip int brief")
print(output)

net_connect.disconnect()