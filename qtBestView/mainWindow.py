#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
主窗口类
初始化菜单栏，状态栏和中心布局
author: Flyuz
last edited: 2018.10
"""
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFormLayout
from PyQt5.QtWidgets import QPushButton, QAction, QLabel, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from qtBestView.objloader import *
from qtBestView.particle import *

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.labName = QLabel(self)
        self.bestView = QLabel(self)
        self.obj = None
        self.para = [0.0 for i in range(7)]
        self.setWindowTitle('3D场景最优视点选择')
        # self.setWindowIcon(QIcon('./png'))
        self.resize(720, 480)
        self.initUi()
        self.initStatusBar()
        self.initToolBar()

    def openFileSlot(self):
        self.file_name = QFileDialog.getOpenFileName(self, "请选择文件", "C:", "OBJ files(*.obj)")
        # 更新状态栏
        self.statusBar().showMessage('请设置参数')
        self.file_name = str(self.file_name[0])
        self.labName.setText(self.file_name)
        self.obj = OBJ(self.file_name, swapyz=False)
        #设置文件路径表编码格式
        self.file_name = self.file_name.encode("gbk")
        # 设置视点方向
        self.ren.GetActiveCamera().SetViewUp(0, 1, 0)
        # 设置视点位置
        self.ren.GetActiveCamera().SetPosition([4000, 0, 0])
        # vtk读取obj文件
        reader = vtk.vtkOBJReader()
        reader.SetFileName(self.file_name)
        reader.Update()
        # 将obj数据传入mapper
        self.mapper.SetInputConnection(reader.GetOutputPort())
        self.iren.Initialize()

    def helpSlot(self):
        QMessageBox.information(self, "Help", "3D场景最优视点选择软件 v1.0 \n作者：flyuz \n若有建议，请联系flyuz1010@gmail.com", QMessageBox.Ok)

    def initToolBar(self):
        #设置工具栏
        openAction = QAction(QIcon('./1.png'), '&打开文件', self)
        openAction.triggered.connect(self.openFileSlot)
        self.openBar = self.addToolBar('打开文件')
        self.openBar.addAction(openAction)

        helpAction = QAction(QIcon('./2.png'), '&帮助', self)
        helpAction.triggered.connect(self.helpSlot)
        self.helpBar = self.addToolBar('帮助')
        self.helpBar.addAction(helpAction)

    def initStatusBar(self):
        #设置状态栏
        self.statusBar()
        self.statusBar().showMessage('请选择文件')


    def initUi(self):
        #设置中心布局
        #外层为QHBoxLayout嵌套QFormLayout
        self.hwg = QWidget()
        self.fwg = QWidget()
        self.hlayout = QHBoxLayout()
        self.flayout = QFormLayout()
        #初始化参数设置区域
        lab4 = QLabel("权重设置")
        lab5 = QLabel("投影面积")
        self.lineEdit5 = QLineEdit()
        self.lineEdit5.setText("0.015")
        lab6 = QLabel("投影周长")
        self.lineEdit6 = QLineEdit()
        self.lineEdit6.setText("0.04")
        lab7 = QLabel("视点熵")
        self.lineEdit7 = QLineEdit()
        self.lineEdit7.setText("25")
        lab8 = QLabel("最大深度")
        self.lineEdit8 = QLineEdit()
        self.lineEdit8.setText("2")
        lab9 = QLabel("可见度")
        self.lineEdit9 = QLineEdit()
        self.lineEdit9.setText("2.5")
        lab10 = QLabel("体特征")
        self.lineEdit10 = QLineEdit()
        self.lineEdit10.setText("700")
        lab11 = QLabel("视点下降度")
        self.lineEdit11 = QLineEdit()
        self.lineEdit11.setText("1.5")
        self.pButton = QPushButton(self)
        self.pButton.setText("开始")
        #将控件添加到flayout
        self.flayout.addRow(lab4)
        self.flayout.addRow(lab5, self.lineEdit5)
        self.flayout.addRow(lab6, self.lineEdit6)
        self.flayout.addRow(lab7, self.lineEdit7)
        self.flayout.addRow(lab8, self.lineEdit8)
        self.flayout.addRow(lab9, self.lineEdit9)
        self.flayout.addRow(lab10, self.lineEdit10)
        self.flayout.addRow(lab11, self.lineEdit11)
        self.flayout.addRow(self.pButton)
        self.flayout.addRow(self.labName)
        self.flayout.addRow(self.bestView)

        #将flayout添加到中间QWidget
        self.fwg.setLayout(self.flayout)
        #设置vtk与qt的接口，初始一个vtk图形
        self.vtkWidget = QVTKRenderWindowInteractor()
        self.initVtk()
        self.hlayout.addWidget(self.vtkWidget)
        self.hlayout.addWidget(self.fwg)
        #设置两部分的比例为5:1
        self.hlayout.setStretchFactor(self.vtkWidget, 3)
        self.hlayout.setStretchFactor(self.fwg, 2)
        self.hwg.setLayout(self.hlayout)
        #将hwg放到主窗口的中心
        self.setCentralWidget(self.hwg)

        self.initAction()

    def initAction(self):
        self.pButton.clicked.connect(self.updateVtk)

    def initVtk(self):
        self.ren = vtk.vtkRenderer()
        # 设置背景颜色
        self.ren.GradientBackgroundOn()
        self.ren.SetBackground(0.1, 0.1, 0.1)
        self.ren.SetBackground2(0.7, 0.7, 0.7)

        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)
        # Create source
        source = vtk.vtkSphereSource()
        source.SetCenter(0, 0, 0)

        # Create a mapper
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(source.GetOutputPort())

        # Create an actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.ren.AddActor(self.actor)


    def updateVtk(self):

        #获取参数信息
        self.para[0] = float(self.lineEdit5.text())  # self.area
        self.para[1] = float(self.lineEdit6.text())  # self.cir
        self.para[2] = float(self.lineEdit7.text())  # self.shan
        self.para[3] = float(self.lineEdit8.text())  # self.dismin
        self.para[4] = float(self.lineEdit9.text())  # self.surfaceVisibility
        self.para[5] = float(self.lineEdit10.text())  # self.eyeVisibility
        self.para[6] = float(self.lineEdit11.text())  # self.eyeDown

        pso = particle(self.obj, self.para)
        self.statusBar().showMessage('正在运行中....')
        result = pso.process()

        # 设置视点位置
        R = 1000 * 4  # 视点球半径
        ja = result[0]
        jb = result[1]
        x = R * math.sin(ja) * math.cos(jb)
        y = R * math.sin(ja) * math.sin(jb)
        z = R * math.cos(ja)
        vpoint = [x, y, z]  # 视点
        self.bestView.setText(str(vpoint))
        # 设置视点位置
        self.ren.GetActiveCamera().SetPosition(vpoint)
        self.iren.Initialize()
        self.statusBar().showMessage('运行完成！')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = mainWindow()
    win.show()
    win.iren.Initialize()
    sys.exit(app.exec_())
