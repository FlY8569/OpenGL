//实现对比度拉伸  
#include <iostream>  
#include <opencv2\core\core.hpp>  
#include <opencv2\highgui\highgui.hpp>  
#include <opencv2\imgproc\imgproc.hpp>  

using namespace cv;
using namespace std;

int main()
{
	Mat srcImage = imread("C:\\Users\\zhangfy\\source\\repos\\Opencv\\sh.jpg");
	if (!srcImage.data)
	{
		cout << "读入图片错误！" << endl;
		return -1;
	}
	imshow("原始图片", srcImage);
	Mat dstImage(srcImage);
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
	int pixMax = 0, pixMin = 255;
	//计算图像像素的最大值和最小值  
	for (int j = 0; j < rowsNum; j++)
	{
		pDataMat = dstImage.ptr<uchar>(j);
		for (int i = 0; i < colsNum; i++)
		{
			if (pDataMat[i]>pixMax)
				pixMax = pDataMat[i];
			if (pDataMat[i] < pixMin)
				pixMin = pDataMat[i];
		}
	}

	//进行对比度拉伸  
	for (int j = 0; j < rowsNum; j++)
	{
		pDataMat = dstImage.ptr<uchar>(j);
		for (int i = 0; i < colsNum; i++)
		{
			pDataMat[i] = (pDataMat[i] - pixMin) * 255 / (pixMax - pixMin);
		}
	}
	imshow("对比度拉伸后的图像", dstImage);
	waitKey();
	return 0;
}