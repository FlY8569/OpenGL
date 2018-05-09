import sys
import pygame
from OpenGL.GLU import *
from pygame.constants import *
from readobj.objloader import *


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
    obj.create_gl_list()  #原图像列表
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # GL_POINT GL_LINE  GL_FILL
    drawmouse(obj.gl_list)

def drawmouse(list):
    clock = pygame.time.Clock()
    rx, ry = (0, 0)
    tx, ty = (0, 0)
    zpos = 5
    rotate = move = False
    while 1:
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4:
                    zpos = max(1, zpos - 1)
                elif e.button == 5:
                    zpos += 1
                elif e.button == 1:
                    rotate = True
                elif e.button == 3:
                    move = True
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    rotate = False
                elif e.button == 3:
                    move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rx += i
                    ry += j
                if move:
                    tx += i
                    ty -= j

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslate(tx / 20., ty / 20., - zpos)
        glRotate(ry / 5, 1, 0, 0)
        glRotate(rx / 5, 0, 0, 1)

        glCallList(list)
        pygame.display.flip()

if __name__ == '__main__':
    initWindow()
    display()
