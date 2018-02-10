#include <time.h>
#include <string>
#include <vector>
#include <gl/glut.h>

//读取模型数据的相关操作  根据str中 KEY的数量来判断str中存储数据格式
int findKey(std::string str, char key);
int findKey(std::string str, std::string key);
//读取模型数据的相关操作  读取f中的索引信息
void getNum(std::string str, std::vector<int> &fv, std::vector<int> &fo);
void getNum(std::string str, std::vector<int> &fv, std::vector<int> &ft, std::vector<int> &fn);
void Swap(float *a, int i, int j);

int qsort(float *a, int begin, int end);

void randqsort(float *a, int begin, int n);

std::vector<GLfloat> vectorCross(std::vector<GLfloat> v1, std::vector<GLfloat> v2);