#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template, Response
import cv2
import time
import os
import sys
from pedestrian_detection_ssdlite import api

#workpath=os.path.dirname(sys.argv[0])
#os.chdir(workpath)          #指定py文件执行路径为当前工作路径

app = Flask(__name__)

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
	uri = "rtsp://admin:edge1234@192.168.1.116:554/cam/realmonitor?channel=1&subtype=1"
	cap = open_cam_rtsp(uri, 640, 480, 200)


	if not cap.isOpened():
		sys.exit('Failed to open camera!')

	counter=0
	counter2 = 0
	while(1):
		counter+=1
		#if counter % 12 !=0:
		#	print(counter)
		#	continue
		#print ("before read:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		if counter % 5 != 0:
			ret, frame = cap.read()
			#print ("after read", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			continue
		ret, frame = cap.read()
		detection_results = api.get_person_bbox(frame, thr=0.5)

		counter2 += 1
		for bb in detection_results:
			x1 = int(bb[0][0])
			y1 = int(bb[0][1])
			x2 = int(bb[1][0])
			y2 = int(bb[1][1])
			person = frame[y1:y2, x1:x2, :]
			#if counter2 % 6 != 0:
			savename=str('116' + str(counter2) +'.jpg')
			cv2.imwrite(savename, person)
			print("write one image", str(getnowtime()))
			frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
			

		(flag, outputFrame) = cv2.imencode(".jpg", frame)
		yield (b'--frame\r\n'
					   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(outputFrame) + b'\r\n')
		
		
@app.route('/video_feed')
def video_feed():
	#Video streaming route. Put this in the src attribute of an img tag
	return Response(main(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
	"""Video streaming home page."""
	return render_template('index.html')

if __name__ == '__main__':
	#plt.imshow(img[:, :,
	#plt.show()
	app.run(host='0.0.0.0', port='5000')
	#gen_frames()

