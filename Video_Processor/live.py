# This script will detect faces via your webcam.
# Tested with OpenCV3
import os
import cv2
from PopUpDirections import addDirection
from DirectionIndicator import message_generator
#from gc_image_processor import *
import json 
import time

# Create the haar cascade
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
area_requirement = 0.15
min_x, min_y = 0.4, 0.4
use_gcloud = False

def process_frame(incoming_frame):
	frame = cv2.flip(incoming_frame, 1)
	# Our operations on the frame come here
	frame_height, frame_width = frame.shape[:2]
	center_x, center_y = int(frame_width/2), int(frame_height/2)
	start_time = time.time()
	faces = None
	if(use_gcloud):
		faces = get_face_coordinates(frame)
	else: 
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, 1.125, 5)
	emptyFrame = False
	if len(faces) ==0:
		emptyFrame = True
	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		relative_area = (w * h)/(frame_height * frame_width)
		face_x, face_y = int(x + w/2), int(y + h/2)
		x_distance, y_distance = ( center_x - face_x)/center_x, (center_y - face_y )/center_y
		#Complete left side or complete top : -1, Complete right side or complete bottom: +1 ?
		if(abs(x_distance) < min_x): 
			x_distance = 0
		if(abs(y_distance) < min_y): 
			y_distance = 0
		addDirection(frame,x_distance, y_distance)
		face_bounding_box = (x, y, w, h)
		message_generator(frame, face_bounding_box, relative_area)
	return frame, emptyFrame