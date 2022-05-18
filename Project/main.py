#!usr/bin/python
import cv2
import pipeline
import globals
import sys

globals.init()
cap=cv2.VideoCapture(sys.argv[1])
i=0
while(cap.isOpened()):
    i=i+1
    ret,frame=cap.read()
    if ret==1:
        #Call the pipeline in a single the captured frame from the video
        out_frame=pipeline.lane_finding_pipeline(frame,1)
        cv2.imshow("output",out_frame)
        if cv2.waitKey(1)&0xFF==ord('q'):
            break
    else:
        print("there's a problem in opening the video")
        break
if not cap.isOpened() :
    print("wrong path format")
