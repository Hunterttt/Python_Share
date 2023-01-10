import xlrd
import xlwt


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
    return(totalarray)


def only_five(parray,warray):
    b = len(parray)
    if b > 5:
        for i in range(0,5):
            #print(parray[i][1],'aaa')
            warray.append(parray[i])

    else:
        for i in range(0,b):
            #print(parray[i][1],'aaa')
            warray.append(parray[i])

    return(warray)


def divide(file = 'file.xlsx', by_index = 0):
    temparray = []
    writearray = []
    array = []
    array = read_excel(file, by_index)
    a = len(array)
    temparray.append(array[0])
    for i in range(1,a):
        if array[i-1][0] == array[i][0]:
            count = 1
            count += 1
            temparray.append(array[i])
            if i == (a-1):
                only_five(temparray,writearray)
                #(writearray[1][1])
            else:
                pass

        elif array[i-1][0] != array[i][0]:

            only_five(temparray,writearray)
            temparray = []
            temparray.append(array[i])
            if i == (a-1):
                only_five(temparray,writearray)
            else:
                pass
   
        else:
            pass

    return(writearray)


def writedown():
    array = []
    array = divide('gejie_Excel02.xlsx', 0)
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('My Worksheet')

    # 参数对应 行, 列, 值
    
    i = len(array)
    j = len(array[0])
    for row in range(0,i):
        for col in range(0,j):
            worksheet.write(row,col, label = array[row][col])

    #worksheet.write(1,0, array[1][1])
    # 保存
    workbook.save('Excel_test.xls')


def main():
    writedown()


if __name__ == '__main__':
    main()








