import os,socket,sys
from pathlib import Path 
from openpyxl import Workbook

ports = input("Enter the ports you want to check, use ',' to separate, then press Enter\nEX '22,23,139'\n: ")
ports_list = [int(n) for n in ports.split(",")]    #逗号隔开变数组

socket.setdefaulttimeout(4)

current_folder = Path(__file__).absolute().parent 
os.chdir(str(current_folder)) 


def txt_to_list(xfile):
#将文件逐行读取到一个列表
    with open(xfile, "r") as temp_file:
        xlist = [line.strip() for line in temp_file if line.strip()]
    return(xlist)

def PortOpen(ip,port):
#socket try connect
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        s.connect((ip,port))
        s.shutdown(2)
        return "Open"

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