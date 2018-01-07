//ʵ�ֶԱȶ�����  
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
		cout << "����ͼƬ����" << endl;
		return -1;
	}
	imshow("ԭʼͼƬ", srcImage);
	Mat dstImage(srcImage);
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
	int pixMax = 0, pixMin = 255;
	//����ͼ�����ص����ֵ����Сֵ  
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

	//���жԱȶ�����  
	for (int j = 0; j < rowsNum; j++)
	{
		pDataMat = dstImage.ptr<uchar>(j);
		for (int i = 0; i < colsNum; i++)
		{
			pDataMat[i] = (pDataMat[i] - pixMin) * 255 / (pixMax - pixMin);
		}
	}
	imshow("�Աȶ�������ͼ��", dstImage);
	waitKey();
	return 0;
}