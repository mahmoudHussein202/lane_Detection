#!usr/bin/python
#import libraries

import numpy as np
import cv2
#from moviepy.editor import VideoFileClip
import pipeline
import globals
import sys

globals.init()
deb=input("please enter 0 for final result, 1 for debugging mode\n")
deb=int(deb)
workMode=input("please enter 0 for photo, 1 for video\n")
workMode=int(workMode)
##selecting work mode photo=1 or video=0
#cap=cv2.VideoCapture("project_video.mp4")

#src_path=input("Enter the source video path: ")
#dstn_path=input("Enter the destination video path: ")
#isDebug=input("Enter 0 for no debbuged output video, 1 for debugged output video: ")
#locationVideo='E:\\4th Mechatronics\\2nd term\\image processing\\Project_data\\project_video.mp4'

#location1='E:\\4th Mechatronics\\2nd term\\image processing\\Project_data\\ppp_video.mp4'
#locationPhoto='E:\\4th Mechatronics\\2nd term\\image processing\\Project_data\\test_images\\test3.jpg'

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
            out_frame=pipeline.lane_finding_pipeline(frame,deb)
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
    out_photo=pipeline.lane_finding_pipeline(in_photo,deb)
    cv2.imshow("output",out_photo)
    cv2.waitKey(0)



#video_output = 'harder_challenge_video_output.mp4'
#clip1 = VideoFileClip("harder_challenge_video.mp4")
#output_clip = clip1.fl_image(lane_finding_pipeline)
#output_clip.write_videofile(video_output, audio=False)
