from pretreatment.eyeloader import *
from pretreatment.objloader import *

obj = OBJ("./TEA.obj", swapyz=False)
eye = EYE("./TEAEyes.obj", swapyz=False)

f = open('./TEA2.obj', 'a')
eyevisface = []
print(eye.faces)
#print(obj.faces)
for eyeface in eye.faces:
    e1index = eyeface[0] - 1
    e2index = eyeface[1] - 1
    e3index = eyeface[2] - 1
    ex1 = eye.vertices[e1index][0]
    ey1 = eye.vertices[e1index][1]
    ez1 = eye.vertices[e1index][2]
    ex2 = eye.vertices[e2index][0]
    ey2 = eye.vertices[e2index][1]
    ez2 = eye.vertices[e2index][2]
    ex3 = eye.vertices[e3index][0]
    ey3 = eye.vertices[e3index][1]
    ez3 = eye.vertices[e3index][2]
    for objface in obj.faces:
        o1index = objface[0] - 1
        ox1 = obj.vertices[o1index][0]
        oy1 = obj.vertices[o1index][1]
        oz1 = obj.vertices[o1index][2]
        if abs(ex1 - ox1) > 0.001 or abs(ey1 - oy1) > 0.001 or abs(ez1 - oz1) > 0.001:
            continue
        o2index = objface[1] - 1
        ox2 = obj.vertices[o2index][0]
        oy2 = obj.vertices[o2index][1]
        oz2 = obj.vertices[o2index][2]
        if abs(ex2 - ox2) > 0.001 or abs(ey2 - oy2) > 0.001 or abs(ez2 - oz2) > 0.001:
            continue
        o3index = objface[2] - 1
        ox3 = obj.vertices[o3index][0]
        oy3 = obj.vertices[o3index][1]
        oz3 = obj.vertices[o3index][2]
        if abs(ex2 - ox2) > 0.001 or abs(ey2 - oy2) > 0.001 or abs(ez2 - oz2) > 0.001:
            continue
        eyevisface.append(objface)
        break
print(eyevisface)
for line in eyevisface:
    f.write("e ")
    for i in line:
        f.write(str(i))
        f.write(" ")
    f.write("\n")
f.close()