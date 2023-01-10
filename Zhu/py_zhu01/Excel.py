import time
import xlrd



def open_excel(file = 'file.xlsx'):#打开要解析的Excel文件
  try:
    data = xlrd.open_workbook(file)
    return data
  except Exception as e:
    print(e)

def read_excel(file = 'file.xlsx', by_index = 0):#直接读取excel表中的各个值
  ip = []
  data = open_excel(file)#打开excel文件
  tab = data.sheets()[by_index]#选择excel里面的Sheet
  nrows = tab.nrows#行数
  ncols = tab.ncols#列数
  for x in range(1, nrows):
     for y in range(1, ncols):
       if y==2:
           ip.append(tab.cell(x,y))
           #value = tab.cell(x,y).value
           print(tab.cell(x,y).value)
       else:
           #value = tab.cell(x,y).value
           print(tab.cell(x,y).value)
  for i in range(0,len(ip)):
        print (ip[i].value)



def main():
	read_excel('Zhu_list.xlsx', 0)



if __name__ == '__main__':
  main()
