import os,sys
from openpyxl import Workbook
from netmiko import Netmiko
import threading
import queue
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
        net_connect = Netmiko(**my_device)     #Netmiko是一个类，net_connect是一个实例，my_device是产生实例时需要的数据属性
        result = net_connect.send_config_from_file(config_file='commands.txt')    #通过实例去调用类函数，实例本身并没有函数属性，是通过风湿理论去调用类里的函数
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

    #print(temp_dict)
    #sorted_list = sorted(result_list,key=(lambda x:x[0]))
    
    wb = Workbook()
    ws = wb.active
    title_list = []
    title_list.append('IP')
    title_list.append('Result')
    ws.append(title_list)

    ip_list2d = numpy.array(ip_list).reshape(-1,1)    #把数据类型转换为数组，再reshape成二维数组，直接把原来读取的IP列表进行转换
    for i in range(len(ip_list)):
        row = ip_list2d[i].tolist()    #把数据类型重新转换为列表
        row.extend(temp_dict[ip_list[i]])    #把字典里key对应的值重新接上
        #print(row)
        ws.append(row)
    wb.save('Result.xlsx')


