#include <time.h>
#include <string>
#include <vector>
#include <gl/glut.h>

//��ȡģ�����ݵ���ز���  ����str�� KEY���������ж�str�д洢���ݸ�ʽ
int findKey(std::string str, char key);
int findKey(std::string str, std::string key);
//��ȡģ�����ݵ���ز���  ��ȡf�е�������Ϣ
void getNum(std::string str, std::vector<int> &fv, std::vector<int> &fo);
void getNum(std::string str, std::vector<int> &fv, std::vector<int> &ft, std::vector<int> &fn);
void Swap(float *a, int i, int j);

int qsort(float *a, int begin, int end);

void randqsort(float *a, int begin, int n);

std::vector<GLfloat> vectorCross(std::vector<GLfloat> v1, std::vector<GLfloat> v2);