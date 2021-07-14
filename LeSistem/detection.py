from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os

from socdist import social_distancing_config as config
from socdist.detection import detect_people
from scipy.spatial import distance as dist


# >MASTER METHOD
def goDetect(oriframe, bounding_box = True, print_info = False):
    # faces, has_mask, no_mask, soc_dist_violate, total_people = 0,0,0,0,0
    # ======= DETECTION =======
    outframe,faces, has_mask, no_mask = detect_mask(oriframe, bounding_box)    # Face Detection: send original frame for detection
    outframe, soc_dist_violate, total_people = socdist_detect(oriframe, outframe, bounding_box)     # Social Distancing Detection: Use original frame for detection then append bounding box to previous frame
    # ======= DISPLAY INFO =======
    if print_info:
        print("Found {0} faces!".format(faces))

    return outframe, faces, has_mask, no_mask, soc_dist_violate, total_people  # and other infos to put in gui


# >METHOD FOR FACE DETECTION (TO BE EXTENDED WITH MASK DETECTION)
prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
maskNet = load_model("face_detector\mask_detector.model")

def detect_mask(frame, bounding_box = True):
    # ======= FACE AND MASK DETECTION =======
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),(104.0, 177.0, 123.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()
    print("detection123:",detections.shape)
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
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")
weightsPath = os.path.sep.join([config.MODEL_PATH, "yolo-fastest-1.1-xl.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolo-fastest-1.1-xl.cfg"])
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
if config.USE_GPU:
	# set CUDA as the preferable backend and target
	print("[INFO] setting preferable backend and target to CUDA...")
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def socdist_detect(oriframe, prevframe, bounding_box = True):
    results = detect_people(oriframe, net, ln, personIdx=LABELS.index("person"))
    violate = set()

    if len(results) >= 2:
        # extract all centroids from the results and compute the
        # Euclidean distances between all pairs of the centroids
        centroids = np.array([r[2] for r in results])
        D = dist.cdist(centroids, centroids, metric="euclidean")

        # loop over the upper triangular of the distance matrix
        for i in range(0, D.shape[0]):
            for j in range(i + 1, D.shape[1]):
                # check to see if the distance between any two
                # centroid pairs is less than the configured number
                # of pixels
                if D[i, j] < config.MIN_DISTANCE:
                    # update our violation set with the indexes of
                    # the centroid pairs
                    violate.add(i)
                    violate.add(j)

    # loop over the results
    for (i, (prob, bbox, centroid)) in enumerate(results):
        # extract the bounding box and centroid coordinates, then
        # initialize the color of the annotation
        (startX, startY, endX, endY) = bbox
        (cX, cY) = centroid
        color = (0, 102, 255)

        # if the index pair exists within the violation set, then
        # update the color
        if i in violate:
            color = (255, 153, 0)

        # draw (1) a bounding box around the person and (2) the
        # centroid coordinates of the person,
        cv2.rectangle(prevframe, (startX, startY), (endX, endY), color, 2)
        cv2.circle(prevframe, (cX, cY), 5, color, 1)


    return prevframe, len(violate), len(results)