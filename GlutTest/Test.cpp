#include "ReadObj.h"

#define WINDOW_HEIGHT 480
#define WINDOW_WIDTH 640

//�����������ĳ�ʼ����
float G_fDistance = 1.5f;

//�������ת�Ƕ� 
float G_fAngle_horizon = 0.0;
float G_fAngle_vertical = 0.0f;

vector<GLfloat> center(3);

GLfloat xx = 0.0f;
GLfloat yy = 0.0f;
GLfloat zz = 0.0f;

//�趨�����ģ���Լ���ʾ�ķ�ʽ
bool redraw = true;
Objmodel *obj1 = new Objmodel();
string path = "obj/rubby.obj";

GLint mode1 = GL_LINE;
GLint mode2 = GL_TRIANGLES;

//light0����
GLfloat Vp0[] = { 0.0, 0.0, 0.0, 1.0 };	    //��Դ������λ��
GLfloat Va0[] = { 0.8, 0.8, 0.8, 1 };       //��Դ������ǿ������  
GLfloat Vd0[] = { 0.6, 0.6, 0.6, 1 };       //��Դɢ���ǿ������  
GLfloat Vs0[] = { 0.5, 0.5, 0.5, 1 };       //��Դ���淴���ǿ������  


////////////////////////////////////////////////
void myinit(void);
void myReshape(GLsizei w, GLsizei h);
void display(void);
void processSpecialKeys(int key, int x, int y);
void processNormalKeys(unsigned char key, int x, int y);



int main(int argc, char* argv[])
{
	glutInit(&argc, argv);

	cout << "����˵����" << endl;
	cout << "С����1��2��3��4�л�ģ��\n";
	cout << "����q(Q)��w(W)��e(E)�л�ģ����ʾ��ʽ\n";
	cout << "���̡�����������������ģ����ת\n";
	cout << "����a(A)�����ӵ��Զ��\n";

	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA);


	//�趨OPENGL����λ�úʹ�С
	glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT);
	glutInitWindowPosition(100, 100);
	glutCreateWindow("ReadObj");

	myinit();
	glutReshapeFunc(myReshape);
	glutSpecialFunc(processSpecialKeys);
	glutKeyboardFunc(processNormalKeys);
	glutDisplayFunc(display);

	glutMainLoop();

	return 0;
}


void myinit(void)
{
	glEnable(GL_DEPTH_TEST);   //������Ȳ���   ���������Զ���Զ����ر���ס��ͼ��

	glShadeModel(GL_SMOOTH);
	//glShadeModel(GL_FLAT);

	glEnable(GL_LIGHTING); 	  //���õ�Դ
	glEnable(GL_LIGHT0);      //����0�Ź�Դ

}

//ͼ�α����洰�ڳߴ�ı���仯
void myReshape(GLsizei w, GLsizei h)
{
	//�趨����
	glViewport(0, 0, w, h);

	//�趨͸�ӷ�ʽ
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(80.0, 1.0*(GLfloat)w / (GLfloat)h, 0.1, 3000.0);
}

void display(void)
{
	glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	//���ó�ģ�;���ģʽ
	glMatrixMode(GL_MODELVIEW);

	//���뵥λ������
	glLoadIdentity();

	//����������Z��ƽ��-G_fDistance (ʹ��������λ�������ǰ��)	//xx, yy, zz,
	/*gluLookAt(xx, yy, zz,
	0, 0, 0,
	0, 1, 0);*/
	glLightfv(GL_LIGHT0, GL_POSITION, Vp0);		//���ù�Դ��λ��
	glLightfv(GL_LIGHT0, GL_AMBIENT, Va0);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, Vd0);
	glLightfv(GL_LIGHT0, GL_SPECULAR, Vs0);
	glTranslatef(0.0, 0.0, -G_fDistance);
	//glScalef(0.3, 0.3, 0.3);
	//glutSolidTeacup(1);
	//��������

	if (redraw) {		//ֻ��һ�� 
		obj1->readFile(path);
		center = obj1->getCenter();
		redraw = false;
	}
	glTranslatef(-center[0], -center[1], -center[2]);
	//glTranslatef(0.0, 0.0, -center[2]);
	glRotatef(G_fAngle_horizon, 0.0f, 1.0f, 0.0f);
	glRotatef(G_fAngle_vertical, 1.0f, 0.0f, 0.0f);
	//glScalef(0.3, 0.3, 0.3);
	obj1->drawBox();
	obj1->showObj(mode1, mode2);	//����Ϊģ�͵���ʾ��ʽ  GL_POINTS	GL_LINES	GL_TRIANGLES

	//glLoadIdentity();

	//����ǰ�󻺳���
	glutSwapBuffers();
	//	glFlush();
}


void processSpecialKeys(int key, int x, int y)
{
	switch (key) {
	case GLUT_KEY_LEFT:
		G_fAngle_horizon -= 10.0f;
		break;
	case GLUT_KEY_RIGHT:
		G_fAngle_horizon += 10.0f;
		break;
	case GLUT_KEY_UP:
		G_fAngle_vertical -= 10.0f;
		break;
	case GLUT_KEY_DOWN:
		G_fAngle_vertical += 10.0f;
		break;
	}
	glutPostRedisplay();
}

void processNormalKeys(unsigned char key, int x, int y)
{
	switch (key) {
	case 97:	//"a"
		G_fDistance -= 2.0f;
		break;
	case 65:	//"A"
		G_fDistance += 2.0f;
		break;
	case 27:	//"Esc"
		exit(0);
	case '1':
		path = "obj/rubby.obj";
		redraw = true; obj1->~Objmodel(); obj1 = new Objmodel(); break;
	case '2':
		path = "obj/bird.obj";
		redraw = true; obj1->~Objmodel(); obj1 = new Objmodel(); break;
	case '3':
		path = "obj/torus.obj";
		redraw = true; obj1->~Objmodel(); obj1 = new Objmodel(); break;
	case '4':
		path = "obj/wan.obj";
		redraw = true; obj1->~Objmodel(); obj1 = new Objmodel(); break;
	case 'q':
	case 'Q':
		mode2 = GL_POINTS; break;
	case 'w':
	case 'W':
		mode2 = GL_TRIANGLES; mode1 = GL_LINE; break;
	case 'e':
	case 'E':
		mode1 = GL_FILL; mode2 = GL_TRIANGLES; break;
	}
	glutPostRedisplay();
}