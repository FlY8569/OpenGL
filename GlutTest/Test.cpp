#include "ReadObj.h"

#define WINDOW_HEIGHT 480
#define WINDOW_WIDTH 640

//摄像机离物体的初始距离
float G_fDistance = 1.5f;

//物体的旋转角度 
float G_fAngle_horizon = 0.0;
float G_fAngle_vertical = 0.0f;

vector<GLfloat> center(3);

GLfloat xx = 0.0f;
GLfloat yy = 0.0f;
GLfloat zz = 0.0f;

//设定读入的模型以及显示的方式
bool redraw = true;
Objmodel *obj1 = new Objmodel();
string path = "obj/rubby.obj";

GLint mode1 = GL_LINE;
GLint mode2 = GL_TRIANGLES;

//light0参数
GLfloat Vp0[] = { 0.0, 0.0, 0.0, 1.0 };	    //光源环境光位置
GLfloat Va0[] = { 0.8, 0.8, 0.8, 1 };       //光源环境光强度数组  
GLfloat Vd0[] = { 0.6, 0.6, 0.6, 1 };       //光源散射光强度数组  
GLfloat Vs0[] = { 0.5, 0.5, 0.5, 1 };       //光源镜面反射光强度数组  


////////////////////////////////////////////////
void myinit(void);
void myReshape(GLsizei w, GLsizei h);
void display(void);
void processSpecialKeys(int key, int x, int y);
void processNormalKeys(unsigned char key, int x, int y);



int main(int argc, char* argv[])
{
	glutInit(&argc, argv);

	cout << "程序说明：" << endl;
	cout << "小键盘1、2、3、4切换模型\n";
	cout << "键盘q(Q)、w(W)、e(E)切换模型显示方式\n";
	cout << "键盘↑、↓、←、→控制模型旋转\n";
	cout << "键盘a(A)控制视点的远近\n";

	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA);


	//设定OPENGL窗口位置和大小
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
	glEnable(GL_DEPTH_TEST);   //启用深度测试   根据坐标的远近自动隐藏被遮住的图形

	glShadeModel(GL_SMOOTH);
	//glShadeModel(GL_FLAT);

	glEnable(GL_LIGHTING); 	  //启用灯源
	glEnable(GL_LIGHT0);      //启用0号光源

}

//图形比例随窗口尺寸改变而变化
void myReshape(GLsizei w, GLsizei h)
{
	//设定视区
	glViewport(0, 0, w, h);

	//设定透视方式
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(80.0, 1.0*(GLfloat)w / (GLfloat)h, 0.1, 3000.0);
}

void display(void)
{
	glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	//设置成模型矩阵模式
	glMatrixMode(GL_MODELVIEW);

	//载入单位化矩阵
	glLoadIdentity();

	//坐标中心向Z轴平移-G_fDistance (使坐标中心位于摄像机前方)	//xx, yy, zz,
	/*gluLookAt(xx, yy, zz,
	0, 0, 0,
	0, 1, 0);*/
	glLightfv(GL_LIGHT0, GL_POSITION, Vp0);		//设置光源的位置
	glLightfv(GL_LIGHT0, GL_AMBIENT, Va0);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, Vd0);
	glLightfv(GL_LIGHT0, GL_SPECULAR, Vs0);
	glTranslatef(0.0, 0.0, -G_fDistance);
	//glScalef(0.3, 0.3, 0.3);
	//glutSolidTeacup(1);
	//绘制物体

	if (redraw) {		//只读一遍 
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
	obj1->showObj(mode1, mode2);	//参数为模型的显示方式  GL_POINTS	GL_LINES	GL_TRIANGLES

	//glLoadIdentity();

	//交换前后缓冲区
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