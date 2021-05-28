#import matplotlib
#matplotlib.use('Agg')
from flask import Flask, render_template, Response
import sys
import time
import logging
import subprocess
import cv2
from pedestrian_detection_ssdlite import api
from matplotlib import pyplot as plt

app = Flask(__name__)

logging.basicConfig(
	stream=sys.stdout,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	datefmt=' %I:%M:%S ',
	level="INFO"
)
logger = logging.getLogger('detector')

'''
def open_cam_onboard(width, height):
	# On versions of L4T prior to 28.1, add 'flip-method=2' into gst_str
	gst_str = ('nvcamerasrc ! '
			   'video/x-raw(memory:NVMM), '
			   'width=(int)2592, height=(int)1458, '
			   'format=(string)I420, framerate=(fraction)30/1 ! '
			   'nvvidconv ! '
			   'video/x-raw, width=(int){}, height=(int){}, '
			   'format=(string)BGRx ! '
			   'videoconvert ! appsink').format(width, height)
	return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
'''
def open_cam_onboard(width, height):
	gst_elements = str(subprocess.check_output('gst-inspect-1.0'))
	if 'nvcamerasrc' in gst_elements:
		# On versions of L4T prior to 28.1, add 'flip-method=2' into gst_str
		gst_str = ('nvcamerasrc ! '
				   'video/x-raw(memory:NVMM), '
				   'width=(int)2592, height=(int)1458, '
				   'format=(string)I420, framerate=(fraction)30/1 ! '
				   'nvvidconv ! '
				   'video/x-raw, width=(int){}, height=(int){}, '
				   'format=(string)BGRx ! '
				   'videoconvert ! appsink').format(width, height)
	elif 'nvarguscamerasrc' in gst_elements:
		gst_str = ('nvarguscamerasrc ! '
				   'video/x-raw(memory:NVMM), '
				   'width=(int)1920, height=(int)1080, '
				   'format=(string)NV12, framerate=(fraction)30/1 ! '
				   'nvvidconv flip-method=0 ! '
				   'video/x-raw, width=(int){}, height=(int){}, '
				   'format=(string)BGRx ! '
				   'videoconvert ! appsink').format(width, height)
	else:
		raise RuntimeError('onboard camera source not found!')
	return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)




def gen_frames():  # generate frame by frame from camera
	#stream detection
	cap = open_cam_onboard(640, 480)

	if not cap.isOpened():
		sys.exit('Failed to open camera!')

	# allow the camera to warmup
	time.sleep(0.1)
	frame_rate_calc = 1
	freq = cv2.getTickFrequency()

	while (cap.isOpened()):
		t1 = cv2.getTickCount()

		ret, frame = cap.read()

		logger.info("FPS: {0:.2f}".format(frame_rate_calc))
		cv2.putText(frame, "FPS: {0:.2f}".format(frame_rate_calc), (20, 20),
					cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2, cv2.LINE_AA)

		result = api.get_person_bbox(frame, thr=0.6)
		if len(result) == 2:
			cmd_1 = " curl -v -d 'nodeName=edge' 'http://192.168.1.101:5001/listen' "
			res = subprocess.Popen(cmd_1, shell=True)
			#res.terminate()
			#try:
    			#	sys.exit(0)
			#except:
    			#	print('die')
			#finally:
    			#	print('cleanup')
			sys.exit(0)
			#break

		for obj in result:
			logger.info('coordinates: {} {}. '.
						format(obj[0], obj[1]))

			cv2.rectangle(frame, obj[0], obj[1], (0, 255, 0), 2)
			#cv2.putText(frame, '{}: {:.2f}'.format(obj[3], obj[2]),
			#            (obj[0][0], obj[0][1] - 5),
			#            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

		# show the frame
		#cv2.imshow("Stream", frame)
		#key = cv2.waitKey(1) & 0xFF

		t2 = cv2.getTickCount()
		time1 = (t2 - t1) / freq
		frame_rate_calc = 1 / time1

		(flag, outputFrame) = cv2.imencode(".jpg", frame)
		yield (b'--frame\r\n'
					   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(outputFrame) + b'\r\n')
		

		# if the `q` key was pressed, break from the loop
		#if key == ord("q"):
			#break
	#sys.exit(0)

@app.route('/video_feed')
def video_feed():
	#Video streaming route. Put this in the src attribute of an img tag
	return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
	"""Video streaming home page."""
	return render_template('index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port='5000')
