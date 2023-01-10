import os, sys
from netmiko import Netmiko
from pathlib import Path 
from openpyxl import Workbook

'''
current_folder = Path(__file__).absolute().parent 
os.chdir(str(current_folder)) 
'''

os.chdir(sys.path[0]) 

def txt_to_list(xfile):
#将文件逐行读取到一个列表
    with open(xfile, "r") as temp_file:
        xlist = [line.strip() for line in temp_file if line.strip()]
    return(xlist)


def show_to_list(xlist):
    
    all_sw = []

    for i in range(len(xlist)):
        print('Checking '+xlist[i]+'...')
        my_device = {
            "host": xlist[i],
            "username": "admin",
            "password": "admin@123",
            "device_type": "cisco_ios",
        }

        net_connect = Netmiko(**my_device)


        output = net_connect.send_command("show cdp nei")

        one_sw = []   #一台SW的所有输出

        lines = output.split('\n')    #把输出按行分开，变成一个列表
        #print(lines)

        for j in range(len(lines)):
            
            #if "AP" in lines[j] or "" in lines[j]:
            if any(each in lines[j] for each in ["AP","com"]):
                one_ap = []     #说明找到一个AP，每次找到一个AP，把此列表重置
                #print(lines[j])
                line = lines[j].strip().split(' ')
                #print(line)
                
                slash = []    #把带有/的项收集起来
                for k in range(len(line)):
                    
                    if "/" in line[k]:
                        slash.append(line[k])
                        
                    else:
                        pass
                #print(slash)
                one_ap.append(xlist[i])
                one_ap.append(slash[0])
                #one_ap.append(line[0])

                output = net_connect.send_command("show int g"+slash[0]+" | in MTU")   #show接口速度

                one_ap.append(output)  

                one_ap.append(lines[j])      #加上AP输出的一行
            else:
                continue

            one_sw.append(one_ap)     #将每次得到的AP数据放入SW列表
        

        if len(one_sw) == 0:
            print("No AP is connected to this swtich!")
        else:        
            #print(one_sw)
            pass
        
        net_connect.disconnect()

        all_sw.extend(one_sw)

    #print(all_sw)

    return all_sw


def list2d_to_xlsx(xlist2d):
#写入Excel文件
    wb = Workbook()
    ws = wb.active
    for i in range(len(xlist2d)):
        ws.append(xlist2d[i])
    wb.save('Check AP int Spd.xlsx')



def main():
    IP_list = txt_to_list("iplist.txt")
    list2d = show_to_list(IP_list)
    list2d_to_xlsx(list2d)



if __name__ == '__main__':
    main()