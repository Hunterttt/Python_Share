import time
import os,sys
from netmiko import Netmiko

os.chdir(sys.path[0]) 

ip1 = "10.19.254.23"

def show_firepower(x_ip):
    d_show_list = []

    my_device = {
    "host": x_ip,
    "username": "admin",
    "password": "Admin123",
    "device_type": "cisco_ios",
    }
    try:
        net_connect = Netmiko(**my_device)

        d_asa = net_connect.send_command('connect module 1 console')

        if 'XYF-SERVER-4115/pri#' in d_asa:
            show_1 = net_connect.send_command('show clock')
            show_2 = net_connect.send_command('show service-policy')
            show_3 = net_connect.send_command('show asp event dp-cp')
            show_4 = net_connect.send_command('show asp event cp-dp')
            net_connect.disconnect()

            d_show_list.append('****************************\nshow clock\n****************************')
            d_show_list.append(show_1)
            d_show_list.append('****************************\nshow service-policy\n****************************')
            d_show_list.append(show_2)
            d_show_list.append('****************************\nshow asp event dp-cp\n****************************')
            d_show_list.append(show_3)
            d_show_list.append('****************************\nshow asp event cp-dp\n****************************')
            d_show_list.append(show_4)
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


