import numpy as np
from OpenGL.GL import *
from scipy.spatial import ConvexHull,Delaunay
import matplotlib.pyplot as plt


def fun(core, prosurface, vx, vy, vz,T):
    vpt = prosurface[0]*prosurface[0] + prosurface[1]*prosurface[1] + prosurface[2]*prosurface[2]
    t = ((core[0]-vx)*prosurface[0] + (core[1]-vy)*prosurface[1] + (core[2]-vz)*prosurface[2]) / vpt
    x = vx + prosurface[0] * t
    y = vy + prosurface[1] * t
    z = vz + prosurface[2] * t
    old = np.mat([x,y,z,1])
    new = old * T
    res = new.getA()
    print(res)
    return [res[0][0],res[0][2]]

def getTransform(a ,b ,c, core,prosurface):
    if (b*prosurface[2] - c*prosurface[1]) < 0.01:
        y = 0
        z = 0
    else:
        y = (c*prosurface[0] - a*prosurface[2]) / (b*prosurface[2] - c*prosurface[1])
        z = (a*prosurface[1] - b*prosurface[0]) / (b*prosurface[2] - c*prosurface[1])
    n = [1,y,z]    #新的y轴
    x0 = -(core[0]*1 + core[1]*y + core[2]*z)
    y0 = -(core[0]*a + core[1]*b + core[2]*c)
    z0 = -(core[0]*prosurface[0] + core[1]*prosurface[1] + core[2]*prosurface[2])
    T = np.mat([[1,y,z,x0],
                 [a,b,c,y0],
                 [prosurface[0], prosurface[1],prosurface[2],z0],
                 [0,0,0,1]])
    return T

def proPoint(obj, vpx, vpy, vpz, a, b, c): #  a b c 头朝向的方向
    #vpnormal = np.array([vpx, vpy, vpz])  #视点
    core = obj.bbox_center[:]  #中心
    face = []
    for row in obj.faces:
        face.append(row[0])
    visVertices = obj.vertices[:]
    prosurface = np.array([vpx-core[0], vpy-core[1], vpz-core[2]]) #投影面法向量
    propoint = []
    T = getTransform(a,b,c,core,prosurface)
    for i in range(len(face)):
        v1index = face[i][0] - 1
        v2index = face[i][1] - 1
        v3index = face[i][2] - 1
        vx1 = visVertices[v1index][0]
        vy1 = visVertices[v1index][1]
        vz1 = visVertices[v1index][2]
        propoint.append(fun(core, prosurface, vx1, vy1, vz1, T))
        vx2 = visVertices[v2index][0]
        vy2 = visVertices[v2index][1]
        vz2 = visVertices[v2index][2]
        propoint.append(fun(core, prosurface, vx2, vy2, vz2, T))
        vx3 = visVertices[v3index][0]
        vy3 = visVertices[v3index][1]
        vz3 = visVertices[v3index][2]
        propoint.append(fun(core, prosurface, vx3, vy3, vz3, T))

    point = np.array(propoint)
    tri = Delaunay(point)


    plt.triplot(point[:, 0], point[:, 1], tri.simplices.copy())
    plt.plot(point[:, 0], point[:, 1], 'o')
    plt.show()


    '''
    List = glGenLists(1)
    glNewList(List, GL_COMPILE)
    #glFrontFace(GL_CCW)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)
    for i in range(len(propoint)):
        glVertex3fv(propoint[i])
    glEnd()
    glEndList()
    return List
    '''

