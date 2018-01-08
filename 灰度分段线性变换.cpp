#include <iostream>
#include <opencv2\core\core.hpp>
#include <opencv2\highgui\highgui.hpp>
#include <opencv2\imgproc\imgproc.hpp>

using namespace cv;
using namespace std;

Mat GrayTo(Mat srcI, int a, int b, int c, int d)
{
	Mat dstImage(srcI);
	int rowsNum = dstImage.rows;
	int colsNum = dstImage.cols;
	//ͼ���������ж�
	if (dstImage.isContinuous())
	{
		colsNum = colsNum * rowsNum;
		rowsNum = 1;
	}
	//ͼ��ָ�����
	uchar *pDataMat;
	//���жԱȶ�����
	for (int j = 0; j<rowsNum; j++)
	{
		pDataMat = dstImage.ptr<uchar>(j);
		for (int i = 0; i<colsNum; i++)
		{
			if (pDataMat[i] < a) {
				pDataMat[i] = pDataMat[i] * c / a;
			}
			else if (pDataMat[i] > b) {
				pDataMat[i] = (pDataMat[i] - b) * (255 - d) / (255 - b) + d;
			}
			else
				pDataMat[i] = (pDataMat[i] - a) * (d - c) / (b - a) + c;
		}
	}
	return dstImage;
}

int main()
{
	char fileName[100];
	cin >> fileName;
	Mat srcImage = imread(fileName, 0);

	if (!srcImage.data)
	{
		cout << "����ͼƬ����" << endl;
		return -1;
	}

	int a, b, c, d;
	cin >> a >> b >> c >> d;
	imshow("ԭʼͼƬ", srcImage);
	imshow("�Աȶ�������ͼ��", GrayTo(srcImage, a, b, c, d));
	waitKey(0);
	return 0;
}
