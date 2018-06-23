from OpenGL.GL import *
import numpy as np
class OBJ:
    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.area = 0   #总片面面积

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = [float(x) for x in values[1:4]]
                if swapyz:
                    v = v[2], v[0], v[1]
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
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append([face, norms, texcoords])

        self.create_bbox()
    def create_bbox(self):
        ps = np.array(self.vertices)
        vmin = ps.min(axis=0)
        vmax = ps.max(axis=0)
        self.bbox_center = ps.mean(axis=0)
        #self.bbox_center = (vmax + vmin) / 2
        self.bbox_half_r = np.max(vmax - vmin)  / 2


    def create_gl_list(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords = face

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glEndList()
