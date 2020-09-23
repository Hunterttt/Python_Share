import subprocess
import time
from pathlib import Path
import threading
from queue import Queue
import ipaddress


#将文件逐行读取到一个列表
with open('tcping_list.txt','r') as temp_file:
    tlist = temp_file.read().splitlines()
# 将需要 ping 的 ip 加入队列
IP_QUEUE = Queue() 
for index in range(len(tlist)):
    IP_QUEUE.put(tlist[index])


count_True, count_False = 0, 0
ip_False = []
ip_True = []

def tcping():
#导入要执行的命令行列表
    global count_True, count_False
    global ip_False, ip_True
    while not IP_QUEUE.empty():
        ip = IP_QUEUE.get()  
        
        output = subprocess.getoutput(ip)     #逐行执行命令行，并获取执行结果 
        lock.acquire()   #同步锁
        #print(output)          #把执行结果输出在屏幕上,会不按顺序来，无法避免
        if 'out' in output:            #如果输出结果中有（time）out字样，tcping失败
            #print('%s is fail' % ip)
            #ip_False.write(ip+"\n")
            ip_False.append(ip.strip().split(' ')[1])
            count_False += 1
        else:
            #print ('%s is ok' % ip)
            #ip_True.write(ip+"\n")
            ip_True.append(ip.strip().split(' ')[1])
            count_True += 1
        lock.release()   #同步锁


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
    # 定义工作线程
    WORD_THREAD = 10
    
    
    threads = []
    lock = threading.Lock()
    for i in range(WORD_THREAD):
        thread = threading.Thread(target=tcping)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    
    bubble_sort_improve(ip_True)
    bubble_sort_improve(ip_False)

    ping_Folder = str(Path.cwd())   #获取当前脚本所在路径

    with open(ping_Folder + '/ip_True.txt', 'w+') as ip_Truetxt:
        ip_Truetxt.write('\n'.join(ip_True))
        ip_Truetxt.write("\n【ping通的ip数】：%d" % count_True)

    with open(ping_Folder + '/ip_False.txt', 'w+') as ip_Falsetxt:
        ip_Falsetxt.write('\n'.join(ip_False))
        ip_Falsetxt.write("\n【ping不通的ip数】：%d" % count_False)


    

    print("【ping通的ip数】：", count_True, "【ping不通的ip数】：", count_False)
    print('程序运行耗时：%s' % (time.time() - start_time))