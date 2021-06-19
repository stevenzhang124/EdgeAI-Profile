import requests
from flask import Flask, request
import cv2
from pedestrian_detection_ssdlite import api
import sys

app = Flask(__name__)



@app.route('/detection', methods=['POST'])
def detection():
	img = request.files["file"]
	img.save('a.jpg')
	image = cv2.imread('a.jpg')

	detection_test = api.get_person_bbox(image, thr=0.5)

	offload(url, detection_test, image)

def offload(url, detection_test, img):
	identify_num = 0
	persons = {}
	for bbox in detection_test:
		x1 = int(bbox[0][0])
		y1 = int(bbox[0][1])
		x2 = int(bbox[1][0])
		y2 = int(bbox[1][1])
		
		person_string = str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2)
		persons[str(identify_num)] = person_string
		identify_num += 1

	print(persons)
	file = {"file": ("file_name.jpg", cv2.imencode(".jpg", img)[1].tobytes(), "image/jpg")}
	info = requests.post(url, data=persons, files=file)


@app.route('/kill-detection', methods=['GET'])
def kill():
	sys.exit()




if __name__ == '__main__':

    app.run(port=5001, debug=True)