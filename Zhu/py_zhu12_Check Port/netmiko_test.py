from os import close
from netmiko import Netmiko


my_device = {
"host": "172.20.39.133",
"username": "admin",
"password": "admin@123",
"device_type": "cisco_ios",
}


try:
    net_connect = Netmiko(**my_device)
    print(type(net_connect))
    net_connect.disconnect()

    print("Open")

except:
    print("close")