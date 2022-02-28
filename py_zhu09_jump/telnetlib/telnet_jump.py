import telnetlib

Host = ""   # 跳板机ip

# 连接Telnet服务器
tn = telnetlib.Telnet(Host, port=23, timeout=10)
tn.set_debuglevel(0)
# 输入跳板机用户名
tn.read_until(b'Username:')   # 这个是获取提示的，有的机器显示的是login或者其他的，根据自己情况修改就行了
tn.write(b"boot" + b'\n')
# 输入跳板机密码
tn.read_until(b'Password:')
tn.write(b"123456" + b'\n')
# 跳到服务器
tn.write(b"telnet 0.5.3.2" + b'\n')
# 输入服务用户名

tn.read_until(b'>>User name:')
tn.write(b"root" + b'\n')

# 输入服务登录密码
tn.read_until(b'>>User password:')
tn.write(b"123456" + b'\n')
tn.write(b'测试命令' + b'\n')

r = tn.read_until(b'#')   # 获取的是#之间的输出，当命令没有以# 结束就换成你的结束标志
sr = str(r, encoding="utf-8")
print(sr)

tn.close()