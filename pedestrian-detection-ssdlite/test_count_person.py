'''
this one is for counting the persons for experiments.
'''

#import matplotlib
#matplotlib.use('Agg')
import cv2
from pedestrian_detection_ssdlite import api
from matplotlib import pyplot as plt
import os
import time

files = os.listdir('./test_img')

for file in files:
	img = cv2.imread('./test_img/'+file)
	t1 = time.time()
	bbox_list = api.get_person_bbox(img, thr=0.5)
	t2 = time.time()
	fps = 1 / (t2-t1)
	print(file + ':', len(bbox_list), 'fps:', fps)

	for i in bbox_list:
		cv2.rectangle(img, i[0], i[1], (125, 255, 51), thickness=2)

	plt.imshow(img[:, :, ::-1])
	plt.show()
