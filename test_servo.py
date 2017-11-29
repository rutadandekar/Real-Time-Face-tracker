#!/usr/bin/python

import time
import numpy as np
import RPi.GPIO as GPIO
from Adafruit_PWM_Servo_Driver import PWM

en_pin = 27 #BCM_GPIO
x_dir_servo_ch = 3
y_dir_servo_ch = 4

servo_x_min = 150  # Min pulse length out of 4096
servo_x_max = 550  # Max pulse length out of 4096
servo_y_min = 300  # Min pulse length out of 4096
servo_y_max = 500  # Max pulse length out of 4096

GPIO.setmode(GPIO.BCM)
GPIO.setup(en_pin,GPIO.OUT)
GPIO.output(en_pin,GPIO.LOW)
pwm = PWM(0x40)
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

run = True
while (run==True):
  try:
    pwm.setPWM(x_dir_servo_ch, 0, servo_x_min)
    pwm.setPWM(y_dir_servo_ch, 0, servo_y_min)
    print 'tick'
    time.sleep(1)
    pwm.setPWM(x_dir_servo_ch, 0, servo_x_max)
    pwm.setPWM(y_dir_servo_ch, 0, servo_y_max)
    print 'tock'
    time.sleep(1)
  except KeyboardInterrupt:
    run=False
GPIO.cleanup()

