import os,sys
from netmiko import Netmiko

os.chdir(sys.path[0]) 

ip1 = "192.168.32.103"
#ip2 = ""

def show_arp(x_ip):

    my_device = {
    "host": x_ip,
    "username": "admin",
    "password": "Admin@123",
    "device_type": "cisco_ios",
    }
    try:
        net_connect = Netmiko(**my_device)
        arp_res = net_connect.send_command('show ip arp')
        net_connect.disconnect()

        return arp_res       #return一定要写在最后
            
    except:
        print("Something wrong")


def count_arp(x_show_arp,x_ip):

    t_list = x_show_arp.splitlines()
    #print(t_list)
    inc = 0      #不能有逗号，会被认为是另一种数据类型
    unk = 0
    for i in range(len(t_list)):        
        if "Adjacencies" in t_list[i]:
            inc += 1
        elif "Ethernet2/1" in t_list[i]:
            unk += 1
        else:
            pass
    print("INCOMPLETE in %s: %d, UNKNOWN in %s: %d" %(x_ip,inc,x_ip,unk))



if __name__ == '__main__':
    #inc1,unk1 = count_arp(show_arp(ip1))
    count_arp(show_arp(ip1),ip1) 
    


