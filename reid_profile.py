'''
profile the execution delay of reid model solely
'''

from reid import cam_reid
import time
import cv2

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

	#app.run(host='0.0.0.0', port=5002, debug=False, threaded = True)
	# img = cv2.imread('example.jpg')
	# detection = api.get_person_bbox(img, thr=0.5)

	detection_list = [
		[[(277, 2), (392, 320)]],
		[[(393, 9), (536, 315)], [(245, 17), (347, 313)]],
		[[(209, 13), (341, 368)], [(381, 4), (520, 360)], [(459, 9), (636, 369)]],
		[[(377, 63), (550, 373)], [(173, 4), (280, 368)], [(266, 0), (416, 367)], [(483, 42), (639, 372)]],
		[[(269, 10), (387, 477)], [(1, 11), (120, 477)], [(128, 33), (239, 474)], [(508, 25), (638, 480)], [(398, 14), (504, 471)]],
		[[(273, 4), (383, 231)], [(13, 6), (129, 231)], [(511, 15), (640, 235)], [(504, 260), (640, 478)], [(119, 12), (233, 238)], [(411, 0), (492, 251)]],
		[[(274, 4), (383, 231)], [(13, 7), (130, 231)], [(510, 14), (640, 249)], [(504, 260), (640, 479)], [(119, 11), (234, 238)], [(408, 248), (489, 480)], [(413, 3), (490, 242)]],
		[[(14, 6), (130, 229)], [(271, 3), (379, 236)], [(510, 14), (640, 258)], [(273, 253), (378, 478)], [(504, 260), (640, 479)], [(414, 248), (490, 480)], [(123, 12), (233, 237)], [(413, 3), (490, 243)]],
		[[(14, 6), (129, 230)], [(271, 3), (377, 250)], [(274, 249), (380, 479)], [(510, 14), (640, 258)], [(504, 260), (640, 478)], [(414, 248), (490, 480)], [(137, 253), (235, 479)], [(130, 10), (234, 238)], [(413, 3), (490, 243)]],
		[[(13, 4), (130, 228)], [(271, 3), (377, 251)], [(275, 249), (381, 478)], [(510, 14), (640, 258)], [(504, 260), (640, 478)], [(414, 248), (490, 480)], [(151, 251), (251, 476)], [(0, 255), (101, 470)], [(413, 3), (490, 243)], [(130, 9), (235, 247)]]
	]
	for i in range(len(detection_list)):
		file = 'edge' + str(i+1) + '.jpg'
		img = cv2.imread('./test_img/' +file)
		detection = detection_list[i]
		print(detection)
		t1 = time.time()
		reid_test(detection, img)
		t2 = time.time()
		t_tmp = t2-t1
		t_total.append(t_tmp)
		print('re-id' + file + 'consumes', t_tmp)