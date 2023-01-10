import os,sys
from openpyxl import Workbook

os.chdir(sys.path[0])

"""
for root,dirs,files in os.walk(base)
首先，os.walk(base) 返回的是一个生成器，是一个元组tuple(root,dirs,files)，
是一个可迭代的对象，所以能用for循环遍历，
这个tuple包含三个元素：
第一个是root，表示“走”到了哪个文件夹位置，指的是当前正在遍历的这个文件夹的本身的地址
第二个是dirs，是一个list ，内容是该文件夹中所有的目录的名字(不包括子目录)，
第三个是files，内容是该文件夹中所有的文件(不包括子目录)。
"""
def get_file_list(xdir):
    tfile_list = []
    for root,dirs,files in os.walk(xdir): 
        #这个tuple里只有三个元素，for循环一次取完，所以实际上并没有循环，且必须一次取完，即使这个脚本不用root,dirs
        for file in files:
            tfile_list.append(os.path.join(root,file))
            #print(os.path.join(root,file))
            #print os.path.join(root,file).decode('gbk').encode('utf-8')
    return(tfile_list)



def get_key_word(xfile):
    trow = []
    with open(xfile, "r") as temp_file:
        xlist = [line.strip() for line in temp_file if line.strip()]
    for line in xlist:
        tlist1 = line.split(' ')
        if tlist1[0] == "hostname":
            trow.append(tlist1[1])

        if tlist1[0] == "PID:":
            trow.append(tlist1[-1])
            break
    return trow


def list2d_to_xlsx(xlist2d):
#写入Excel文件
    wb = Workbook()
    ws = wb.active
    for i in range(len(xlist2d)):
        ws.append(xlist2d[i])
    wb.save('SN Result.xlsx')


if __name__ == '__main__':
    rlist_2d = []
    file_list = get_file_list("dir")    #得到所有文件的路径列表
    #print(file_list)
    for file_path in file_list:   #遍历所有文件
        if get_key_word(file_path):    #如果文件中得到的项不为空
            rlist_2d.append(get_key_word(file_path))
        else:
            rlist_2d.append(["Not Cisco"])   #追加一个项
    
    #print(rlist_2d)
    list2d_to_xlsx(rlist_2d)



