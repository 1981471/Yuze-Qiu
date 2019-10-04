#include <iostream> 
#include <fstream>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp> 
#include<opencv2/highgui/highgui.hpp> 
#include <opencv2/imgproc/imgproc.hpp>
#include <math.h>
using namespace cv;
using namespace std;
int main()
{
	Mat M1 = imread("C:\\Users\\apple\\Desktop\\test\\7.jpg");//载入原始图，且必须以二值图模式载入
	Mat M2,M;    cvtColor( M1, M2 , CV_BGR2GRAY);   threshold(M2, M, 100, 255, CV_THRESH_BINARY);
	imshow("原始图", M);    waitKey(5000); //等待5000ms后窗口自动关闭 //初始化结果图
	Mat dstImage = Mat::zeros(M.rows, M.cols, CV_8UC3);
	M = M<100;/*M提取阈值小于100的部分*/   imshow("阈值", M);//waitKey(50);
	vector<vector<Point>>contours;	vector<Vec4i>hierarchy;//定义轮廓和层次结构
	findContours(M, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_NONE);
	//迭代器输出/*for (vector<vector<Point>>::iterator it=contours.begin();it!=contours.end();++it){for (vector<Point>::iterator inner_it=it->begin();inner_it!=it->end();++inner_it){cout<<*inner_it<<endl;}}*/
	ofstream out("out.txt");	//下标输出
	out << "new output database" << endl;
	out << "   axis X        axis Y" << endl;
	for (int i = 0; i<contours.size(); i++)
	{   for (int j = 0; j<contours[i].size(); j++)
		{   out.open("out.txt", std::ios::out | std::ios::app);
			out <<setw(10)<<contours[i][j].x << setw(10)<< contours[i][j].y << endl;
			out.close();
			cout << contours[i][j].x << "	" << contours[i][j].y << endl; 
			//out.open("out.txt", std::ios::out | std::ios::app);out << setw(10) << contours[i][j].x << setw(10) << contours[i][j].y << endl;out.close(); 
			//ofstream f;f.open("C:\ Users \apple\Desktop\ 坐标轮廓线.txt", ios::out | ios::app);f << contours[i][j].x << "	" << contours[i][j].y << endl;
		}	cout << "datas of i ietation complete" << endl;}
	int index = 0;
	for (; index >= 0; index = hierarchy[index][0])
	{   Scalar color(rand() % 255, rand() % 255, rand() % 255);
		drawContours(dstImage, contours, index, color, 1, 8, hierarchy);/*遍历顶层轮廓，以随机颜色绘制出每个连接组件颜色*/}
	imshow("轮廓图", dstImage);
	waitKey(5000); //等待5000ms后窗口自动关闭   getchar();
}


