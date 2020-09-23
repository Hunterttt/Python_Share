import xlrd
import time
from netmiko import ConnectHandler
from netmiko import redispatch


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
    
    jumpserver = {
        "device_type": "terminal_server",         ##1
        "ip": "192.168.32.10",               ##2
        "username": "man",         ##3
        "password": "cisco",         ##4
        "secret": "fuck"                ##4
        }
        
    net_connect = ConnectHandler(**jumpserver)
    # Manually handle interaction in the Terminal Server (fictional example, but 
    # hopefully you see the pattern)
    time.sleep(3)
    net_connect.write_channel("\n")
    time.sleep(1)
    output = net_connect.read_channel()
    # Should hopefully see the terminal server prompt
    #print(output)

    for j in range(1,b):
        print('Now is checking '+namepass[j][1]+',the ip address is '+namepass[j][6])

        # Login to end device from terminal server
        net_connect.write_channel("telnet "+namepass[j][6]+"\n")
        time.sleep(3)


        
        # Manually handle the Username and Password
        max_loops = 5
        i = 1
        while i <= max_loops:
            output = net_connect.read_channel()
            
            if 'sername:' in output:
                net_connect.write_channel(namepass[j][7] + '\n')
                time.sleep(1)
                output = net_connect.read_channel()
        
            # Search for password pattern / send password
            if 'assword:' in output:
                net_connect.write_channel(namepass[j][8] + '\n')
                time.sleep(1)
                output = net_connect.read_channel()
                # Did we successfully login

            if '>' in output:
                net_connect.write_channel('enable\n')
                time.sleep(1)
                output = net_connect.read_channel()
                if 'assword:' in output:
                    net_connect.write_channel(namepass[j][9] + '\n')
                    time.sleep(1) 
                    output = net_connect.read_channel() 
                if '#' in output:  
                    break             
            elif '#' in output:
                break
                
            net_connect.write_channel('\n')
            time.sleep(1)
            i += 1

        # We are now logged into the end device 
        # Dynamically reset the class back to the proper Netmiko class   
        redispatch(net_connect, device_type='cisco_ios')    #
        #net_connect.send_command('show version')

        write_file = open(namepass[j][1]+'_'+date+'.txt', 'w')   #模式为追加
        
        for n in range(0,d):
            print(command[n][1], file=write_file)
            print("\n", file=write_file)

            output = net_connect.send_command(command[n][1])

            print(output, file=write_file)
            print("\n=============================================\n", file=write_file)
        write_file.close()



        """
        net_connect.write_channel("ssh xx@10.30.1.11\n")    #连接远程机器,必须得带回车
        time.sleep(3)                                                 #必须得等待几秒，否则读取不到返回
        result = net_connect.read_channel()                    #读取返回结果
        if 'assword' in result:
            net_connect.write_channel("password\n")     #输入密码
            time.sleep(5)
        """

        
    net_connect.disconnect()
    


def main():
    temp_IP = excel_to_list2d('Zhu_list.xlsx', 1)
    temp_command = excel_to_list2d('Zhu_list.xlsx', 2)

    show_to_txt(temp_IP,temp_command)


if __name__ == '__main__':
    main()