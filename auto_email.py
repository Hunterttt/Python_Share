import smtplib
import os
import time

from email.mime.text import MIMEText


def send_mail(subject, message):
# メールを送信
	from_addr = "tianyuanttt@yahoo.co.jp"
	#to_addr = "tianyuan.ttt@hotmail.com"      #发个单个地址

	to_addrs = ["tianyuan.ttt@hotmail.com","tianyuan.ttt@gmail.com"]    #发给多个地址
	user_name = from_addr
	passwd = "wasaxqwaxs5"
	
	msg = MIMEText(message)
	msg['Subject'] = subject
	msg['From'] = from_addr
	#msg['To'] = to_addr
	msg['To'] = ",".join(to_addrs)
	
	smtp = smtplib.SMTP("smtp.mail.yahoo.co.jp", 587)
	smtp.login(user_name, passwd)
	#smtp.sendmail(from_addr, to_addr, msg.as_string())    #发给单个地址
	smtp.sendmail(from_addr, to_addrs, msg.as_string())    #发给多个地址
	smtp.quit()


def txt_to_list(xfile):
#将文件逐行读取到一个列表
    with open(xfile,'r') as temp_file:
        xlist = temp_file.read().splitlines()
    return(xlist)


def main():
	#ip_list = []
	ip_list = txt_to_list('iplist.txt')
	#print(ip_list)
	while True:
		rlist = []
		for i in ip_list:
			result = os.popen('ping %s' %i)
			if 'bytes=32 time=' in result.read():
				print('Can ping %s' %i)
			else:
				print('Can not ping %s' %i)
				rlist.append('Can not ping %s' %i)

		if len(rlist) == 0:
			pass
		else:
			print('Sending email')
			ip = '\n'.join(i for i in rlist)
			send_mail("Camera issue", "Hi all\n\nSome cameras are not online, please check.\n\n"+ip+'\n\nFusion Systems')
		
		time.sleep(5)


if __name__ == '__main__':
    main()
