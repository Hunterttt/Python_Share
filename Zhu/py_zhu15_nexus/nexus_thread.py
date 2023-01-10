import os,sys
from openpyxl import Workbook
from netmiko import Netmiko
import time
import threading
import queue
import ipaddress
import numpy

os.chdir(sys.path[0]) 

q = queue.Queue()


def Txt_To_List(xfile):
#将文件逐行读取到一个列表
    with open(xfile, "r") as temp_file:
        xlist = [line.strip() for line in temp_file if line.strip()]
    return(xlist)



def Input(ip):

    my_device = {
    "host": ip,
    "username": "admin",
    "password": "Admin@123",
    "device_type": "cisco_ios",
    }
    try:
        net_connect = Netmiko(**my_device)
        result = net_connect.send_config_from_file(config_file='commands.txt')
        net_connect.disconnect()
        return "done"
    except:
        return "something wrong"


def Input_Thread():
#从线程列表中拿ip
    while not q.empty():
        ip = q.get()  
        
        print("Checking %s..." %ip)
        row = [] 
        row.append(ip)
                   
        row.append(Input(ip))

        temp_result_list2d.append(row)


def List2d_To_Dict(xlist2d):
#把列表中的第一个元素作为字典的key，剩下的作为值
    xdict = {}
    for i in range(len(xlist2d)):
        key = xlist2d[i][0]         
        tlist = xlist2d[i]
        tlist.pop(0)    #删掉第一个元素
        value = tlist
        xdict[key] = value
    return(xdict)


def Dict0_To_List(xdict):
#把字典中的key提取出来，放在一个列表里
    xlist = []
    for key in xdict:
        xlist.append(key)
    return(xlist)


def Bubble_Sort_Improve(lst2):    #进阶冒泡排序法，看笔记
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

    temp_result_list2d = []     #全局数组，多线程的结果汇集

    ip_list = Txt_To_List('iplist.txt')


    for i in range(len(ip_list)):
        q.put(ip_list[i])           #把ip地址放入线程队列
    
    THREAD = 5           #线程数
    threads = []

    for i in range(THREAD):       
        thread = threading.Thread(target=Input_Thread)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


    temp_dict = {}
    temp_dict = List2d_To_Dict(temp_result_list2d)
    #sorted_list = sorted(result_list,key=(lambda x:x[0]))
    dict0_list = Dict0_To_List(temp_dict)        #得到IP列表

    sort_dict0_list = Bubble_Sort_Improve(dict0_list)

    #print(sort_dict0_list)


    wb = Workbook()
    ws = wb.active
    title_list = []
    title_list.append('IP')
    title_list.append('Result')


    ws.append(title_list)

    
    sort_dict0_list2d = numpy.array(sort_dict0_list).reshape(-1,1)   #把数据类型转换为数组，再reshape成二维数组

    #print(sort_dict0_list2d)
    for i in range(len(sort_dict0_list)):
            
        row = sort_dict0_list2d[i].tolist()    #把数据类型重新转换为列表
        #print(row)
        
        row.extend(temp_dict[sort_dict0_list[i]])    #把字典里key对应的值重新接上
        #print(row)
        ws.append(row)
    wb.save('Result.xlsx')

