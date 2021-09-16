import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from openpyxl import Workbook
import os,sys

os.chdir(sys.path[0])

def txt_to_list(xfile):
#将文件逐行读取到一个列表
    with open(xfile,'r') as temp_file:
        xlist = temp_file.read().splitlines()
    return(xlist)

def demand_ip(ip):
    header = {"User-Agent": UserAgent().random}    #伪造head的User-Agent字段，假装是从浏览器发出的请求
    sourse_html = 'https://www.ip.cn/?ip={}'      #根据网站不同链接不同

    sourse_html = sourse_html.format(ip)    #参数ip来代替sourse_html里面的大括号
    response = requests.get(sourse_html, headers = header)     #headers这个参数有些教程里没有

    bs0bj = BeautifulSoup(response.text, 'lxml')
    ip_address_tag = []
    text_list = []
    ip_address_tag = bs0bj.find("div", {'class': 'well'}).find_all('code')    #两次查找
    for item in ip_address_tag:
        text = item.get_text()#.strip()           #提取tag里面的text
        text_list.append(text)
    return text_list


def list2d_to_xlsx(xlist2d):
#写入Excel文件
    wb = Workbook()
    ws = wb.active
    ws.append(['您查询的IP','所在地理位置','GeoIP'])
    for i in range(len(xlist2d)):
        ws.append(xlist2d[i])
    wb.save('IpGet.xlsx')


def main():
    ip_list = []
    ip_list = txt_to_list('iplist.txt')
    
    result_list = []
    for ip in ip_list: 
        result_list.append(demand_ip(ip))

    #print(result_list)
    list2d_to_xlsx(result_list)


if __name__ == '__main__':
    main()