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
	//图像连续性判断
	if (dstImage.isContinuous())
	{
		colsNum = colsNum * rowsNum;
		rowsNum = 1;
	}
	//图像指针操作
	uchar *pDataMat;
	//进行对比度拉伸
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
		cout << "读入图片错误！" << endl;
		return -1;
	}

	int a, b, c, d;
	cin >> a >> b >> c >> d;
	imshow("原始图片", srcImage);
	imshow("对比度拉伸后的图像", GrayTo(srcImage, a, b, c, d));
	waitKey(0);
	return 0;
}
