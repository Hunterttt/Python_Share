import ipaddress

def txt_to_dict(xfile):
    xdict = {}
    temp_file = open(xfile,'r+')
    for line in temp_file:
        (key,value) = line.strip().split(' ',1)    #对每行内容以空格进行切割，只切割一次
        xdict[key] = value
    temp_file.close()
    return(xdict)


def dict0_to_list(xdict):
#把字典中的key提取出来，放在一个列表里
    xlist = []
    for key in xdict:
        xlist.append(key)
    return(xlist)


def bubble_sort_improve(lst2):    #进阶冒泡排序法，看笔记
#对key列表进行排序
    lstlen = len(lst2)
    i = 1; times = 0
    while i > 0:
        times += 1
        change = 0
        for j in range(1, lstlen):
            if ipaddress.IPv4Address(lst2[j-1]) > ipaddress.IPv4Address(lst2[j]):   #ipaddress.IPv4Address可以直接将IP地址转换为数值
#使用标记记录本轮排序中是否有数据交换
                change = j
                lst2[j],lst2[j-1] = lst2[j-1],lst2[j]
        #print(('sorted {0}:{1}').format(times, lst2))
#将数据交换标记作为循环条件，决定是否继续进行排序
        i = change
    return(lst2)


def dict_to_txt(xlist,xdict):
#遍历排序后的key列表，再从原来的字典中取出相应的值，一起写入文件
    temp_file = open('sort_dict.txt','w')
    for i in range(0,len(xlist)):
        temp_file.write(xlist[i]+xdict[xlist[i]]+'\n')
    temp_file.close()



def main():
    temp_dic = txt_to_dict('ipall.txt')

    temp_list = dict0_to_list(temp_dic)

    temp_list = bubble_sort_improve(temp_list)

    dict_to_txt(temp_list,temp_dic)



if __name__ == '__main__':
    main()