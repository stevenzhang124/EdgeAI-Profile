'''
profile the execution delay of detection model solely
'''


import requests
import cv2
from pedestrian_detection_ssdlite import api
import sys
import time





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

		i += 1
