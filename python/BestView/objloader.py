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
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.eye = []
        self.area = 0   #总片面面积
        self.eyearea = 0
        self.maxX = 0
        self.minX = 0
        self.maxY = 0
        self.minY = 0
        self.maxZ = 0
        self.minZ = 0

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'e':
                v = [int(x) for x in values[1:4]]
                self.eye.append(v)
            if values[0] == 'v':
                v = [float(x) for x in values[1:4]]
                if swapyz:
                    v = v[2], v[0], v[1]
                if v[0] > self.maxX:
                    self.maxX = v[0]
                if v[0] < self.minX:
                    self.minX = v[0]
                if v[1] > self.maxY:
                    self.maxY = v[1]
                if v[1] < self.minY:
                    self.minY = v[1]
                if v[2] > self.maxZ:
                    self.maxZ = v[2]
                if v[2] < self.minZ:
                    self.minZ = v[2]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = [float(x) for x in values[1:4]]
                if swapyz:
                    v = v[2], v[0], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                v = [float(x) for x in values[1:3]]
                self.texcoords.append(v)
            elif values[0] == 'f':
                face = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                self.faces.append(face)

        self.create_bbox()
        self.getarea()

    def create_bbox(self):
        ps = np.array(self.vertices)
        #vmin = ps.min(axis=0)
        #vmax = ps.max(axis=0)
        self.bbox_center = ps.mean(axis=0)
        #self.bbox_half_r = np.max(vmax - vmin) / 2
        self.bbox_half_r = np.sqrt(((self.maxX - self.minX) / 2) ** 2 + ((self.maxY - self.minY) / 2) ** 2 + (
                    (self.maxZ - self.minZ) / 2) ** 2)


    def getarea(self):   #总片面面积
        for index in self.faces:
            #index = face[0]
            self.area = self.area + getarea(self.vertices[index[0]-1], self.vertices[index[1]-1], self.vertices[index[2]-1])
        #for index in self.eye:
        #    self.eyearea = self.eyearea + getarea(self.vertices[index[0] - 1], self.vertices[index[1] - 1],
        #                                    self.vertices[index[2] - 1])
        #print("eyearea" + str(self.eyearea))
        #print("总面积")
        #print(self.area)
