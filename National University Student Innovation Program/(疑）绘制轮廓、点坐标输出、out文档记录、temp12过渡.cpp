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
	//����ԭʼͼ���ұ����Զ�ֵͼģʽ����
//	Mat M1 = imread("C:\\Users\\apple\\Desktop\\test\\����1.jpg");
	Mat M1 = imread("test\\����1.jpg");
	Mat M2,M;
	cvtColor( M1, M2 , CV_BGR2GRAY);
	threshold(M2, M, 100, 255, CV_THRESH_BINARY);
	imshow("ԭʼͼ", M);
	//waitKey(5000); //�ȴ�5000ms�󴰿��Զ��ر�
				  //��ʼ�����ͼ
	Mat dstImage = Mat::zeros(M.rows, M.cols, CV_8UC3);
	//M��ȡ��ֵС��250�Ĳ���
	M = M<250;
	imshow("��ֵ", M);
	//waitKey(50);
	//���������Ͳ�νṹ
	vector<vector<Point>>contours;
	vector<Vec4i>hierarchy;
	findContours(M, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_NONE);
	//���������
	/*for (vector<vector<Point>>::iterator it=contours.begin();it!=contours.end();++it)
	{
	for (vector<Point>::iterator inner_it=it->begin();inner_it!=it->end();++inner_it)
	{
	cout<<*inner_it<<endl;
	}
	}
	*/
	//�±����
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
			//ofstream f;f.open("C:\ Users \apple\Desktop\ ����������.txt", ios::out | ios::app);f << contours[i][j].x << "	" << contours[i][j].y << endl;
		}	cout << "datas of i ietation complete" << endl;
	}
	//���������������������ɫ���Ƴ�ÿ�����������ɫ
	int index = 0;
	for (; index >= 0; index = hierarchy[index][0])
	{
		Scalar color(rand() % 255, rand() % 255, rand() % 255);
		drawContours(dstImage, contours, index, color, 1, 8, hierarchy);
	}
	imshow("����ͼ", dstImage);
//	waitKey(5000); //�ȴ�5000ms�󴰿��Զ��ر�
	//getchar();
	FILE *fp1;
	char ch[60], ch1; int k = CountLines("out.txt") - 3; //if ((fp1 = fopen("temp12.txt", "w")) == NULL) {	printf("can't fopen this file!\n");	exit(0);}
	ofstream temp12("temp12.txt");	fp1 = fopen("temp12.txt", "w");
	cout << "normally create the temporary text" << endl;
	int i = 3,j=0;   //while ((ch = getchar()) != '#')	fputc(ch, fp1);	fclose(fp1);
	while (!feof(fp1))//�ļ�δ����
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
	ReadFile.open(filename, ios::in);//ios::in ��ʾ��ֻ���ķ�ʽ��ȡ�ļ�  
	if (ReadFile.fail())//�ļ���ʧ��:����0  	
	{		
		return 0;	}	
	else//�ļ�����  	
	{		
		while (getline(ReadFile, tmp, '\n'))	{	
			n++;		}	
	ReadFile.close();		
	return n;	
	}
}



