from flask import Flask, request
from reid import cam_reid
import psutil  #pip3 install psutil
import GPUtil

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
	#parse the message from server
	video_stream = []
	read_video()
	#new Thread
	pass

def read_video():
	#get the video ID
	uri = "rtsp://admin:edge1234@192.168.1.108:554/cam/realmonitor?channel=1&subtype=1"
	cap = open_cam_rtsp(uri, 640, 480, 200)


	if not cap.isOpened():
		sys.exit('Failed to open camera!')
	return cap

def get_frame(cap):

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
	
	return frame

def detect_person(frame):

	detection_results = api.get_person_bbox(frame, thr=0.5)

	#persons = []
	#for bbox in detection_results:
	#	x1 = int(bbox[0][0])
	#	y1 = int(bbox[0][1])
	#	x2 = int(bbox[1][0])
	#	y2 = int(bbox[1][1])

		#person = frame[y1:y2, x1:x2, :]
		#persons.append(person)

	#return detection_results, persons
	return detection_results, frame


@app.route('/reid', methods=['GET', 'POST'])
def server_inference(persons):
	#get the required parameters: cropped images
	print("get persons", len(persons))
	identify_names = {}
	for key, person in persons.items():
		identify_name, score = compare.run(person, origin_f, origin_name)
		if(identify_name in [ "MJ1", "MJ2", "MJ3", "MJ4", "MJ5"]):
			identify_name = "Person_1"
		elif(identify_name in ["QY1", "QY2", "QY3", "QY4", "QY5"]):
			identify_name = "Person_2"
		else:
			identify_name = "Unknown"
		print("identify name:{}, score:{}".format(identify_name, round(1-score, 2)))
		identify_names[key] = identify_name
		
	return identify_names


def offload():
	pass

@app.route('/get_status', methods=['GET'])
def get_status():
	cpu_usage = psutil.cpu_percent()
	#print('空闲内存：%dM %fG'%(mem.available//M, mem.available/G))
	mem = psutil.virtual_memory()
	mem_usage = mem.available
	Gpus = GPUtil.getGPUs()
	for gpu in Gpus:
		gpu_usage = gpu.memoryUtil * 100

	return cpu_usage, mem_usage, gpu_usage



