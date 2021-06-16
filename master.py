import requests
from flask import Flask, request
import cv2
from pedestrian_detection_ssdlite import api
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
	detection_test = api.get_person_bbox(img, thr=0.5)
	print(detection_test)
	identify_num = 0
	persons = {}
	for bbox in detection_test:
		x1 = int(bbox[0][0])
		y1 = int(bbox[0][1])
		x2 = int(bbox[1][0])
		y2 = int(bbox[1][1])
		person = img[y1:y2, x1:x2, :]
		persons[identify_num] = person
		identify_num += 1

	print(persons)
	data = json.dumps(persons)
	info = requests.post(url, data=data)

offload()


