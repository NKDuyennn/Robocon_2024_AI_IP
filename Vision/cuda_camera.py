#      ▄▀▄     ▄▀▄
#     ▄█░░▀▀▀▀▀░░█▄
# ▄▄  █░░░░░░░░░░░█  ▄▄
# █▄▄█ █░░▀░░┬░░▀░░█ █▄▄█

###################################
##### Authors:  Hocj2me       #####
##### BK Galaxy Robotics      #####
##### Creation: 2024          #####
###################################

import numpy as np
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator  # ultralytics.yolo.utils.plotting is deprecated
from math import *
from test_control import *
# Load the YOLOv8 model
model = YOLO('ball_silo_detect.pt')

label_map = model.model.names
print(label_map)


cap = cv2.VideoCapture(2) 
cap.set(3, 640)
cap.set(4, 480)

while True:
    _, img = cap.read()
    
    # BGR to RGB conversion is performed under the hood
    # see: https://github.com/ultralytics/ultralytics/issues/2575
    results = model.predict(img)

    for r in results:
        
        annotator = Annotator(img)
        
        boxes = r.boxes
        if(len(boxes) < 1):
            stop()
        for box in boxes:
            
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            print(b)
            c = box.cls
            annotator.box_label(b, model.names[int(c)])

            
            x1, y1, x2, y2 = int(b[0]), int(b[1]), int(b[2]), int(b[3])
            if 'ball' not in model.names[int(c)]:
                continue

            pixelLenght = 680
            real_ball_height = 0.19
            focal_length = 0.4
            fov = 138
            NthPixel = (x2 + x1) // 2 
            image = cv2.circle(img, ((x2 + x1) // 2,(y2 + y1) // 2), radius=0, color=(0, 0, 255), thickness=3)

            distance = (real_ball_height * focal_length * 480) / (x2 - x1) 
            angle =    abs(pixelLenght/2 - NthPixel ) * fov  / pixelLenght
            if ((x2 + x1) // 2) < pixelLenght/2:
                angle = angle
            else:
                angle = -1 * angle

            print('Distance: ' + str(distance) + ' m')
            print('Angle y: ' + str(angle) + ' deg')
            if angle < -10:
                turnLeft()
            elif angle > -10:
                turnRight()
            elif(distance > 20):
                forword()
            else:
                stop()
            cv2.putText(img, '%.2f m' % distance, (x1, y1 + 75), 0, 0.7, (0, 255, 0), 2,
                            lineType=cv2.LINE_AA)
            cv2.putText(img, '%.2f deg' % angle, (x1, y1 + 50), 0, 0.7, (0, 255, 0), 2,
                        lineType=cv2.LINE_AA)
          
    img = annotator.result()  
    cv2.imshow('YOLO V8 Detection', img)     
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()
