import os
import re


# 获取文件路径
def filePath(path):
    for name in os.scandir(path):
        # 有文件夹递归
        if name.is_dir():
            print('has subfolder')
        else:
            if bool(re.search('cdp nei',name.path)):     #bool() 函数用于将给定参数转换为布尔类型，如果没有参数，返回 False。
                print('has show cdp nei file')
            else:
                onefile = fileRead(name.path)
                for line in onefile:
                    result_list.append(line)
                result_list.append("\n\n\n\n\n\n\n\n\n\n")


# 读文件
def fileRead(read_path):
    one_file_list = []  #记录提取的文件内容

    # 打开文件
    with open(read_path,'r') as temp_file:
        ilist = temp_file.read().splitlines()
        #print(ilist)

    for line in ilist:
        #print(type(line))
        #print(line)
        if "hostname" in line:
            ihostname = line.split(' ')[1]
            one_file_list.append(ihostname)
            break
        else:
            pass

    for i in range(len(ilist)):
        if "show inventory" in ilist[i]:
            one_file_list.append("#################show inventory##################")
            tkey = ihostname+"#"
            j = i+1
            while tkey not in ilist[j]:
                one_file_list.append(ilist[j])
                j+=1
        else:
            pass

        if "show int status" in ilist[i]:
            one_file_list.append("#################show int status##################")
            tkey = ihostname+"#"
            j = i+1
            while tkey not in ilist[j]:
                one_file_list.append(ilist[j])
                j+=1
        else:
            pass

        if "show env all" in ilist[i]:
            one_file_list.append("#################show env all##################")
            tkey = ihostname+"#"
            j = i+1
            while tkey not in ilist[j]:
                one_file_list.append(ilist[j])
                j+=1
        else:
            pass


        if "show processes memory" in ilist[i]:
            one_file_list.append("#################show processes memory##################")
            tkey = ihostname+"#"
            j = i+1
            while tkey not in ilist[j]:
                one_file_list.append(ilist[j])
                j+=1
        else:
            pass

        if "show logging" in ilist[i]:
            one_file_list.append("#################show logging##################")
            tkey = ihostname+"#"
            j = i+1
            while tkey not in ilist[j]:
                one_file_list.append(ilist[j])
                j+=1
        else:
            pass

    
    #print(one_file_list)
    return one_file_list

    






if __name__ == '__main__':
    result_list = []       # 接收结果数据

    xread_path = input("Enter the path: ")
    filePath(xread_path)
    write_path = xread_path+"\\all.txt"
    with open(write_path,'w') as file_data:
        for tline in result_list:
            file_data.write(tline+'\n')
    file_data.close()