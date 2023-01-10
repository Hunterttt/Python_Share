import xlrd
import time
from netmiko import Netmiko
import os

date = time.strftime("%Y%m%d", time.localtime())

def open_excel(xfile):
#打开要解析的Excel文件
    try:
        data = xlrd.open_workbook(xfile)
        return data
    except Exception as e:
      print(e)


def excel_to_list2d(excel_file, by_index):   #by_index表示选择excel里面的第几个Sheet
#将excel表中的各个值读入一个二维数组
    data = open_excel(excel_file)
    table = data.sheets()[by_index]

    totalarray = []
    for row in range(table.nrows):
        subarray = []
        for col in range(table.ncols):
            subarray.append(table.cell(row,col).value)
        totalarray.append(subarray)

    return(totalarray)   #返回这个二维数组


def show_to_txt(namepass,command):
    b = len(namepass)
    d = len(command)

    newfile = ('./'+date)
    os.mkdir(newfile)
    os.chdir(newfile)

    for j in range(1,b):
        print('Now is checking '+namepass[j][1]+',the ip address is '+namepass[j][2])
        my_device = {
            "host": namepass[j][2],
            "username": namepass[j][4],
            "password": namepass[j][5],
            "device_type": "cisco_ios",
        }
        
        net_connect = Netmiko(**my_device)
        
        write_file = open(namepass[j][1]+'_'+date+'.txt', 'w')   #模式为追加

        for n in range(0,d):
            print(command[n][1], file=write_file)
            print("\n", file=write_file)
            
            output = net_connect.send_command(command[n][1])
            
            print(output, file=write_file)
            print("\n=============================================\n", file=write_file)
        write_file.close()
        
        net_connect.disconnect()
    
    os.chdir('..')


def main():
    temp_namepass = excel_to_list2d('Zhu_list.xlsx', 0)
    temp_command = excel_to_list2d('Zhu_list.xlsx', 1)

    show_to_txt(temp_namepass,temp_command)


if __name__ == '__main__':
    main()








