import cv2
import numpy as np

def get_cropped_image(frame, filePath):
	hsv_min = np.array([0, 250, 100],np.uint8)
	hsv_max = np.array([10, 255, 255],np.uint8)
	hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	frame_threshed = cv2.inRange(hsv_img, hsv_min, hsv_max)

	se = np.ones((1, 1), dtype='uint8')
	image_close = cv2.morphologyEx(frame_threshed, cv2.MORPH_CLOSE, se)

	ret,thresh = cv2.threshold(image_close, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	areaArray = []
	for i, c in enumerate(contours):
	    area = cv2.contourArea(c)
	    areaArray.append(area)

	sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
	largestcontour = sorteddata[0][1]

	x, y, w, h = cv2.boundingRect(largestcontour)

	cropped_img = frame[y+3:y+h-3,x+3:x+w-3]
	cv2.imwrite(filePath,cropped_img)

def frame_processing(frame):
	cv2.rectangle(frame, (250,100), (700, 475), (0, 0, 255), 2)
	cv2.putText(frame, "Press S to scan image", (10, 90), cv2.FONT_HERSHEY_TRIPLEX, 0.75, (0, 0, 255), 2)
	cv2.putText(frame, "& quit camera", (10, 115), cv2.FONT_HERSHEY_TRIPLEX, 0.75, (0, 0, 255), 2)
	cv2.putText(frame, "Press Q to quit camera", (10, 50), cv2.FONT_HERSHEY_TRIPLEX, 0.75, (0, 0, 255), 2)
	return frame

def get_image_by_webcam(filePath = "demo.jpg"):
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

	while(True):
		ret, frame = cap.read()
		frame = frame_processing(frame)
		try:
			cv2.imshow('preview',frame)
			if cv2.waitKey(1) & 0xFF == ord('s'):
				get_cropped_image(frame, filePath)
				break
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		except:
			raise Exception("THIS DEVICE DOES NOT HAVE CAMERA.")

	cap.release()
	cv2.destroyAllWindows()

	return filePath