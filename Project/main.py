#!usr/bin/python
#import libraries

import numpy as np
import cv2
#from moviepy.editor import VideoFileClip
import pipeline
import globals
import sys

globals.init()

workMode=input("please enter 0 for photo, 1 for video\n")
workMode=int(workMode)


if workMode ==1:
    locationVideo=input("please enter the complete path of the video\n")

    cap=cv2.VideoCapture(locationVideo)



    #fps=cap.get(cv2.CAP_PROP_FPS)
    #frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
    #height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )
    #frameSize = (int(width), int(height))




    #out = cv2.VideoWriter(location1,0x7634706d , fps, frameSize)

    #i=0
    while(cap.isOpened()):
        #i=i+1
        ret,frame=cap.read()
        if ret==1:
            #Call the pipeline in a single the captured frame from the video
            out_frame=pipeline.lane_finding_pipeline(frame,0)
            #out.write(out_frame)
            #print("Producing output video, ",int((i/frame_count)*100),"% completed.", end='\r')

            cv2.imshow("output",out_frame)
            if cv2.waitKey(10)==27:
             break
        else:
            print("Video has been Produced")
            break

    cap.release()
    #out.release()
    cv2.destroyAllWindows()

elif workMode ==0:
    locationPhoto=input("please enter the complete path of the photo\n")


    in_photo=cv2.imread(locationPhoto)
    out_photo=pipeline.lane_finding_pipeline(in_photo,1)
    cv2.imshow("output",out_photo)
    cv2.waitKey(0)



