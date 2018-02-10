#include"ReadObj.h"

//����
Objmodel::Objmodel() {
	v_num = 0;
	vt_num = 0;
	vn_num = 0;
	f_num = 0;
}
//����
Objmodel::~Objmodel() {
	v_num = 0;
	vt_num = 0;
	vn_num = 0;
	f_num = 0;
	vertex.clear();
	vertex_texture.clear();
	vertex_normal.clear();
	face_vertex.clear();
	face_normal.clear();
	face_texture.clear();
	face_normal.clear();
}

/*------------------------------------------�ຯ��--------------------------------------------*/
//���㷨��
void Objmodel::calculateNormal() {
	vector<vector<GLfloat>> rawNormal(v_num);
	for (int i = 0; i < v_num; i++)
		rawNormal[i].resize(3);
	vector<GLfloat> v1(3);
	vector<GLfloat> v2(3);
	vector<GLfloat> f_norm1(3);
	vector<GLfloat> f_norm2(3);
	vector<GLfloat> f_norm3(3);
	for (int i = 0; i < f_num; i++) {
		for (int j = 0; j < 3; j++) {
			v1[j] = vertex[face_vertex[i][1] - 1][j] - vertex[face_vertex[i][0] - 1][j];
			v2[j] = vertex[face_vertex[i][2] - 1][j] - vertex[face_vertex[i][1] - 1][j];
		}
		//���1
		f_norm1 = vectorCross(v1, v2);
		v1 = v2;
		for (int j = 0; j < 3; j++) {
			v2[j] = vertex[face_vertex[i][0] - 1][j] - vertex[face_vertex[i][2] - 1][j];
		}
		//���2
		f_norm2 = vectorCross(v1, v2);
		v1 = v2;
		for (int j = 0; j < 3; j++) {
			v2[j] = vertex[face_vertex[i][1] - 1][j] - vertex[face_vertex[i][0] - 1][j];
		}
		//���3
		f_norm3 = vectorCross(v1, v2);
		//���������������������ƽ��֮����Ϊÿ����ķ���
		for (int i = 0; i < 3; i++) {
			f_norm1[0] = (f_norm1[0] + f_norm2[0] + f_norm3[0]) / 3.0f;
			f_norm1[1] = (f_norm1[1] + f_norm2[1] + f_norm3[1]) / 3.0f;
			f_norm1[2] = (f_norm1[2] + f_norm2[2] + f_norm3[2]) / 3.0f;
		}

		for (int j = 0; j < 3; j++) {
			rawNormal[face_vertex[i][j] - 1] = f_norm1;
		}
		rawNormal[face_vertex[i][0] - 1] = f_norm3;	//������������������������ֱ���Ϊÿ����ķ���
		rawNormal[face_vertex[i][1] - 1] = f_norm1;
		rawNormal[face_vertex[i][2] - 1] = f_norm2;
	}
	vertex_normal = rawNormal;
}

