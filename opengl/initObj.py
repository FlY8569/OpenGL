import sys
import pygame
from OpenGL.GLU import *
from pygame.constants import *
from opengl.objloader import *
from opengl.a1 import *
from opengl.a2 import *
from opengl.a3 import *

def initWindow():
    pygame.init()
    viewport = (800, 600)

    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

    glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION) #设置透视方式
    glLoadIdentity()  # 指定当前矩阵为单位矩阵

    width, height = viewport
    gluPerspective(90.0, width / float(height), 0.1, 1000.0)  #设置视区
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)


def display():
    obj = OBJ("./bird.obj", swapyz=False)
    obj.create_bbox()
    #obj.create_gl_list()
    #obj.getarea()
    vponit = [obj.bbox_center[0], obj.bbox_center[1] , obj.bbox_center[2]+2.0]
    head = [0,0,1]
    a1 = A1(obj,vponit, head)
    a1.drawDelaunay()
    #a1.getlenth()
    a2 = A2(obj, vponit)
    a2.getvisibleface()
    a3 = A3(obj, vponit, a1.area, a1.T, a2.visface)
    a3.getshannon()
    #a2.get_a2_list()
    #缓冲，让下次读入加快
    #with open("./bird.pkl", 'wb') as f:
    #    pickle.dump(obj, f)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # GL_POINT GL_LINE  GL_FILL
    clock = pygame.time.Clock()
    #drawmouse(obj.create_gl_list)
    # while True:
    #     clock.tick(300)
    #     for event in pygame.event.get():
    #         if event.type in (QUIT, KEYDOWN):
    #             sys.exit()
    #     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #     glLoadIdentity()
    #     gluLookAt(obj.bbox_center[0], obj.bbox_center[1], obj.bbox_center[2]+2.0,
    #               obj.bbox_center[0], obj.bbox_center[1], obj.bbox_center[2],
    #               0, 1, 0)
    #     glCallList(obj.create_gl_list())
    #     pygame.display.flip()

# def drawmouse(list):
#     clock = pygame.time.Clock()
#     rx, ry = (0, 0)
#     tx, ty = (0, 0)
#     zpos = 5
#     rotate = move = False
#     while 1:
#         clock.tick(30)
#         for e in pygame.event.get():
#             if e.type == QUIT:
#                 sys.exit()
#             elif e.type == KEYDOWN and e.key == K_ESCAPE:
#                 sys.exit()
#             elif e.type == MOUSEBUTTONDOWN:
#                 if e.button == 4:
#                     zpos = max(1, zpos - 1)
#                 elif e.button == 5:
#                     zpos += 1
#                 elif e.button == 1:
#                     rotate = True
#                 elif e.button == 3:
#                     move = True
#             elif e.type == MOUSEBUTTONUP:
#                 if e.button == 1:
#                     rotate = False
#                 elif e.button == 3:
#                     move = False
#             elif e.type == MOUSEMOTION:
#                 i, j = e.rel
#                 if rotate:
#                     rx += i
#                     ry += j
#                 if move:
#                     tx += i
#                     ty -= j
#
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#         glLoadIdentity()
#
#         glTranslate(tx / 20., ty / 20., - zpos)
#         glRotate(ry / 5, 1, 0, 0)
#         glRotate(rx / 5, 0, 0, 1)
#
#         glCallList(list)
#         pygame.display.flip()


