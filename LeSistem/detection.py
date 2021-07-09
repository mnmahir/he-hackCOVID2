import cv2

# >MASTER METHOD
def goDetect(oriframe, bounding_box = True, print_info = False):
    # ======= DETECTION =======
    outframe,faces = face_detect(oriframe, bounding_box)    # Face Detection: send original frame for detection
    # outframe, infos = socdist_detect(oriframe, outframe, bounding_box)     # Social Distancing Detection: Use original frame for detection then append bounding box to previous frame
    # ======= DISPLAY INFO =======
    if print_info:
        print("Found {0} faces!".format(faces))

    return outframe, faces  # and other infos to put in gui


# >METHOD FOR FACE DETECTION (TO BE EXTENDED WITH MASK DETECTION)
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
def face_detect(frame, bounding_box = True):
    faces = faceCascade.detectMultiScale(
        frame, #Source
        scaleFactor = 1.2, #This has a 20% scale factor which means that the model is thorough but works slower
        minNeighbors = 5, #Affect quality of detected faces. Higher value results in less detection but higher quality. 3-6
        minSize = (30, 30) #Minimum object size. (30, 30) is good for face detection
    )

    
    if bounding_box:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return frame, len(faces)



# >METHOD FOR SOCIAL DISTANCING DETECTION
def socdist_detect(oriframe, prevframe, bounding_box = True):
    pass