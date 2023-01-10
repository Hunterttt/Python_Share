import xlrd
from netmiko import Netmiko
import os
import sys
import time
import win32gui
import win32api
from pynput.mouse import Button, Controller as mController
from pynput.keyboard import Key, Controller as kController

mouse = mController()
keyboard = kController()
name = input("input name: ")      #输入发给谁

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


# 传入类名，标题，返回tuple(句柄，坐标左，坐标左顶，坐标左右，坐标左底)
def findWindow(classname, titlename):
    hand = win32gui.FindWindow(classname, titlename)
    if(hand != 0):
        left, top, right, bottom = win32gui.GetWindowRect(hand)
        return{'hand': hand, 'left': left, 'top': top, 'right': right, 'bottom': bottom}
    else:
        print("找不到[%s]这个人/群" % titlename)
        return 0


# 发送消息,需要窗口标题，消息内容两个参数
def to_wechat(windowTitle, message):
# 微信pc端的输入框都没有句柄，所以需要通过模拟点击来获得焦点
    winClass = "ChatWnd" # 默认是微信消息
    win = findWindow(winClass, windowTitle)
    if(win):
        win32gui.SetForegroundWindow(win['hand'])
        time.sleep(0.2) # 这里要缓一下电脑才能反应过来，要不然可能找不到焦点
        inputPos = [win['right']-50, win['bottom']-50]
        win32api.SetCursorPos(inputPos) # 定位鼠标到输入位置

    # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
        mouse.press(Button.left)
        mouse.release(Button.left)
        keyboard.type(message) # 程序运行时候，这里一定要是英文输入状态，要不然可能无法发送消息
    # 发送消息的快捷键是 Alt+s
        with keyboard.pressed(Key.alt):
            keyboard.press('s')
            keyboard.release('s')
    else:
        print("发送消息给[%s]失败" % windowTitle)


def show_to_wechat(namepass,command):
    b = len(namepass)
    d = len(command)

    for j in range(1,b):
        print('Now is checking '+namepass[j][1]+',the ip address is '+namepass[j][2])
        my_device = {
            "host": namepass[j][2],
            "username": namepass[j][4],
            "password": namepass[j][5],
            "device_type": "cisco_ios",
        }
        
        net_connect = Netmiko(**my_device)
            
        for n in range(0,d):   
            output = net_connect.send_command(command[n][1])
            to_wechat(name, '######'+command[n][1]+'######\n\n'+output)


        
        net_connect.disconnect()



def main():
    temp_namepass = excel_to_list2d('Zhu_list.xlsx', 0)
    temp_command = excel_to_list2d('Zhu_list.xlsx', 1)

    times = int(input("input times: "))     #输入重复几次
    interval = int(input("input interval: "))     #输入间隔时间
    for i in range(0,times):
        print(i+1)
        show_to_wechat(temp_namepass,temp_command)
        i+=1
        time.sleep(interval)


if __name__ == '__main__':
    main()








