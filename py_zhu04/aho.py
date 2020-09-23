import ipaddress

def txt_to_2dlist(xfile):
#文档读为二维数组
    list2d = []
    temp_file = open(xfile,'r+')
    for line in temp_file:
        if '*' in line:
            pass
        else:
            list2d.append(line.strip().split(','))
    temp_file.close()
    return(list2d)


def prefix_to_arrange(xlist):
    arrange = []
    for i in range(0,len(xlist)):
        arrange.append(xlist[i][0] + ':   ' + str(ipaddress.IPv4Network(xlist[i][0])[1]) + ' - ' + str(ipaddress.IPv4Network(xlist[i][0])[-2]))    #选出地址列表中的正数第二个和倒数第二个
    return(arrange)


def list_to_txt(xlist):
#将列表写入新文件
    temp_file=open('arrange.txt','w')
    temp_file.write('\n'.join(xlist))
    temp_file.close()


def main():
    temp_2dlist = txt_to_2dlist('boss.txt') 
    temp_arrange = prefix_to_arrange(temp_2dlist)
    list_to_txt(temp_arrange)

if __name__ == '__main__':
    main()
