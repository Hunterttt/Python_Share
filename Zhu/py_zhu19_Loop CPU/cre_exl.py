import os,sys
import openpyxl

os.chdir(sys.path[0]) 

wb = openpyxl.Workbook()
ws = wb.active
wb.save('show_cpu.xlsx')