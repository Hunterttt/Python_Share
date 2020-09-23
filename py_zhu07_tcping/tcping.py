import os
import subprocess
import time
from pathlib import Path

def txt_to_list(xfile):
#将文件逐行读取到一个列表
    with open(xfile,'r') as temp_file:
        xlist = temp_file.read().splitlines()
    return(xlist)


def tcping(xlist):
#导入要执行的命令行列表
    start_Time = int(time.time())
    count_True, count_False = 0, 0
    ping_Folder = str(Path.cwd())   #获取当前脚本所在路径
    with open(ping_Folder + '/ip_True.txt', 'w+') as ip_True, \
            open(ping_Folder + '/ip_False.txt', 'w+') as ip_False:
        for index in range(len(xlist)):  
            output = subprocess.getoutput(xlist[index])     #逐行执行命令行，并获取执行结果 
            print(output)          #把执行结果输出在屏幕上
            if 'out' in output:            #如果输出结果中有（time）out字样，tcping失败
                print('%s is fail' % xlist[index])
                ip_False.write(xlist[index]+"\n")
                count_False += 1
            else:
                print ('%s is ok' % xlist[index])
                ip_True.write(xlist[index]+"\n")
                count_True += 1
        ip_False.write("【ping不通的ip数】：%d" % count_False)
        ip_True.write("【ping通的ip数】：%d" % count_True)
        end_Time = int(time.time())
        print("【time(秒)】：", end_Time - start_Time, "s")
        print("【ping通的ip数】：", count_True, "【ping不通的ip数】：", count_False)


def main():
    tlist = txt_to_list('tcping_list.txt')
    tcping(tlist)
        


if __name__ == '__main__':
    main()