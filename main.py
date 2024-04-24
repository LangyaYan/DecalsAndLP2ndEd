import numpy as np
from ultralytics import YOLO
import cv2

import util
#from sort.sort import *
from util import read_lp, write_csv

results = {}
#tracking the lp
#mot_tracker = Sort()

#load models
decal_lp = YOLO ('best.pt')

#load video
cap = cv2.VideoCapture('./testRun.mp4')

#lp class id
lp_id=[1]
#decal class id
decal_id=[0]


#read frames

frame_nmr=-1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if ret and frame_nmr <10:
        results[frame_nmr]={}
        #detect license plate
        detections = decal_lp(frame)[0]
        detect_lp = []
        detect_decal = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in lp_id:
                detect_lp.append([x1,y1,x2,y2,score])


            if int(class_id) in decal_id:
                detect_decal.append([x1,y1,x2,y2,score])

            #crop license plate
            lp_crop = frame[int(detect_lp[-1][1]):int(detect_lp[-1][3]),int(detect_lp[-1][0]):int(detect_lp[-1][2]),:]

            decal_crop = frame[int(detect_lp[-1][1]):int(detect_lp[-1][3]), int(detect_lp[-1][0]):int(detect_lp[-1][2]), :]

            #process license plate
            lp_crop_gray=cv2.cvtColor(lp_crop,cv2.COLOR_BGR2GRAY)
            _,lp_crop_thresh = cv2.threshold(lp_crop_gray,150,225,cv2.THRESH_BINARY_INV)
            lptext, lpscore = read_lp(lp_crop_thresh)
            car_id = lptext


            # process decal
            decal_crop_gray = cv2.cvtColor(decal_crop, cv2.COLOR_BGR2GRAY)
            _, decal_crop_thresh = cv2.threshold(decal_crop_gray, 150, 225, cv2.THRESH_BINARY_INV)
            dptext, dpscore = read_lp(decal_crop_thresh)

            if lptext is not None and dptext is not None:
                results[frame_nmr][car_id] ={'license_plate': {'lp_text': lptext,
                                                               'lp_score': detect_lp[-1][4],
                                                               'lp_text_score': lpscore},
                                             'decal':{'decal_text':dptext,
                                                      'decal_score':detect_lp[-1][4],
                                                      'decal_text_score':dpscore}}
#track lp
#track_ids=mot_tracker.update(np.array(detect_lp))

#assign an ID to the LP

#write results
write_csv(results,'./test.csv')
