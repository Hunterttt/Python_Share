from netaddr import IPAddress
import ipaddress

def txt_to_2dlist(xfile):
#文档读为二维数组
    list2d = []
    temp_file = open(xfile,'r+')
    for line in temp_file:
        list2d.append(line.strip().split(' '))
    temp_file.close()
    return(list2d)


def netmask_to_prefix(xlist):
    prefix = []
    for i in range(0,len(xlist)):
        pre2 = IPAddress(xlist[i][3]).netmask_bits()     #得到网络掩码数字
        pre1 = str(ipaddress.ip_network(xlist[i][2] + '/' + str(pre2), strict=False).network_address)   #得到网络前缀
        prefix.append(pre1 + '/' + str(pre2))
    return(prefix)


def list_to_txt(xlist):
#将列表写入新文件
    temp_file=open('prefix.txt','w')
    temp_file.write('\n'.join(xlist))
    temp_file.close()


def main():
    temp_2dlist = txt_to_2dlist('ipaddtosubnet.txt') 
    temp_prefix = netmask_to_prefix(temp_2dlist)
    list_to_txt(temp_prefix)

if __name__ == '__main__':
    main()
