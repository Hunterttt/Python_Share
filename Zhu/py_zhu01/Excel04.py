import xlrd
import time
from netmiko import Netmiko
import os

date = time.strftime("%Y%m%d", time.localtime())

def open_excel(file = 'file.xlsx'):#打开要解析的Excel文件
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
      print(e)

def read_excel(file = 'file.xlsx', by_index = 0):#将excel表中的各个值读入一个二维数组
    data = open_excel(file)#打开excel文件
    table = data.sheets()[by_index]#选择excel里面的Sheet

    totalarray = []
    for row in range(table.nrows):
        subarray = []
        for col in range(table.ncols):
            subarray.append(table.cell(row,col).value)
        totalarray.append(subarray)

    return(totalarray)   #返回这个二维数组




def showcommand():
    array = []
    command = []
    array = read_excel('Zhu_list.xlsx', 0)
    command = read_excel('Zhu_list.xlsx', 1)

    b = len(array)
    d = len(command)

    newfile = ('./'+date)
    os.mkdir(newfile)
    os.chdir(newfile)

    for j in range(1,b):
        print('Now is checking '+array[j][1]+',the ip address is '+array[j][2])
        my_device = {
            "host": array[j][2],
            "username": array[j][4],
            "password": array[j][5],
            "device_type": "cisco_ios",
        }
        
        net_connect = Netmiko(**my_device)
        
        write_file = open(array[j][1]+'_'+date+'.txt', 'w')   #模式为追加

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
    showcommand()



if __name__ == '__main__':
    main()








