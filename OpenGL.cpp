
#include <GL/glut.h>

GLfloat rotate_angle1 = 0.0;
GLfloat dSize = 0.3; //立方体大小
void myDisplay(void)
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glLoadIdentity();
	glRotatef(rotate_angle1, -0.3, 0.3, -0.3);
	glBegin(GL_QUADS);
	//上  
	glColor3f(0.0, 1.0, 0.0);  //绿
	glNormal3d(0.0, 0.0, 1.0); //上
	glVertex3d(dSize, dSize, dSize);
	glVertex3d(-dSize, dSize, dSize);
	glVertex3d(-dSize, -dSize, dSize);
	glVertex3d(dSize, -dSize, dSize);
	//下  
	glColor3f(0.0, 0.0, 1.0);  //蓝
	glNormal3d(0.0, 0.0, -1.0);//下
	glVertex3d(dSize, dSize, -dSize);
	glVertex3d(-dSize, dSize, -dSize);
	glVertex3d(-dSize, -dSize, -dSize);
	glVertex3d(dSize, -dSize, -dSize);
	//前  
	glColor3f(1.0, 0.0, 0.0); //红
	glNormal3d(1.0, 0.0, 0.0);//前
	glVertex3d(dSize, dSize, dSize);
	glVertex3d(dSize, -dSize, dSize);
	glVertex3d(dSize, -dSize, -dSize);
	glVertex3d(dSize, dSize, -dSize);
	//后  
	glColor3f(0.0, 1.0, 1.0);  //青
	glNormal3d(-1.0, 0.0, 0.0);//后  
	glVertex3d(-dSize, dSize, dSize);
	glVertex3d(-dSize, dSize, -dSize);
	glVertex3d(-dSize, -dSize, -dSize);
	glVertex3d(-dSize, -dSize, dSize);
	//左  
	glColor3f(1.0, 0.0, 1.0);  //品红
	glNormal3d(0.0, -1.0, 0.0);//左  
	glVertex3d(dSize, -dSize, dSize);
	glVertex3d(dSize, -dSize, -dSize);
	glVertex3d(-dSize, -dSize, -dSize);
	glVertex3d(-dSize, -dSize, dSize);
	//右   
	glColor3f(1.0, 1.0, 0.0); //黄
	glNormal3d(0.0, 1.0, 0.0);//右  
	glVertex3d(dSize, dSize, dSize);
	glVertex3d(dSize, dSize, -dSize);
	glVertex3d(-dSize, dSize, -dSize);
	glVertex3d(-dSize, dSize, dSize);

	rotate_angle1 += 3;
	glEnd();
	glFlush();
	glutSwapBuffers();
}

void myIdle(void)
{
	myDisplay();
	Sleep(20);  //减慢旋转速度
}

int main(int argc, char *argv[])
{
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE);
	glutInitWindowPosition(100, 100);
	glutInitWindowSize(400, 400);
	glutCreateWindow("立方体旋转MODEL");
	glutDisplayFunc(&myDisplay);
	glutIdleFunc(&myIdle);
	glutMainLoop();
	return 0;
}
