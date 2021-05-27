import os,socket,sys
from openpyxl import Workbook
from netmiko import Netmiko
import time
import threading
import queue
import ipaddress
import numpy

os.chdir(sys.path[0]) 

ports = input("Enter the ports you want to check, use ',' to separate, then press Enter\nEX '22,23,139'\n: ")
ports_list = [int(n) for n in ports.split(",")]    #逗号隔开变数组

socket.setdefaulttimeout(4)

q = queue.Queue()


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



def Check(tports_list):
#导入要执行的命令行列表
    while not q.empty():
        ip = q.get()  
        
        print("Checking %s..." %ip)
        row = [] 
        row.append(ip)
        for j in range(len(tports_list)):    #同一个循环，会顺序执行，得到第一个的结果后才会执行第二个，不用担心顺序           
            row.append(PortOpen(ip,ports_list[j]))
            #time.sleep(5)
            #print(ip,tports_list[j])
        temp_result_list2d.append(row)


def list2d_to_dict(xlist2d):
#把列表中的第一个元素作为字典的key，剩下的作为值
    xdict = {}
    for i in range(len(xlist2d)):
        key = xlist2d[i][0]         
        tlist = xlist2d[i]
        tlist.pop(0)    #删掉第一个元素
        value = tlist
        xdict[key] = value
    return(xdict)


def dict0_to_list(xdict):
#把字典中的key提取出来，放在一个列表里
    xlist = []
    for key in xdict:
        xlist.append(key)
    return(xlist)


def bubble_sort_improve(lst2):    #进阶冒泡排序法，看笔记
#对key列表进行排序
    lstlen = len(lst2)
    i = 1; times = 0
    while i > 0:
        times += 1
        change = 0
        for j in range(1, lstlen):
            if ipaddress.IPv4Address(lst2[j-1]) > ipaddress.IPv4Address(lst2[j]):   #ipaddress.IPv4Address可以直接将IP地址转换为数值
#使用标记记录本轮排序中是否有数据交换
                change = j
                lst2[j],lst2[j-1] = lst2[j-1],lst2[j]
        #print(('sorted {0}:{1}').format(times, lst2))
#将数据交换标记作为循环条件，决定是否继续进行排序
        i = change
    return(lst2)





if __name__ == '__main__':
    start_time = time.time()

    temp_result_list2d = []     #全局数组，多线程的结果汇集

    ip_list = txt_to_list('iplist.txt')


    for i in range(len(ip_list)):
        q.put(ip_list[i])           #把ip地址放入线程队列
    
    THREAD = 5           #线程数
    threads = []

    for i in range(THREAD):       
        thread = threading.Thread(target=Check,args=(ports_list,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


    temp_dict = {}
    temp_dict = list2d_to_dict(temp_result_list2d)
    #sorted_list = sorted(result_list,key=(lambda x:x[0]))
    dict0_list = dict0_to_list(temp_dict)        #得到IP列表

    sort_dict0_list = bubble_sort_improve(dict0_list)

    #print(sort_dict0_list)


    wb = Workbook()
    ws = wb.active
    title_list = []
    title_list.append('IP')
    for title in ports_list:
        title_list.append(title)

    ws.append(title_list)

    
    sort_dict0_list2d = numpy.array(sort_dict0_list).reshape(-1,1)   #把数据类型转换为数组，再reshape成二维数组

    #print(sort_dict0_list2d)
    for i in range(len(sort_dict0_list)):
            
        row = sort_dict0_list2d[i].tolist()    #把数据类型重新转换为列表
        #print(row)
        
        row.extend(temp_dict[sort_dict0_list[i]])    #把字典里key对应的值重新接上
        #print(row)
        ws.append(row)
    wb.save('Port Check.xlsx')


    print('程序运行耗时：%s' % (time.time() - start_time))