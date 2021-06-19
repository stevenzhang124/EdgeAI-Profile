import requests
import subprocess
from flask import Flask, request
#from reid import cam_reid
import psutil  #pip3 install psutil
import GPUtil
import json
import numpy as np
import cv2

video_stream = []

app = Flask(__name__)

def open_cam_rtsp(uri, width, height, latency):
	gst_str = ('rtspsrc location={} latency={} ! '
			   'rtph264depay ! h264parse ! omxh264dec ! '
			   'nvvidconv ! '
			   'video/x-raw, width=(int){}, height=(int){}, '
			   'format=(string)BGRx ! '
			   'videoconvert ! appsink').format(uri, latency, width, height)
	return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


@app.route('/controller', methods=['GET', 'POST'])
def controller():
	global video_stream

	#parse the message from server
	messages = request.form.to_dict()

	if messages['url']:
		video_stream.append(messages['url'])

	if messages['kill-url']:
		video_stream.remove(messages['kill-url'])

	if messages['kill-detection']:
		info = requests.get('http://localhost:5001/kill-detection')

	if messages['kill-reid']:
		info = requests.get('http://localhost:5002/kill-reid')

	if messages['start-detection']:
		cmd = "python3 worker-detection.py"
		subprocess.Popen(cmd, shell=True)

	if messages['start-reid']:
		cmd = "python3 worker-reid.py"
		subprocess.Popen(cmd, shell=True)

	#send frames
	for uri in video_stream:
		read_video(uri)

	
def read_video(uri):
	#get the video ID
	#uri = "rtsp://admin:edge1234@192.168.1.108:554/cam/realmonitor?channel=1&subtype=1"
	cap = open_cam_rtsp(uri, 640, 480, 200)


	if not cap.isOpened():
		sys.exit('Failed to open camera!')


	counter=0
	while (cap.isOpened()):
		#t1 = cv2.getTickCount()
		counter+=1
		#if counter % 12 !=0:
		#	print(counter)
		#	continue
		
		if counter % 5 != 0:
			ret, frame = cap.read()
			continue
		break
	
	file = {"file": ("file_name.jpg", cv2.imencode(".jpg", frame)[1].tobytes(), "image/jpg")}
	info = requests.post('http://localhost:5001/kill-detection', files=file)
	


@app.route('/get_status', methods=['GET'])
def get_status():
	cpu_usage = psutil.cpu_percent()
	#print('available memory：%dM %fG'%(mem.available//M, mem.available/G))
	mem = psutil.virtual_memory()
	mem_usage = mem.available
	Gpus = GPUtil.getGPUs()
	for gpu in Gpus:
		gpu_usage = gpu.memoryUtil * 100

	info = {}
	info['node'] = '192.168.1.100'
	info['cpu_usage'] = cpu_usage
	info['mem_usage'] = mem_usage
	info['gpu_usage'] = gpu_usage

	print(info)

	return json.dumps(info)


if __name__ == '__main__':
    app.run(port=5000, debug=True)


