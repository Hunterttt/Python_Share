import os,socket,sys
from pathlib import Path 
from openpyxl import Workbook
from netmiko import Netmiko

os.chdir(sys.path[0]) 

ports = input("Enter the ports you want to check, use ',' to separate, then press Enter\nEX '22,23,139'\n: ")
ports_list = [int(n) for n in ports.split(",")]    #逗号隔开变数组

socket.setdefaulttimeout(4)


def txt_to_list(xfile):
#将文件逐行读取到一个列表
    with open(xfile, "r") as temp_file:
        xlist = [line.strip() for line in temp_file if line.strip()]
    return(xlist)

def PortOpen(ip,port):
#socket try connect
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)     #创建socker实例

    try:
        s.connect((ip,port))
        """
        If the connection is interrupted by a signal, the method waits until the connection completes, 
        if the signal handler doesn’t raise an exception and the socket is blocking or has a timeout, raise a socket.timeout on timeout. 
        For non-blocking sockets, the method raises an InterruptedError exception if the connection is interrupted by a signal (or the exception raised by the signal handler).
        """
        s.shutdown(2)

        if port == 22:
            my_device = {
            "host": ip,
            "username": "admin",
            "password": "admin@123",
            "device_type": "cisco_ios",
            }

            try:
                net_connect = Netmiko(**my_device)
                net_connect.disconnect()

                return "access"

            except:
                return "cannot access"


        #return "Open"

    except socket.timeout:
        return "CLOSE/TIMEOUT"
        			
    except:
        return "CLOSE"





def list2d_to_xlsx(xlist2d,xlist):
#写入Excel文件
    wb = Workbook()
    ws = wb.active
    title_list = []
    title_list.append('IP')
    for title in xlist:
        title_list.append(title)
    ws.append(title_list)
    for i in range(len(xlist2d)):
        ws.append(xlist2d[i])
    wb.save('Port Check.xlsx')


def main():
    result_list = []
    ip_list = []
    ip_list = txt_to_list('iplist.txt')
    for i in range(len(ip_list)):
        print("Checking %s..." %ip_list[i])
        row = [] 
        row.append(ip_list[i]) 
        for j in range(len(ports_list)):          
            row.append(PortOpen(ip_list[i],ports_list[j]))

        result_list.append(row)



    #print(result_list)
    list2d_to_xlsx(result_list,ports_list)

if __name__ == '__main__':
    main()