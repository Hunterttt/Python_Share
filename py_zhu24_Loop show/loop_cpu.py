import time
import os,sys
from netmiko import Netmiko

os.chdir(sys.path[0]) 

ip1 = "192.168.32.103"

def show_firepower(x_ip):
    d_show_list = []

    my_device = {
    "host": x_ip,
    "username": "admin",
    "password": "Admin@123",
    "device_type": "cisco_ios",
    }
    try:
        net_connect = Netmiko(**my_device)

        d_asa = net_connect.send_command('show inventory')

        if 'TM00030000E' in d_asa:
            show_1 = net_connect.send_command('show processes cpu')
            show_2 = net_connect.send_command('show ip int bri')
            net_connect.disconnect()

            d_show_list.append('****************************\nshow processes cpu\n****************************')
            d_show_list.append(show_1)
            d_show_list.append('****************************\nshow ip int bri\n****************************')
            d_show_list.append(show_2)
            d_show_list.append('\n\n\n\n')

            return d_show_list

        else:
            print("Something is wrong.")

    except:
        print("Cannot login the device.")







def add_res_to_txt(x_show_list):
    d_file = open('res.txt','a')
    d_file.write('\n'.join(x_show_list))
    d_file.close()



if __name__ == '__main__':

    t_file = open('res.txt','w')
    t_file.close()

    i = 1


    while 1:
        t_res_list = show_firepower(ip1)
        
        count_list = []
        count_list.append('@@@This is the '+str(i)+' time check.@@@\n')
        res_list = count_list + t_res_list
        time.sleep(5)
        add_res_to_txt(res_list)

        print('Finished the '+str(i)+' time check. If you want to stop. Please press Ctrl+C.')

        i += 1


