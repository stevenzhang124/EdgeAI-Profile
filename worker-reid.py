from flask import Flask, request
from reid import cam_reid

app = Flask(__name__)

reid_mode = cam_reid.reid_model()

# encode origin image
compare = cam_reid.Compare(model=reid_mode, origin_img="./image/origin")
origin_f, origin_name = compare.encode_origin_image()


	

@app.route('/reid', methods=['POST'])
def reid():
	#parse the request
	detection_test = request.form.to_dict()
	img = request.files["file"]
	img.save('a.jpg')
	image = cv2.imread('a.jpg')
	# dimensions = image.shape
	# print(dimensions)
	# cv2.imshow("Image", image)
	# cv2.waitKey (0)

	persons = {}
	for key, value in detection_test.items():
		locations = value.split(' ')
		x1 = int(locations[0])
		y1 = int(locations[1])
		x2 = int(locations[2])
		y2 = int(locations[3])
		person = image[y1:y2, x1:x2, :]
		persons[key] = person

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

@app.route('/kill-reid', methods=['GET'])
def kill():
	sys.exit()

if __name__ == '__main__':

    app.run(port=5002, debug=True)