//��ȡģ������
void Objmodel::readFile(string path) {
	string str;
	string message;
	ifstream infile;
	infile.open(path.c_str(), ios::in);		//������ķ�ʽ���ļ�
	if (!infile.is_open()) {
		cout << "�޷����ļ�" << endl;
		infile.close();
		return;
	}
	while (!infile.eof()) {
		getline(infile, message);		    //��˳���ȡ�ļ��е�ÿ����
		vector<GLfloat> a(3);

		if (message.size() == 0)
			continue;
		if (message[0] == '#')		                //��#��ͷ����ע��
			continue;
		else if (message[0] == 'v') {		        //��������
			if (message[1] == 't') {		        //��ͼ�����
				istringstream sin(message);
				sin >> str >> a[0] >> a[1] >> a[2];
				vertex_texture.push_back(a);	    //ѹ����ͼ����
				vt_num++;
			}
			else if (message[1] == 'n') {		     //������Ϣ
				istringstream sin(message);
				sin >> str >> a[0] >> a[1] >> a[2];
				vertex_normal.push_back(a);	         //ѹ�뷨������
				vn_num++;
			}
			else {
				istringstream sin(message);
				sin >> str >> a[0] >> a[1] >> a[2];
				vertex.push_back(a);	             //ѹ�붥������
				v_num++;
			}
		}
		else if (message[0] == 'f') {
			vector<int> fv(3);
			vector<int> fvn(3);
			vector<int> fvt(3);
			istringstream sin(message);
			if (findKey(message, '/') == 6) {		//  ��ʽΪV1/VT1/VN1 V2/VT2/VN2 V3/VT3/VN3
				getNum(message, fv, fvt, fvn);
				face_vertex.push_back(fv);
				face_texture.push_back(fvt);
				face_normal.push_back(fvn);
			}
			else if (findKey(message, '/') == 3) {		//��ʽΪ V1/T1 V2/T2 V3/T3
				sin >> str;	//f
				getNum(message, fv, fvt);
				face_vertex.push_back(fv);
				face_texture.push_back(fvt);
			}
			else if (findKey(message, '/') == 0) {		//��ʽΪ V1 V2 V3
				sin >> str;	//f
				sin >> fv[0] >> fv[1] >> fv[2];
				face_vertex.push_back(fv);
			}
			else if (findKey(message, "//") == 3) {		//��ʽΪ V1//N1 V2//N2 V3//N3
				getNum(message, fv, fvn);
				face_vertex.push_back(fv);
				face_normal.push_back(fvn);
			}
			f_num++;
		}
	}
	if (vertex_normal.size() == 0)
		calculateNormal();		//���㷨��
	infile.close();
}

//��ʾģ������
void Objmodel::showObj(GLint mode1, GLint mode2) {
	glPolygonMode(GL_FRONT_AND_BACK, mode1);  //�������������������model��ʽ���
	glBegin(mode2);
	for (int i = 0; i < f_num; i++)	//Ŀǰ���÷��򣬲��ӹ��գ�ֻ��Ϊ�˰Ѷ����ģ����ʾһ��
	{
		//glNormal3f(vertex_normal[face_normal[i][0] - 1][0], vertex_normal[face_normal[i][0] - 1][1], vertex_normal[face_normal[i][0] - 1][2]);
		glNormal3f(vertex_normal[face_vertex[i][0] - 1][0], vertex_normal[face_vertex[i][0] - 1][1], vertex_normal[face_vertex[i][0] - 1][2]);
		glVertex3f(vertex[face_vertex[i][0] - 1][0], vertex[face_vertex[i][0] - 1][1], vertex[face_vertex[i][0] - 1][2]);

		glNormal3f(vertex_normal[face_vertex[i][1] - 1][0], vertex_normal[face_vertex[i][1] - 1][1], vertex_normal[face_vertex[i][1] - 1][2]);
		glVertex3f(vertex[face_vertex[i][1] - 1][0], vertex[face_vertex[i][1] - 1][1], vertex[face_vertex[i][1] - 1][2]);

		glNormal3f(vertex_normal[face_vertex[i][2] - 1][0], vertex_normal[face_vertex[i][2] - 1][1], vertex_normal[face_vertex[i][2] - 1][2]);
		glVertex3f(vertex[face_vertex[i][2] - 1][0], vertex[face_vertex[i][2] - 1][1], vertex[face_vertex[i][2] - 1][2]);
	}
	glEnd();
}


