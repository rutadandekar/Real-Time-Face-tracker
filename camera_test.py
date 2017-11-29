import cv2
import numpy as np
import time
import picamera
import picamera.array

cv2.namedWindow('Image')
cap = cv2.VideoCapture(0)

while(1):
	ret, img = cap.read()
	cv2.imshow('Image',img)
	print 'step'
	cv2.waitKey(1000)
	
'''
with picamera.PiCamera() as camera:
	time.sleep(2)
	with picamera.array.PiRGBArray(camera) as stream:
		while(1):	
			camera.capture(stream, format='bgr')
			# At this point the image is available as stream.array
			image = stream.array
			cv2.imshow('Image',image)
			print 'step'
			cv2.waitKey(1000)
'''
