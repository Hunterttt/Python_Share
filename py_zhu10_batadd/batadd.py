import os


dir_path = os.path.dirname(os.path.abspath(__file__))    #py文件的所在文件夹的绝对路径


def namelist():

    AllList = os.listdir(dir_path)          #将文件夹中文件名字读成一个列表
    NameList = []

    for name in AllList:
        if name.endswith('.bat'):
            NameList.append(name)
        else:
            pass

    print(NameList)
    return(NameList)


def batadd(NameList):
    os.chdir(dir_path)     #到py文件的所在文件夹
    NameListLen = len(NameList)
    
    for i in range(NameListLen):
        with open(NameList[i],'r+') as temp_file:    #r+表示即可读又可写
            content = temp_file.read()      #文件内容
            xlist = content.splitlines()  #把每个文件读到一个列表中
            if "@echo off" in xlist[0]:
                pass
            else:   #在文件前加一行
                temp_file.seek(0, 0)
                temp_file.write('@echo off\n'+content)


def main():
    BatList = namelist()
    batadd(BatList)


if __name__ == '__main__':
    main()
