import win32gui
import win32api
#import win32con
#import win32clipboard as clipboard
import time
from pynput.mouse import Button, Controller as mController
from pynput.keyboard import Key, Controller as kController

'''
发送微信消息逻辑
①找到微信窗口句柄
②把窗口放到最顶层，win32gui.SetForegroundWindow(win['hand'])就是这个作用
③在微信输入窗口点击一下，获得焦点
④输入消息内容，
⑤Alt+S,发送消息
'''

mouse = mController()
keyboard = kController()


# 传入类名，标题，返回tuple(句柄，坐标左，坐标左顶，坐标左右，坐标左底)
def findWindow(classname, titlename):
    hand = win32gui.FindWindow(classname, titlename)
    if(hand != 0):
        left, top, right, bottom = win32gui.GetWindowRect(hand)
        return{'hand': hand, 'left': left, 'top': top, 'right': right, 'bottom': bottom}
    else:
        print("找不到[%s]这个人/群" % titlename)
        return 0




# 发送消息,需要窗口标题，消息内容两个参数, 第三个可选，如果值true，就是发送QQ(Tim)消息，否则是微信消息
def send(windowTitle, message):
# 微信pc端的输入框都没有句柄，所以需要通过模拟点击来获得焦点.虽然QQ有句柄，但是为了统一，也用模拟点击吧
# 定位QQ(tim)窗口输入框位置，模拟鼠标点击来获得焦点。
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



def main():
    send("婷婷Caitlin", "焦耳")


if __name__ == '__main__':
    main()

'''
# 发送消息,需要窗口标题，消息内容两个参数, 第三个可选，如果值true，就是发送QQ(Tim)消息，否则是微信消息
def send(windowTitle, message, isqq=0):
# 微信pc端的输入框都没有句柄，所以需要通过模拟点击来获得焦点.虽然QQ有句柄，但是为了统一，也用模拟点击吧
# 定位QQ(tim)窗口输入框位置，模拟鼠标点击来获得焦点。
    if(isqq):
        winClass = "TXGuiFoundation" # 如果指明是QQ消息，那就发QQ消息。这里用的是TIM,如果是QQ消息的话，可以用None代替，或者自己用spy++查找
    else:
        winClass = "ChatWnd" # 默认是微信消息
        win = findWindow(winClass, windowTitle)
    if(win):
        win32gui.SetForegroundWindow(win['hand'])
        time.sleep(0.002) # 这里要缓一下电脑才能反应过来，要不然可能找不到焦点
        inputPos = [win['right']-50, win['bottom']-50]
        win32api.SetCursorPos(inputPos) # 定位鼠标到输入位置
    # win32gui.SendMessage


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




# 发送QQ消息,这里默认使用 TIM
def qqsend(windowTitle, message):
    win = findWindow("TXGuiFoundation", windowTitle)
if(win):
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(win32con.CF_UNICODETEXT, message)
    clipboard.CloseClipboard()
# 填充消息
    win32gui.SendMessage(win['hand'], 770, 0, 0)
# 回车发送消息
    win32gui.SendMessage(win['hand'], win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
else:
    print("发送消息给[%s]失败" % windowTitle)
'''