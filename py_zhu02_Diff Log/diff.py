import difflib
import codecs
import time
import os
import shutil

date = time.strftime("%Y%m%d", time.localtime())


def cphtml(file1, file2, diffres):     #“生成比较文件html”函数
    with open(file1)  as f1, open(file2) as f2:
       text1 = f1.readlines()
       text2 = f2.readlines()
    
    diff = difflib.HtmlDiff()
    with codecs.open(diffres+".html", 'w','utf-8') as f:
        f.write(diff.make_file(text1, text2))  



def cpAandB():
    DateList = os.listdir('.')    #得到log文件夹列表
    
    while True:
        dateA = input("Please input the old dateA (YYYYMMDD):")
        if dateA in DateList:
            break
        else:
            print("No log of the date. Please input the dateA agian")
            continue
        
    while True:
        dateB = input("Please input the new dateB (YYYYMMDD):")
        if dateB in DateList:
            break
        else:
            print("No log of the date. Please input the dateB agian")
            continue


    newfile = ('./diff_'+date)
    os.mkdir(newfile)


    LogListA = os.listdir(dateA)    #得到log列表
    LogListB = os.listdir(dateB)
    
    LogListLen = len(LogListA)
    
    for i in range(0, LogListLen):
        PathA = ('./'+dateA+'/'+LogListA[i])
        PathB = ('./'+dateB+'/'+LogListB[i])

        data1 = open(PathA).read()
        open(PathA).close()
        data2 = open(PathB).read()
        open(PathB).close()

        if data1 == data2:
            pass
        else:
            print(LogListA[i]+" changed, please check the html")
            resmane = LogListA[i]
            cphtml(PathA, PathB, resmane)
            shutil.move('./'+LogListA[i]+'.html', './diff_'+date)    #将生成的html文件移入比较文件夹



def main():
    cpAandB()



if __name__ == '__main__':
    main()

