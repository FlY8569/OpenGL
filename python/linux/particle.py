# -*- coding: utf-8 -*-
from linux.objloader import *
from linux.projectionAndShannon import *
from linux.visibleAndDis import *


class particle:
    def __init__(self):
        # 粒子树
        self.particle_num = 6
        # 迭代次数
        self.N = 30

        # 学习因子
        self.C = (1.4962, 1.4962)
        # 惯性因子
        self.w = 1.4
        # 最大速度
        self.Vmax = np.pi / 3
        # 角度范围
        self.Xmax = [np.pi, np.pi * 2]
        # 适应值
        self.fitness = np.zeros(self.particle_num)
        # OBJ
        self.obj = OBJ("./tea1000e.obj", swapyz=False)
        # 视点球半径
        self.R = 1000 * 2
        # 输出结果
        self.f = open('result.txt', 'w')
        self.data = open('data.txt', 'w')

        # 粒子的角度
        self.angle = np.zeros((self.particle_num, 2))
        # 粒子的位置
        self.point = np.zeros((self.particle_num, 3))
        # 粒子的头朝向
        self.head = np.zeros((self.particle_num, 3))
        # 局部最好位置
        self.pbest = np.zeros((self.particle_num, 2))
        # 全局最好位置
        self.gbest = np.zeros(2)
        # 粒子的速度
        self.V = np.zeros((self.particle_num, 2))
        # 全局最优位置对应的fitness
        self.gbest_fitness = -1

    def init(self):
        self.angle = np.array([[0, 0],  # 前方
                               [3.14, 0],  # 后方
                               [1.57, 1.57],  # 高处
                               [1.57, 3.14],  # 左方
                               [1.57, 0],  # 右方
                               [1.57, 4.7]])  # 下方
        self.pbest = self.angle.copy()
        for i in range(self.particle_num):
            self.point[i], self.head[i] = self.getpoint(self.angle[i], self.R)
            self.fitness[i] = self.calculateFitness(self.obj, self.point[i], self.head[i])
            self.V[i] = [np.random.rand() * self.Vmax, np.random.rand() * self.Vmax]

    def getpoint(self, angle, R):
        x = R * math.sin(angle[0]) * math.cos(angle[1])
        y = R * math.sin(angle[0]) * math.sin(angle[1])
        z = R * math.cos(angle[0])
        ViewPoint = [x, y, z]  # 视点位置
        t = R / math.cos(angle[0])
        if abs(z - t) < 0.0001:
            head = [-1, 0, 0]  # 头朝向
        else:
            head = [-x, -y, t - z]
        return ViewPoint, head

    def calculateFitness(self, obj, ViewPoint, head):
        a1 = VisibleAndDis(obj, ViewPoint)
        a2 = ProjectionAndShannon(obj, ViewPoint, head, a1.visface)
        fit = [0 for i in range(7)]

        fit[0] = a2.area / 1000000 * 15
        fit[1] = a2.cir / 10000 * 0.42
        fit[2] = a2.shan / 10 * 0.5
        fit[3] = a1.dismin / 1000 * 1.3
        fit[4] = a1.surfaceVisibility * 2.6
        fit[5] = a1.eyeVisibility * 670
        fit[6] = ViewPoint[2] / 1000
        self.f.write(
            "面积：" + str(fit[0]) + "周长：" + str(fit[1]) + "视点熵：" + str(fit[2]) + "距离：" + str(fit[3]) + "可见度：" + str(
                fit[4]) + "眼睛：" + str(fit[5]) + "下降度" + str(fit[6]) + "\n")
        self.data.write("v " + str(ViewPoint) + "\n" + "d " +str(fit[0]) + " " + str(fit[1]) + " " + str(fit[2]) + " " + str(fit[3]) + " " + str(
                fit[4]) + " " + str(fit[5]) + " " + str(fit[6]) + "\n")
        print("面积：" + str(fit[0]) + "周长：" + str(fit[1]) + "视点熵：" + str(fit[2]) + "距离：" + str(fit[3]) + "可见度：" + str(
            fit[4]) + "眼睛：" + str(fit[5]) + "下降度" + str(fit[6]) + "\n")
        newFitness = fit[0] + fit[1] + fit[2] + fit[3] + fit[4] + fit[5]
        return newFitness

    # 更新gbest_fitness
    def updateGbest(self):
        newfitness = -1
        index = 0
        for i in range(self.particle_num):
            if self.fitness[i] > newfitness:
                index = i
                newfitness = self.fitness[i]
        if newfitness > self.gbest_fitness:
            self.gbest = self.angle[index].copy()
            self.gbest_fitness = newfitness

    def updateV(self):
        for i in range(self.particle_num):
            v = self.w * self.V[i] + self.C[0] * np.random.rand() * (self.pbest[i] - self.angle[i]) + \
                self.C[1] * np.random.rand() * (self.gbest - self.angle[i])
            self.V[i] = v
        self.V[self.V > self.Vmax] = self.Vmax * np.random.rand()
        self.V[self.V < -self.Vmax] = -self.Vmax * np.random.rand()

    # 更新每个粒子的位置和pbest
    def updateX(self):
        for i in range(self.particle_num):
            for j in range(2):
                self.angle[i][j] = self.angle[i][j] + self.V[i][j]
                if self.angle[i][j] < 0 or self.angle[i][j] > self.Xmax[j]:
                    self.angle[i][j] = self.Xmax[j] * np.random.rand()
            self.point[i], self.head[i] = self.getpoint(self.angle[i], self.R)
            newFitness = self.calculateFitness(self.obj, self.point[i], self.head[i])
            if newFitness > self.fitness[i]:
                self.pbest[i] = self.angle[i].copy()
                self.fitness[i] = newFitness

    def process(self):
        n = 0
        self.init()
        self.updateGbest()
        while n < self.N:
            if (n == self.N / 2):
                self.init()
                self.updateGbest()
            self.updateV()
            self.updateX()
            self.updateGbest()
            n += 1
            self.w -= 0.01
            self.f.write(str(n) + "\n")
            self.f.write(str(self.gbest) + "\n")
            self.f.write(str(self.gbest_fitness) + "\n")
            self.f.write("----------\n")
            print(str(n) + "次已完成")
        self.f.close()
