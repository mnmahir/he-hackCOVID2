from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os

# >MASTER METHOD
def goDetect(oriframe, bounding_box = True, print_info = False):
    # ======= DETECTION =======
    outframe,faces, has_mask, no_mask = detect_mask(oriframe, bounding_box)    # Face Detection: send original frame for detection
    # outframe = socdist_detect(oriframe, outframe, bounding_box)     # Social Distancing Detection: Use original frame for detection then append bounding box to previous frame
    # ======= DISPLAY INFO =======
    if print_info:
        print("Found {0} faces!".format(faces))

    return outframe, faces, has_mask, no_mask  # and other infos to put in gui


# >METHOD FOR FACE DETECTION (TO BE EXTENDED WITH MASK DETECTION)
prototxtPath = r"D:\Project\Face-Mask-Detection\face_detector\deploy.prototxt"
weightsPath = r"D:\Project\Face-Mask-Detection\face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
maskNet = load_model("D:\Project\Face-Mask-Detection\mask_detector.model")

def detect_mask(frame, bounding_box = True):
    # ======= FACE AND MASK DETECTION =======
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),(104.0, 177.0, 123.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()
    faces = []
    locs = []
    preds = []

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            faces.append(face)
            locs.append((startX, startY, endX, endY))

    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)


    # ======= BOUNDING BOX =======
    has_mask = 0
    no_mask = 0

    for (box, pred) in zip(locs, preds):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred
        if mask > withoutMask:
            has_mask += 1
            label = "Mask"
        else:
            no_mask += 1
            label = "No Mask"
        if bounding_box:
            color = (0, 255, 0) if label == "Mask" else (255, 0, 0)
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    return frame, len(faces), has_mask, no_mask



# >METHOD FOR SOCIAL DISTANCING DETECTION
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
def socdist_detect(oriframe, prevframe, bounding_box = True):

    (regions, _) = hog.detectMultiScale(oriframe, 
                                            winStride=(4, 4),
                                            padding=(8, 8),
                                            scale=1.03)

    if bounding_box:
        for (x, y, w, h) in regions:
                cv2.rectangle(prevframe, (x, y), 
                            (x + w, y + h), 
                            (255, 0, 0), 2)
    
    return prevframe