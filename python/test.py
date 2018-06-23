list = [[1,2,3], [2,5,6]]
fl=open('list.txt', 'w')
for i in list:
    for j in i:
        fl.write(str(j))
        fl.write(" ")
    fl.write("\n")
fl.close()
