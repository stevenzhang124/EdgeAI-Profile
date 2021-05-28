#import matplotlib
#matplotlib.use('Agg')
import sys
import time
import logging
import subprocess
import cv2
from pedestrian_detection_ssdlite import api
from matplotlib import pyplot as plt

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

img = cv2.imread('test_img/example.jpg')
bbox_list = api.get_person_bbox(img, thr=0.6)
print(bbox_list)

for i in bbox_list:
    cv2.rectangle(img, i[0], i[1], (125, 255, 51), thickness=2)

plt.imshow(img[:, :, ::-1])
plt.show()

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

    for obj in result:
        logger.info('coordinates: {} {}. '.
                    format(obj[0], obj[1]))

        cv2.rectangle(frame, obj[0], obj[1], (0, 255, 0), 2)
        #cv2.putText(frame, '{}: {:.2f}'.format(obj[3], obj[2]),
        #            (obj[0][0], obj[0][1] - 5),
        #            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    # show the frame
    cv2.imshow("Stream", frame)
    key = cv2.waitKey(1) & 0xFF

    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