//����obj��Χ������	��������ƽ�Ƶ�ԭ��
vector<GLfloat> Objmodel::getCenter(/*GLfloat &x,GLfloat &y,GLfloat &z*/) {

	GLfloat x_max, x_min, y_max, y_min, z_max, z_min, x_center, y_center, z_center, x_sum, y_sum, z_sum;
	/*x_max = x_min = vertex[0][0];
	y_max = y_min = vertex[0][1];
	z_max = z_min = vertex[0][2];*/
	x_max = x_min = y_max = y_min = z_max = z_min = 0.0f;
	float *x = new float[v_num];
	float *y = new float[v_num];
	float *z = new float[v_num];

	for (int i = 0; i < v_num; i++) {
		x[i] = vertex[i][0];
		y[i] = vertex[i][1];
		z[i] = vertex[i][2];
	}

	randqsort(x, 0, v_num);		//�������
	randqsort(y, 0, v_num);
	randqsort(z, 0, v_num);

	for (int i = 0; i < 10; i++) {			//ȡ��С10������ƽ����Ϊ��Сֵ
		x_min += x[i];
		y_min += y[i];
		z_min += z[i];
	}
	x_min /= 10; y_min /= 10; z_min /= 10;
	for (int i = v_num - 10; i < v_num; i++) {		//ȡ���10������ƽ����Ϊ���ֵ
		x_max += x[i];
		y_max += y[i];
		z_max += z[i];
	}
	x_max /= 10; y_max /= 10; z_max /= 10;

	x_center = (x_min + x_max) / 2.0;
	y_center = (y_min + y_max) / 2.0;
	z_center = (z_min + z_max) / 2.0;
	x_sum = fabs(x_max - x_min);
	y_sum = fabs(y_max - y_min);
	z_sum = fabs(z_max - z_min);


	one0fcatercorner.push_back(x_max);
	one0fcatercorner.push_back(y_max);
	one0fcatercorner.push_back(z_max);

	other0fcatercorner.push_back(x_min);
	other0fcatercorner.push_back(y_min);
	other0fcatercorner.push_back(z_min);

	center.push_back(x_center);
	center.push_back(y_center);
	if (((z_center <= 0.1f && z_center >= -0.1f) || z_min >= 0.0f) && (x_sum >= 2.0f || y_sum >= 2.0f))
		z_center += z_sum / 2 + y_sum / 2.0 * tan(60.0*AngleToRadion);
	center.push_back(z_center);

	delete[] x;
	delete[] y;
	delete[] z;
	return center;

}

////����ģ�͵İ�Χ��
void Objmodel::drawBox() {
	vector<GLfloat> v1 = one0fcatercorner;
	vector<GLfloat> v2 = other0fcatercorner;
	glColor3f(1.0f, 0.0f, 0.0f);
	glBegin(GL_LINE_LOOP);
	glVertex3f(v1[0], v1[1], v1[2]);
	glVertex3f(v1[0], v1[1], v2[2]);
	glVertex3f(v2[0], v1[1], v2[2]);
	glVertex3f(v2[0], v1[1], v1[2]);
	glEnd();

	glBegin(GL_LINE_LOOP);
	glVertex3f(v1[0], v1[1], v1[2]);
	glVertex3f(v1[0], v1[1], v2[2]);
	glVertex3f(v1[0], v2[1], v2[2]);
	glVertex3f(v1[0], v2[1], v1[2]);
	glEnd();

	glBegin(GL_LINE_LOOP);
	glVertex3f(v1[0], v1[1], v1[2]);
	glVertex3f(v2[0], v1[1], v1[2]);
	glVertex3f(v2[0], v2[1], v1[2]);
	glVertex3f(v1[0], v2[1], v1[2]);
	glEnd();

	glBegin(GL_LINE_LOOP);
	glVertex3f(v2[0], v2[1], v2[2]);
	glVertex3f(v2[0], v1[1], v2[2]);
	glVertex3f(v1[0], v1[1], v2[2]);
	glVertex3f(v1[0], v2[1], v2[2]);
	glEnd();

	glBegin(GL_LINE_LOOP);
	glVertex3f(v2[0], v2[1], v2[2]);
	glVertex3f(v2[0], v1[1], v2[2]);
	glVertex3f(v2[0], v1[1], v1[2]);
	glVertex3f(v2[0], v2[1], v1[2]);
	glEnd();

}