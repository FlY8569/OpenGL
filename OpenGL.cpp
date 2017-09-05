#include "stdafx.h"
#include <GL/glut.h>

GLfloat rotate_angle1 = 0.0;
GLfloat dSize = 0.3; //�������С
void myDisplay(void)
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glLoadIdentity();
	glRotatef(rotate_angle1, -0.3, 0.3, -0.3);
	glBegin(GL_QUADS);
	//��  
	glColor3f(0.0, 1.0, 0.0);  //��
	glNormal3d(0.0, 0.0, 1.0); //��
	glVertex3d(dSize, dSize, dSize);
	glVertex3d(-dSize, dSize, dSize);
	glVertex3d(-dSize, -dSize, dSize);
	glVertex3d(dSize, -dSize, dSize);
	//��  
	glColor3f(0.0, 0.0, 1.0);  //��
	glNormal3d(0.0, 0.0, -1.0);//��
	glVertex3d(dSize, dSize, -dSize);
	glVertex3d(-dSize, dSize, -dSize);
	glVertex3d(-dSize, -dSize, -dSize);
	glVertex3d(dSize, -dSize, -dSize);
	//ǰ  
	glColor3f(1.0, 0.0, 0.0); //��
	glNormal3d(1.0, 0.0, 0.0);//ǰ
	glVertex3d(dSize, dSize, dSize);
	glVertex3d(dSize, -dSize, dSize);
	glVertex3d(dSize, -dSize, -dSize);
	glVertex3d(dSize, dSize, -dSize);
	//��  
	glColor3f(0.0, 1.0, 1.0);  //��
	glNormal3d(-1.0, 0.0, 0.0);//��  
	glVertex3d(-dSize, dSize, dSize);
	glVertex3d(-dSize, dSize, -dSize);
	glVertex3d(-dSize, -dSize, -dSize);
	glVertex3d(-dSize, -dSize, dSize);
	//��  
	glColor3f(1.0, 0.0, 1.0);  //Ʒ��
	glNormal3d(0.0, -1.0, 0.0);//��  
	glVertex3d(dSize, -dSize, dSize);
	glVertex3d(dSize, -dSize, -dSize);
	glVertex3d(-dSize, -dSize, -dSize);
	glVertex3d(-dSize, -dSize, dSize);
	//��   
	glColor3f(1.0, 1.0, 0.0); //��
	glNormal3d(0.0, 1.0, 0.0);//��  
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
	Sleep(20);  //������ת�ٶ�
}

int main(int argc, char *argv[])
{
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE);
	glutInitWindowPosition(100, 100);
	glutInitWindowSize(400, 400);
	glutCreateWindow("��������תMODEL");
	glutDisplayFunc(&myDisplay);
	glutIdleFunc(&myIdle);
	glutMainLoop();
	return 0;
}
