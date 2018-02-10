#include "RObjFx.h"

/*--------------------------------------辅助函数-------------------------------------------*/
//读取模型数据的相关操作  根据str中 KEY的数量来判断str中存储数据格式
int findKey(std::string str, char key) {
	int value = 0;
	for (int i = 0; i < str.size(); i++) {
		if (str[i] == key)
			value++;
	}
	return value;
}
//重载
int findKey(std::string str, std::string key) {
	int value = 0;
	for (int i = 0; i < str.size() - 1; i++) {
		if (str[i] == key[0] && str[i + 1] == key[1]) {
			value++;
			i++;
		}
	}
	return value;
}

//读取模型数据的相关操作  读取f中的索引信息
void getNum(std::string str, std::vector<int> &fv, std::vector<int> &fo) {
	int num = 0;
	int det = 0;
	std::vector<int> ff(6);
	for (int i = 0; i < str.size() && det < 6; i++) {
		if (str[i] >= '0' && str[i] <= '9')
			num = num * 10 + str[i] - '0';
		else {
			if (num != 0) {
				ff[det] = num;
				det++;
				num = 0;
			}
		}
	}
	fv[0] = ff[0];	fv[1] = ff[2];	fv[2] = ff[4];
	fo[0] = ff[1];	fo[1] = ff[3];	fo[2] = ff[5];
}

//读取模型数据的相关操作  读取f中的索引信息	重载函数
void getNum(std::string str, std::vector<int> &fv, std::vector<int> &ft, std::vector<int> &fn) {
	int num = 0;
	int det = 0;
	std::vector<int> ff(9);
	for (int i = 0; i < str.size() && det < 9; i++) {
		if (str[i] >= '0' && str[i] <= '9')
			num = num * 10 + str[i] - '0';
		else {
			if (num != 0) {
				ff[det] = num;
				det++;
				num = 0;
			}
		}
	}
	fv[0] = ff[0];	fv[1] = ff[3];	fv[2] = ff[6];
	ft[0] = ff[1];	ft[1] = ff[4];	ft[2] = ff[7];
	fn[0] = ff[2];	fn[1] = ff[5];	fn[2] = ff[8];
}
//排序
//随机快速排序
void Swap(float *a, int i, int j) {
	float temp = a[i];
	a[i] = a[j];
	a[j] = temp;
}

int qsort(float *a, int begin, int end) {
	int i, j;
	i = begin - 1; j = begin;
	for (; j < end; j++)
	{
		if (a[j] <= a[end - 1])
			Swap(a, ++i, j);
	}
	return i;
}

void randqsort(float *a, int begin, int n) {
	while (begin >= n)
		return;
	srand((unsigned)time(NULL));
	int key = (begin + rand() % (n - begin));
	Swap(a, key, n - 1);
	int m = qsort(a, begin, n);
	randqsort(a, begin, m);
	randqsort(a, m + 1, n);
}

std::vector<GLfloat> vectorCross(std::vector<GLfloat> v1, std::vector<GLfloat> v2) {
	std::vector<GLfloat> result(3);
	result[0] = v1[1] * v2[2] - v1[2] * v2[1];
	result[1] = v1[2] * v2[0] - v1[0] * v2[2];
	result[2] = v1[0] * v2[1] - v1[1] * v2[1];
	return result;
}
