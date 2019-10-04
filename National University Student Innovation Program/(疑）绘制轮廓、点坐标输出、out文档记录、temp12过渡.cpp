#include <iostream> 
#include <fstream>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp> 
#include<opencv2/highgui/highgui.hpp> 
#include <opencv2/imgproc/imgproc.hpp>
#include <math.h>
#include<stdio.h>
#include<stdlib.h>
#include <string>
#pragma once 
using namespace cv;
using namespace std;
int CountLines(string filename);
int main()
{
	//载入原始图，且必须以二值图模式载入
//	Mat M1 = imread("C:\\Users\\apple\\Desktop\\test\\字帖1.jpg");
	Mat M1 = imread("test\\字帖1.jpg");
	Mat M2,M;
	cvtColor( M1, M2 , CV_BGR2GRAY);
	threshold(M2, M, 100, 255, CV_THRESH_BINARY);
	imshow("原始图", M);
	//waitKey(5000); //等待5000ms后窗口自动关闭
				  //初始化结果图
	Mat dstImage = Mat::zeros(M.rows, M.cols, CV_8UC3);
	//M提取阈值小于250的部分
	M = M<250;
	imshow("阈值", M);
	//waitKey(50);
	//定义轮廓和层次结构
	vector<vector<Point>>contours;
	vector<Vec4i>hierarchy;
	findContours(M, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_NONE);
	//迭代器输出
	/*for (vector<vector<Point>>::iterator it=contours.begin();it!=contours.end();++it)
	{
	for (vector<Point>::iterator inner_it=it->begin();inner_it!=it->end();++inner_it)
	{
	cout<<*inner_it<<endl;
	}
	}
	*/
	//下标输出
	ofstream out("out.txt");
	out << "new output database" << endl;
	out << "   axis X        axis Y" << endl;
	for (int i = 0; i<contours.size(); i++)
	{
		for (int j = 0; j<contours[i].size(); j++)
		{
			out.open("out.txt", std::ios::out | std::ios::app);
			out <<setw(10)<<contours[i][j].x << setw(10)<< contours[i][j].y << endl;
			out.close();
			cout << contours[i][j].x << "	" << contours[i][j].y << endl; 
			//out.open("out.txt", std::ios::out | std::ios::app);out << setw(10) << contours[i][j].x << setw(10) << contours[i][j].y << endl;out.close(); 
			//ofstream f;f.open("C:\ Users \apple\Desktop\ 坐标轮廓线.txt", ios::out | ios::app);f << contours[i][j].x << "	" << contours[i][j].y << endl;
		}	cout << "datas of i ietation complete" << endl;
	}
	//遍历顶层轮廓，以随机颜色绘制出每个连接组件颜色
	int index = 0;
	for (; index >= 0; index = hierarchy[index][0])
	{
		Scalar color(rand() % 255, rand() % 255, rand() % 255);
		drawContours(dstImage, contours, index, color, 1, 8, hierarchy);
	}
	imshow("轮廓图", dstImage);
//	waitKey(5000); //等待5000ms后窗口自动关闭
	//getchar();
	FILE *fp1;
	char ch[60], ch1; int k = CountLines("out.txt") - 3; //if ((fp1 = fopen("temp12.txt", "w")) == NULL) {	printf("can't fopen this file!\n");	exit(0);}
	ofstream temp12("temp12.txt");	fp1 = fopen("temp12.txt", "w");
	cout << "normally create the temporary text" << endl;
	int i = 3,j=0;   //while ((ch = getchar()) != '#')	fputc(ch, fp1);	fclose(fp1);
	while (!feof(fp1))//文件未结束
	{   ifstream in("out.txt");int icount = 0;
		while (in.getline(ch, 60)) {
			icount++;
			if (icount == i&&icount<=k) {
//				cout << ch << endl; 
				break;
			}
		}
		temp12 << ch << endl;
		i = i + 100;
		if (ch == NULL||ch[0]=='\n'||i>k)break;
	}
	temp12.close();
	cout << "normally write in the temporary text" << endl;
	if ((fp1 = fopen("temp12.txt", "r")) == NULL) {
		printf("can't fopen this file!\n");
		exit(0);}
	while ((ch1 = fgetc(fp1)) != EOF)
		putchar(ch1);
	fclose(fp1);
	cout << "first part is ok!" << endl;
	waitKey(0);

}


int CountLines(string filename) {
	ifstream ReadFile;	
	int n = 0;	
	string tmp;	
	ReadFile.open(filename, ios::in);//ios::in 表示以只读的方式读取文件  
	if (ReadFile.fail())//文件打开失败:返回0  	
	{		
		return 0;	}	
	else//文件存在  	
	{		
		while (getline(ReadFile, tmp, '\n'))	{	
			n++;		}	
	ReadFile.close();		
	return n;	
	}
}



