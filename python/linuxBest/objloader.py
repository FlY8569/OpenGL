# -*- coding: utf-8 -*-
import numpy as np

#计算3d 面片面积
def getarea(a, b, c):
    ab = np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
    ac = np.sqrt((a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2 + (a[2] - c[2]) ** 2)
    bc = np.sqrt((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 + (b[2] - c[2]) ** 2)
    s = (ab + ac + bc) / 2.0
    area = np.sqrt(s * (s - ab) * (s - ac) * (s - bc))
    return area

class OBJ:
    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.faces = []
        self.eye = []
        self.area = 0   #总片面面积

        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'e':
                v = [int(x) for x in values[1:4]]
                self.eye.append(v)
            if values[0] == 'v':
                v = [float(x) for x in values[1:4]]
                if swapyz:
                    v = v[2], v[0], v[1]
                self.vertices.append(v)

            elif values[0] == 'f':
                face = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                self.faces.append(face)

        self.getarea()


    def getarea(self):   #总片面面积
        for index in self.faces:
            self.area = self.area + getarea(self.vertices[index[0]-1], self.vertices[index[1]-1], self.vertices[index[2]-1])

