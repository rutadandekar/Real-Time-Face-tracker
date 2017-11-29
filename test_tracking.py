import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Load camera
cap = cv2.VideoCapture(0)

while(True):
    ret, img = cap.read()
    img = cv2.flip(img,0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #print faces
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow('img',img)
    cv2.waitKey(10)

# Exit closing all windows
cap.release()
cv2.destroyAllWindows()

