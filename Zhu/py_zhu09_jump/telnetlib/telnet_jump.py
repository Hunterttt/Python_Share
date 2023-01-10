import telnetlib

Host = "192.168.32.101"   # 跳板机ip
J_username = 'admin'
J_password = 'Admin@123'
J_enable = '123.com'

k7_username = 'Cisco'
k7_password = '123.com'


def get_mac(xoutput):
    list2d = xoutput.split(' ')
    for i in list2d:
        if len(i) == 14 and '.' in i:
            return(i)
        else:
            pass



if __name__ == '__main__':

    tn = telnetlib.Telnet(Host, port=23, timeout=10)  # 连接Telnet服务器
    tn.set_debuglevel(0)    #The higher the value of debuglevel, the more debug output you get 

    tn.read_until(b'Username:')   # 这个是获取提示的，有的机器显示的是login或者其他的，根据自己情况修改就行了
    tn.write(bytes(J_username, encoding= 'utf-8') + b'\n')     #相当于b
    tn.read_until(b'Password:')
    tn.write(bytes(J_password, encoding= 'utf-8') + b'\n')
    tn.read_until(b'>')
    tn.write(b"ena" + b'\n')
    tn.read_until(b'Password:')
    tn.write(bytes(J_enable, encoding= 'utf-8') + b'\n')

    tn.read_until(b'#')
    tn.write(b"telnet 192.168.12.2" + b'\n')   # 跳到服务器

    tn.read_until(b'Username:')  
    tn.write(bytes(k7_username, encoding= 'utf-8') + b'\n')
    tn.read_until(b'Password:')
    tn.write(bytes(k7_password, encoding= 'utf-8') + b'\n')
    tn.read_until(b'#')

    #tn.read_until(b'>>User name:')
    #tn.write(b"root" + b'\n')
    #
    ## 输入服务登录密码
    #tn.read_until(b'>>User password:')
    #tn.write(b"123456" + b'\n')


    tgt_IP = input("Enter the target IP: ")

    tn.write(b'show ip arp ' + bytes(tgt_IP, encoding= 'utf-8') + b'\n')

    mac = tn.read_until(b'#')   # 获取的是#之间的输出，当命令没有以# 结束就换成你的结束标志

    mac1 = str(mac, encoding="utf-8")

    print(mac1)
    print(get_mac(mac1))

    tn.close()