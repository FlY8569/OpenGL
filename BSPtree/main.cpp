#include <iostream>
#include <vector>
#include <time.h>
#include "bsp_tree.h"
#include "face.h"
using namespace std;

int main()
{
	BspTree<float> bspTree;

	//创造一些面片
	vector<Face<float>> face_vec;
	srand(time(0));
	for (int i = 0; i<16; ++i)
	{
		Face<float> face;
		for (int j = 0; j<3; ++j)
			face.point[j] = Point<float>(-200 + rand() % 400, -200 + rand() % 400, -200 + rand() % 400);
		face_vec.push_back(face);
	}
	//初始化bsp树并遍历
	bspTree.InitBspTree(face_vec, Point<float>(-200, -200, -200), Point<float>(200, 200, 200), 5);
	bspTree.TraverseBspTree();
	bspTree.DeleteBspTree();

	system("pause");
	return 0;
}
