#!/usr/bin/python
import numpy as np
import time
# Servo control
import RPi.GPIO as GPIO
from Adafruit_PWM_Servo_Driver import PWM
# Face tracking
import cv2

# Defines
FACE_CASCADE_CLASSIFIER = 'haarcascade_frontalface_default.xml'
VIDEO_DEVICE = 0
SERVO_ENABLE_PIN = 27 #BCM_GPIO
X_SERVO_CHANNEL = 3
Y_SERVO_CHANNEL = 4


class FaceTracker():
	def __init__(self, classifier_file='haarcascade_frontalface_default.xml', video_device=0):
		# Load the cascade classifiers to detect faces
		self.face_cascade = cv2.CascadeClassifier(classifier_file)
		# Load camera
		self.camera = cv2.VideoCapture(video_device)
		self.faces = None
		self.image = None

	def detect(self):
		ret, img = self.camera.read()
		if ret==False:
			print 'Failed to read from camera!'
			return None
		img = cv2.flip(img,0)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		self.faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
		self.image = img
		return self.faces

	def map_to_range(self,value,in_min,in_max,out_min,out_max):
		return ((value-in_min)*(out_max-out_min)/(in_max-in_min))+out_min

	def locate_face(self,face):
		h,w = self.image.shape[0],self.image.shape[1]
		face_x,face_y = face[0]+(face[2]/2),face[1]+(face[3]/2)
		face_x,face_y = self.map_to_range(face_x,0,w,-1.0,1.0),self.map_to_range(face_y,0,h,-1.0,1.0)
		return face_x,face_y

	def show(self):
		if self.image is not None:
			for (x,y,w,h) in self.faces:
				cv2.rectangle(self.image,(x,y),(x+w,y+h),(255,0,0),2)
			cv2.imshow('Face Tracker',self.image)
			cv2.waitKey(10)

	def __del__(self):
		self.camera.release()
		cv2.destroyAllWindows()


class ServoController():
	def __init__(self, enable_pin,x_servo_channel,y_servo_channel,servo_x_min=150,servo_x_max=550,servo_y_min=300,servo_y_max=500):
		self.en_pin = enable_pin
		self.x_dir_servo_ch = x_servo_channel
		self.y_dir_servo_ch = y_servo_channel
		# Max pulse lengths out of 4096
		self.servo_x_min = servo_x_min
		self.servo_x_max = servo_x_max
		self.servo_y_min = servo_y_min
		self.servo_y_max = servo_y_max
		# Enable the servos
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.en_pin,GPIO.OUT)
		GPIO.output(self.en_pin,GPIO.LOW)
		# Instantiate the pwm library
		self.pwm = PWM(0x40)
		self.pwm.setPWMFreq(60)
		# Initial positions of servos
		self.x = (self.servo_x_min+self.servo_x_min)/2
		self.y = (self.servo_y_min+self.servo_y_min)/2
		# Define controller constants
		self.KP = 12

	def constrain(self,value,min_value,max_value):
		return min(max_value,max(min_value,value))

	def offset_servos(self,error_x,error_y):
		self.x += self.KP*error_x
		self.y += self.KP*error_y
		self.x,self.y = int(self.constrain(self.x,self.servo_x_min,self.servo_x_max)),int(self.constrain(self.y,self.servo_y_min,self.servo_y_max))
		self.pwm.setPWM(self.x_dir_servo_ch, 0, self.x)
		self.pwm.setPWM(self.y_dir_servo_ch, 0, self.y)

	def __del__(self):
		GPIO.output(self.en_pin,GPIO.HIGH)
		time.sleep(1)
		GPIO.cleanup()

if __name__=='__main__':
	servo_controller = ServoController(SERVO_ENABLE_PIN, X_SERVO_CHANNEL, Y_SERVO_CHANNEL)
	detector = FaceTracker(FACE_CASCADE_CLASSIFIER,VIDEO_DEVICE)
	run = True
	while(run==True):
		try:
			faces = detector.detect()
			if len(faces)>0:
				loc = detector.locate_face(faces[0])
				servo_controller.offset_servos(loc[0],loc[1])
			detector.show()
		except KeyboardInterrupt:
			run=False
	del servo_controller
	del detector
