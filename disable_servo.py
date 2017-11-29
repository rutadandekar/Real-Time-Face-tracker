#!/usr/bin/python


#### Script to disable servos

import time
import RPi.GPIO as GPIO

en_pin = 27 #BCM_GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(en_pin,GPIO.OUT)
time.sleep(1)
GPIO.output(en_pin,GPIO.HIGH)

