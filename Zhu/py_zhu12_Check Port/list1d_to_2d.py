import numpy
l = [1,2,3,4,5,6,7,8]

arr = numpy.array(l)
result = arr.reshape(-1,1)  # 将一维数组变成4行5列  原数组不会被修改或者覆盖
print(result)
#l.resize((1, 8))  # 覆盖原来的数据将新的结果给原来的数组
#print(l)