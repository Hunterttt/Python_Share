import ipaddress


def read_to_list(xfile):
#将文件逐行读取到一个列表
    with open(xfile,'r') as f:
        list = f.read().splitlines()
    return(list)


def bubble_sort_improve(lst2):    #要比较的IP地址列表
#进阶冒泡排序法，看笔记
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


def write_to_file(list):
#将列表写入新文件
    f=open("newiponly.txt","w")
    f.write('\n'.join(list))
    f.close()


def main():
    temp_list = read_to_list('iponly.txt')

    temp_list = bubble_sort_improve(temp_list)

    write_to_file(temp_list)


if __name__ == '__main__':
    main()