'''
profile the execution delay of detection model and reid model when both the two mdoels are offloaded to the memory
'''


import requests
import cv2
from pedestrian_detection_ssdlite import api
import sys
import time
from reid import cam_reid


reid_mode = cam_reid.reid_model()
# encode origin image
compare = cam_reid.Compare(model=reid_mode, origin_img="./image/origin")
origin_f, origin_name = compare.encode_origin_image()


def reid_test(detection, frame):
	for z in detection:
		x1 = int(z[0][0])
		y1 = int(z[0][1])
		x2 = int(z[1][0])
		y2 = int(z[1][1])
		person = frame[y1:y2, x1:x2, :]
		identify_name, score = compare.run(person, origin_f, origin_name)
		if(identify_name in [ "MJ1", "MJ2", "MJ3", "MJ4", "MJ5"]):
			identify_name = "Person_1"
		elif(identify_name in ["QY1", "QY2", "QY3", "QY4", "QY5"]):
			identify_name = "Person_2"
		else:
			identify_name = "Unknown"
		print("identify name:{}, score:{}".format(identify_name, round(1-score, 2)))



if __name__ == '__main__':
	img = cv2.imread('example.jpg')
	detection = api.get_person_bbox(img, thr=0.5)
	# app.run(host='0.0.0.0', port=5001, debug=False, threaded = True)
	i = 0
	while(i < 10 ):
		file = 'edge' + str(i+1) + '.jpg'
		img = cv2.imread('./test_img/' +file)
		t1 = time.time()
		detection = api.get_person_bbox(img, thr=0.5)
		#print(detection)
		t2 = time.time()
		t_tmp = t2-t1
		print('detection' + file + 'consumes', t_tmp)


		t1 = time.time()
		reid_test(detection, img)
		t2 = time.time()
		t_tmp = t2-t1
		print('re-id' + file + 'consumes', t_tmp)


		i += 1
