from openpyxl import Workbook


def txt_to_list2d(xfile):
#文档读为二维数组
    list2d = []
    temp_file = open(xfile,'r+')
    for line in temp_file:
        if ' ' not in line:
            subrow = []    #临时数组，存放单独的一行
            subrow.append(line.strip())
        else:
            tlist1 = line.strip().split(' ')
            tlist2 = list(filter(lambda x:len(x)>1,tlist1))    #去掉里面长度小于等于1的元素
            if (len(tlist2) == 6): 
                list2d.append(subrow + tlist2)
            elif (len(tlist2) == 5):      #mgmt0特殊的那行
                tlist2.insert(1,'')
                list2d.append(subrow + tlist2)
            else:
                list2d.append(tlist2)
    temp_file.close()
    for i in range(len(list2d)):    #合并元素
        list2d[i][1] += list2d[i][2]    
        list2d[i][5] += list2d[i][6]
        del list2d[i][6],list2d[i][2]
    return(list2d)


def list2d_to_xlsx(xlist2d):
#写入Excel文件
    wb = Workbook()
    ws = wb.active
    ws.append(['Device ID','Local Intrfce','Holdtme','Platform','Port ID'])
    for i in range(len(xlist2d)):
        ws.append(xlist2d[i])
    wb.save('cdp_tidied.xlsx')
 

def main():
    temp_list2d = txt_to_list2d('cdp.txt') 
    list2d_to_xlsx(temp_list2d)


if __name__ == '__main__':
    main()
