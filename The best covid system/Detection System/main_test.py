import maskDetect
import socDistDetect
import video
import argparse
import time
import cv2
import numpy
import imutils

cap = cv2.VideoCapture(0)

#Check if webcame is available or not
if not cap.isOpened():
    raise IOError("Webcam not available")

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation = cv2.INTER_CUBIC)
    #Mirrors the input camera footage
    frame_flip = cv2.flip(frame,1)
    cv2.imshow('Camera', frame_flip)
    
    #Press 'q' to close the camera feed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
cap.release()
cv2.destroyAllWindows()