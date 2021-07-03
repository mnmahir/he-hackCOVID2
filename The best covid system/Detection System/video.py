import time
import cv2
import numpy
import imutils


cap = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

class camera:
    #Check if webcam is available or not
    if not cap.isOpened():
        raise IOError("Webcam not available")
    while True:
        ret, frame = cap.read()
        #Mirrors the input camera footage
        frame = cv2.flip(frame,1)
        
        faces = faceCascade.detectMultiScale(
            frame, #Source
            scaleFactor = 1.2, #This has a 20% scale factor which means that the model is thorough but works slower
            minNeighbors = 5, #Affect quality of detected faces. Higher value results in less detection but higher quality. 3-6
            minSize = (30, 30) #Minimum object size. (30, 30) is good for face detection
        )
        
        print("Found {0} faces!".format(len(faces)))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.imshow('Camera', frame)
    
        #Press 'q' to close the camera feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    
cap.release()
cv2.destroyAllWindows()