import numpy as np
from OpenGL.GL import *

def sameside(A, B, C, P):

    ab = np.array([A[0] - B[0], A[1] - B[1], A[2] - B[2]])
    ac = np.array([C[0] - A[0], C[1] - A[1], C[2] - A[2]])
    ap = np.array([P[0] - A[0], P[1] - A[1], P[2] - A[2]])
    v1 = np.cross(ab, ac)
    v2 = np.cross(ab, ap)
    if np.dot(v1, v2) > 0:
        return True
    return False

def visible(obj, vpnormal):
    m = 0
    face = []
    for row in obj.faces:
        face.append(row[0])
    visVertices = obj.vertices[:]
    for i in range(len(face)):
        v1index = face[m][0] - 1
        v2index = face[m][1] - 1
        v3index = face[m][2] - 1
        vx1 = visVertices[v1index][0]
        vy1 = visVertices[v1index][1]
        vz1 = visVertices[v1index][2]
        vx2 = visVertices[v2index][0]
        vy2 = visVertices[v2index][1]
        vz2 = visVertices[v2index][2]
        vx3 = visVertices[v3index][0]
        vy3 = visVertices[v3index][1]
        vz3 = visVertices[v3index][2]
        a = (vy1 - vy2) * (vz1 - vz3) - (vy1 - vy3) * (vz1 - vz2)
        b = (vz1 - vz2) * (vx1 - vx3) - (vx1 - vx2) * (vz1 - vz3)
        c = (vx1 - vx2) * (vy1 - vy3) - (vx1 - vx3) * (vy1 - vy2)
        curnormal = np.array([a, b, c])

        if np.dot(vpnormal, curnormal) <= 0:
            del face[m]
            m = m - 1
        m = m + 1
        #
    for k in range(len(face)-1, -1, -1):
        cnt = 0
        for i in face[k]:
            vx = visVertices[i-1][0]
            vy = visVertices[i-1][1]
            vz = 0
            p = [vx, vy, vz]
            for j in face:
                v1index = j[0] - 1
                v2index = j[1] - 1
                v3index = j[2] - 1
                if v1index == i or v2index == i or v3index == i:
                    break
                vx1 = visVertices[v1index][0]
                vy1 = visVertices[v1index][1]
                vz1 = 0
                vx2 = visVertices[v2index][0]
                vy2 = visVertices[v2index][1]
                vz2 = 0
                vx3 = visVertices[v3index][0]
                vy3 = visVertices[v3index][1]
                vz3 = 0
                a = [vx1, vy1, vz1]
                b = [vx2, vy2, vz2]
                c = [vx3, vy3, vz3]
                if sameside(a, b, c, p) and sameside(b, c, a, p) and sameside(c, a, b, p):
                    arrz = visVertices[v1index][2] + visVertices[v2index][2] + visVertices[v3index][2]
                    if visVertices[i-1][2] <= arrz / 3:
                        cnt = cnt+1
        if cnt >= 1:
            del face[k]
    return face


class A2:
    def __init__(self, obj, vpoint):
        self.obj = obj
        self.core = obj.bbox_center[:]  # 图形中心
        self.vp = vpoint  # 视点位置
        self.visface = None


    def getvisibleface(self):
        self.visface = visible(self.obj,self.vp)
        print(self.visface)


    def get_a2_list(self):
        self.a2_list = glGenLists(1)
        glNewList(self.a2_list, GL_COMPILE)
        glColor3f(1.0, 1.0, 1.0)

        for face in self.visface:
            glBegin(GL_POLYGON)
            for i in range(len(face)):
                glVertex3fv(self.obj.vertices[face[i] - 1])
            glEnd()
        glEndList()
