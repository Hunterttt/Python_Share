
import os,sys
from netmiko import Netmiko

os.chdir(sys.path[0]) 

ip1 = "10.19.254.23"

my_device = {
"host": ip1,
"username": "admin",
"password": "Admin123",
"device_type": "cisco_ios",
}
try:
    net_connect = Netmiko(**my_device)
    d_asa = net_connect.send_command('connect module 1 console')
    net_connect.disconnect()

    print(d_asa)

except:
    print("Cannot login the device.")