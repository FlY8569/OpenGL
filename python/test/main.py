from test.loader import *
from test.visible import *
import math
import time
if __name__ == '__main__':
    ja = 1.57
    jb = 3.14
    R = 2000
    x = R * math.sin(ja) * math.cos(jb)
    y = R * math.sin(ja) * math.sin(jb)
    z = R * math.cos(ja)
    vpoint = [x, y, z]  # 视点
    obj = OBJ("tea1000e.obj", False)
    start = time.time()
    face = funVisible1(obj, vpoint)
    end = time.time()
    print(end - start)

    print(vpoint)
    f = open('./result.obj', 'a')
    for line in obj.vertices:
        f.write("v ")
        for i in line:
            f.write(str(i))
            f.write(" ")
        f.write("\n")
    for line in face:
        f.write("f ")
        for i in line:
            f.write(str(i))
            f.write(" ")
        f.write("\n")
    f.close()
