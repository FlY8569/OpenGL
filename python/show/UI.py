import sys
import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.constants import *
from show.objloader import *

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
        obj = OBJ("./tea1000e.obj", swapyz=False)

        R = 1000 * 2  # 视点球半径
        ja = 0.60868651
        jb = 2.7665885

        x = R * math.sin(ja) * math.cos(jb)
        y = R * math.sin(ja) * math.sin(jb)
        z = R * math.cos(ja)
        vpoint = [x, y, z]  # 视点
        print(vpoint)
        obj.create_gl_list()

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # GL_POINT GL_LINE  GL_FILL
        clock = pygame.time.Clock()
        #drawmouse(obj.create_gl_list)
        while True:
            clock.tick(300)
            for event in pygame.event.get():
                if event.type in (QUIT, KEYDOWN):
                    sys.exit()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            gluLookAt(vpoint[0], vpoint[1], vpoint[2],
                  0, 0, 0,
                  0, 1, 0)
                  #head[0], head[1], head[2])
            glCallList(obj.gl_list)
            pygame.display.flip()






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