import os,sys
from openpyxl import Workbook
from netmiko import Netmiko,ConnectHandler
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

    trow = []
    try:
        net_connect = ConnectHandler(**my_device)

        original1 = net_connect.send_command('show inven')
        tlist1 = original1.split("\n")
        tlist2 = list(filter(lambda x:len(x)>1,tlist1))
        tlist3 = tlist2[1].split(' ')
        pid_sn = list(filter(lambda x:len(x)>4,tlist3))
        #print(pid_sn) 
    
        original2 = net_connect.send_command('show system uptime | in "System uptime"') 
        tlist5 = original2.split('     ')
        tlist6 = list(filter(lambda x:len(x)>1,tlist5))
        #print(tlist6[1].strip())
        uptime = tlist6[1].strip()
    
        original3 = net_connect.send_command('show version | in "system:    version"') 
        tlist7 = original3.split(':')
        #print(tlist7[1].strip())
        verison = tlist7[1].strip()
    
        original4 = net_connect.send_command('show hostname') 
        #print(original4.strip())
        hostname = original4.strip()
    
        original5 = net_connect.send_command('show processes cpu | in util') 
        #print(original5.strip())
        cpu = original5.strip()
    
        original6 = net_connect.send_command('show environment | in N7K-F248XP-25') 
        #print(original6.strip())
        power = original6.strip()
        #power = "rwerwe\nrwerrw"


        trow.append(ip)
        trow.append(hostname)
        trow.extend(pid_sn)
        trow.append(verison)
        trow.append(uptime)
        trow.append(cpu)
        trow.append(power)



        net_connect.disconnect()

        #print(trow)


        return trow
    except:
        return [ip,"something wrong"]




def Input_Thread():
#从线程列表中拿ip
    while not q.empty():
        ip = q.get()  
        
        print("Checking %s..." %ip)

        '''
        row = [] 
        row.append(ip)
                   
        row.append(Input(ip))
        '''

        temp_result_list2d.append(Input(ip))


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

    #print(temp_result_list2d)
    temp_dict = {}
    temp_dict = List2d_To_Dict(temp_result_list2d)

    #print(temp_dict)
    #sorted_list = sorted(result_list,key=(lambda x:x[0]))     #从小到大排序
  
    wb = Workbook()
    ws = wb.active
    title_list = []
    title_list.extend(['IP','HOSTNAME','PID','SN','VERSION','UPTIME','CPU','POWER'])

    ws.append(title_list)

    ip_list2d = numpy.array(ip_list).reshape(-1,1)    #把数据类型转换为数组，再reshape成二维数组，直接把原来读取的IP列表进行转换
    for i in range(len(ip_list)):
        row = ip_list2d[i].tolist()    #把数据类型重新转换为列表
        row.extend(temp_dict[ip_list[i]])    #把字典里key对应的值重新接上
        #print(row)
        ws.append(row)
    wb.save('Inspection Result.xlsx')



