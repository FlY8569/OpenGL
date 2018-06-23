from myBestView.objloader import *
from myBestView.eyeloader import *
from myBestView.a1 import *
from myBestView.a2 import *


class particle:
    def __init__(self):
        #粒子树
        self.particle_num = 5
        #迭代次数
        self.N = 20
        #学习因子
        self.C = (1.49445, 1.49445)
        #惯性因子
        self.w = 1.4
        #最大速度
        self.Vmax = np.pi * 2
        #角度范围
        self.Xmax = [np.pi, np.pi * 2]
        #适应值
        self.fitness = np.zeros(self.particle_num)
        #OBJ
        self.obj = OBJ("./rubby.obj", swapyz=False)
        self.eye = EYE("./rubbyEyes.obj", swapyz=False)
        # 视点球半径
        self.R = self.obj.bbox_half_r * 3

        # 粒子的角度
        self.angle = np.zeros((self.particle_num, 2))
        #粒子的位置
        self.point = np.zeros((self.particle_num, 3))
        #粒子的头朝向
        self.head = np.zeros((self.particle_num, 3))
        #局部最好位置
        self.pbest = np.zeros((self.particle_num, 2))
        #全局最好位置
        self.gbest = np.zeros(2)
        # 粒子的速度
        self.V = np.zeros((self.particle_num, 2))
        #全局最优位置对应的fitness
        self.gbest_fitness = -1

    def init(self):
        self.angle = np.array([[0, 0],
        [3.14,0],
        [1.57, 1.57],
        [1.57, 3.14],
        [1.57, 4.7]])
        self.pbest = self.angle.copy()
        for i in range(self.particle_num):
            #self.angle[i] = [np.random.rand() * self.Xmax[0], np.random.rand() * self.Xmax[1]]
            #self.pbest[i] = self.angle[i].copy()
            self.point[i],self.head[i] = self.getpoint(self.angle[i], self.R)
            self.fitness[i] = self.calculateFitness(self.obj, self.eye, self.point[i], self.head[i])
            self.V[i] = [np.random.rand() * self.Vmax, np.random.rand() * self.Vmax]
        print("初始化完成~")


    def getpoint(self, angle, R):
        x = R * math.sin(angle[0]) * math.cos(angle[1])
        y = R * math.sin(angle[0]) * math.sin(angle[1])
        z = R * math.cos(angle[0])
        vpoint = [x, y, z]  # 视点位置
        t = R / math.cos(angle[0])
        if abs(z - t) < 0.0001:
            head = [-1, 0, 0]  # 头朝向
        else:
            head = [-x, -y, t - z]
        return vpoint, head

    def calculateFitness(self, obj, eye, point, head):
        a1 = A1(obj, point, head)
        a2 = A2(obj, eye, point)
        print("面积：", a1.area, "周长：", a1.cir, "距离：", a2.dismin, "可见度：", a2.surfaceVisibility, "眼睛：", a2.eyeVisibility)
        newFitness = 0.42 * a1.area + 2.6 * a1.cir + 13 * a2.dismin + 15 * a2.surfaceVisibility + 670 * a2.eyeVisibility
        return newFitness

    #更新gbest_fitness
    def updateGbest(self):
        newfitness = -1
        index = 0
        for i in range(self.particle_num):
            if(self.fitness[i] > newfitness):
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
        self.V[self.V > self.Vmax] = self.Vmax
        self.V[self.V < -self.Vmax] = -self.Vmax

    #更新每个粒子的位置和pbest
    def updateX(self):
        for i in range(self.particle_num):
            for j in range(2):
                self.angle[i][j] = self.angle[i][j] + self.V[i][j]
                if self.angle[i][j] < 0 or self.angle[i][j] > self.Xmax[j]:
                    self.angle[i][j] = self.Xmax[j] * np.random.rand()
            self.point[i], self.head[i] = self.getpoint(self.angle[i], self.R)
            newFitness = self.calculateFitness(self.obj, self.eye, self.point[i], self.head[i])
            if newFitness > self.fitness[i]:
                self.pbest[i] = self.angle[i].copy()
                self.fitness[i] = newFitness

    def process(self):
        n = 0
        self.init()
        self.updateGbest()
        while n < self.N:
            self.updateV()
            self.updateX()
            self.updateGbest()
            n += 1
            print(n)
            print(self.gbest)
            print(self.gbest_fitness)
            print("----------")