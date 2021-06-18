import requests
from flask import Flask, request
import cv2
#from pedestrian_detection_ssdlite import api
import json

def query():
	'''
	query the device parameters
	'''
	IP_list = ['127.0.0.1']
	infos = []
	for ip in IP_list:
		info = requests.get('http://' + ip + ':5000/get_status')
		infos.append(info.json())

	#return infos
	print(infos)

def decision():
	'''
	generate the offloading decisions
	'''
	pass

def message():
	'''
	send the control message to the edge devices
	'''
	pass


def offload():
	url = 'http://127.0.0.1:5000/reid'
	img = cv2.imread('example.jpg')
	#detection_test = api.get_person_bbox(img, thr=0.5)
	detection_test = [[(267, 62), (343, 270)], [(201, 65), (255, 227)], [(187, 64), (228, 169)], [(101, 73), (144, 202)]]
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
	

offload()

'''
identify_num = 0
	persons = {}
	persons_copy = {}
	for bbox in detection_test:
		x1 = int(bbox[0][0])
		y1 = int(bbox[0][1])
		x2 = int(bbox[1][0])
		y2 = int(bbox[1][1])
		person = img[y1:y2, x1:x2, :]
		persons_copy[identify_num] = person
		person_string = cv2.imencode('.jpg', person)[1].tobytes()
		persons[identify_num] = person_string
		identify_num += 1

	print(persons)
	#data = json.dumps(persons)
	content_type = 'image/jpeg'
	headers = {'content-type': content_type}
'''

