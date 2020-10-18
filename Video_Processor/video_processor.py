# This script will detect faces via your webcam.
# Tested with OpenCV3
import os
import cv2
import json 

area_requirement = 0.15
min_x, min_y = 0.25, 0.25

cap = cv2.VideoCapture(0)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)
	# Our operations on the frame come here
	frame_height, frame_width = frame.shape[:2]
	center_x, center_y = int(frame_width/2), int(frame_height/2)
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, 1.1, 5)

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		relative_area = (w * h)/(frame_height * frame_width)
		if(relative_area > area_requirement):
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			face_x, face_y = int(x + w/2), int(y + h/2)
			x_distance, y_distance = (face_x - center_x)/center_x, (face_y - center_y)/center_y
			#Complete left side or complete top : -1, Complete right side or complete bottom: +1 ?
			if(abs(x_distance) < min_x): 
				x_distance = 0
			if(abs(y_distance) < min_y): 
				y_distance = 0

	# Display the resulting frame
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()