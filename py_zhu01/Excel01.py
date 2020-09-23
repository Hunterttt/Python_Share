import xlrd


def open_excel(file = 'file.xlsx'):#打开要解析的Excel文件
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
      print(e)

def read_excel(file = 'file.xlsx', by_index = 0):#直接读取excel表中的各个值
    data = open_excel(file)#打开excel文件
    table = data.sheets()[by_index]#选择excel里面的Sheet

    totalarray = []
    for row in range(table.nrows):
        subarray = []
        for col in range(table.ncols):
            subarray.append(table.cell(row,col).value)
        totalarray.append(subarray)

    print(totalarray[1][1])
    print(totalarray[2][2])
    return(totalarray)




  
  


def main():
	read_excel('Zhu_list.xlsx', 0)



if __name__ == '__main__':
    main()








