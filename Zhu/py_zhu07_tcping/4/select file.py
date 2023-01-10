import tkinter
from tkinter import filedialog

root = tkinter.Tk()          #打开交互窗口，没有下面的withdrew的话，后面会有一个tkinter的小窗口
root.withdraw()           #不显示tkinter的小窗口

filename = filedialog.askopenfilename()      #得到文件的绝对路径
print(filename)