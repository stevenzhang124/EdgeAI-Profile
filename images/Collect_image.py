#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import time
import os
import sys

#workpath=os.path.dirname(sys.argv[0])
#os.chdir(workpath)          #指定py文件执行路径为当前工作路径

def getnowtime():
	mstime=int(1000*time.time())
	print(mstime)
	return mstime

def open_cam_rtsp(uri, width, height, latency):
	gst_str = ('rtspsrc location={} latency={} ! '
			   'rtph264depay ! h264parse ! omxh264dec ! '
			   'nvvidconv ! '
			   'video/x-raw, width=(int){}, height=(int){}, '
			   'format=(string)BGRx ! '
			   'videoconvert ! appsink').format(uri, latency, width, height)
	return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

def main():

	#uri = "rtsp://admin:admin@192.168.1.117:554/stream2"
	uri = "rtsp://admin:edge1234@192.168.1.115:554/cam/realmonitor?channel=1&subtype=1"
	cap = open_cam_rtsp(uri, 640, 480, 200)


	if not cap.isOpened():
		sys.exit('Failed to open camera!')

	counter=0
	while(1):
		#counter+=1
		#if counter % 12 !=0:
		#	print(counter)
		#	continue
		#print ("before read:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		#if counter % 10 != 0:
		#	ret, frame = cap.read()
			#print ("after read", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		#	continue
		ret, frame = cap.read()
		cv2.imshow('get', frame)
		key = cv2.waitKey(1) & 0xFF
		#cv2.waitKey()
		#savename=str(getnowtime())+'.jpg'
		#cv2.imwrite(savename,frame)
		if key == ord("s"):
			savename=str(getnowtime())+'.jpg'
			cv2.imwrite(savename,frame)
			print("write one image", str(getnowtime()))
		else:
			continue
		
		

if __name__=="__main__":
	main()
