#include "opencv2\opencv.hpp"
#include "opencv2\imgproc\imgproc.hpp"
#include "opencv2\highgui\highgui.hpp"
#include "iostream"
using namespace cv;
int main() {
	VideoCapture capture(0);  //从摄像头读入视频
	Mat edges;
	while (1) {
		Mat frame, dstimage;
		Mat mapx, mapy;
		capture >> frame;
		imshow("initial loading video", frame);
		//waitKey(30);
		if (waitKey(1) == NULL) { break; }
		dstimage.create(frame.size(), frame.type());
		mapx.create(frame.size(), CV_32FC1);
		mapy.create(frame.size(), CV_32FC1);
		for (int j = 0; j < frame.rows; j++) {
			for (int i = 0; i < frame.cols; i++) {
				mapx.at<float>(j, i) = static_cast<float>(frame.cols - i);
				mapy.at<float>(j, i) = static_cast<float>(j);
			}
		}
		remap(frame, dstimage, mapx, mapy, CV_INTER_LINEAR, BORDER_CONSTANT, Scalar(0, 0, 0));
		cvtColor(dstimage, edges, COLOR_BGR2GRAY);
		blur( edges, edges, Size(7, 7));
		Canny( edges, edges, 3, 30, 3);
		imshow("new loading video", dstimage);
		imshow("edges of video", edges);
		if (waitKey(1) >= 0) break;
	}
	return 0;
}