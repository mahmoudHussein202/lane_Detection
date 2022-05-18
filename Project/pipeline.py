
#import libraries
import numpy as np
import cv2
import binaryThreshold
import wrapper
import find_lane_pixels_using_histogram
import find_lane_pixels_using_prev_poly
import fit_poly
import measure_curvature_meters
import position_measurement
import project_lane_info
import globals


def lane_finding_pipeline(img,isDebug):
    #Step 1 use filters to extract the possible lines which can be the lane 
    binary_thresh = binaryThreshold.binary_thresholded(img)
    #Step 2 choose the part of the video that possibly we can find the lane 
    binary_warped, M_inv = wrapper.warp(binary_thresh)
    #out_img = np.dstack((binary_thresh, binary_thresh, binary_thresh))*255
    """ cv2.imshow("wrap",binary_warped)
    cv2.waitKey(1) """
    #Step 3
    #Find Lane from the histogram if it is the first frame
    if (len(globals.left_fit_hist) == 0):
        project_lane_info.temp= np.zeros_like(img)
        
        #make a filter to elimiminate all pixels above the road
        for y in range(0, 720):
            for x in range(0, 1280):
                # threshold the pixel
                project_lane_info.temp[y, x] = 255 if y>500 else 0  

        #cv2.imshow("file",project_lane_info.temp)
       # cv2.waitKey(1)

        #return pixels that contain the lane
        leftx, lefty, rightx, righty = find_lane_pixels_using_histogram.find_lane_pixels_using_histogram(binary_warped)
        #print(binary_warped)
        
        #get a second order equation that fit the points of the lane
        left_fit, right_fit, left_fitx, right_fitx, ploty = fit_poly.fit_poly(binary_warped,leftx, lefty, rightx, righty)
        # Store fit in history
        globals.left_fit_hist = np.array(left_fit) 
        new_left_fit = np.array(left_fit)
        globals.left_fit_hist = np.vstack([globals.left_fit_hist, new_left_fit]) 
        #print(np.vstack([globals.left_fit_hist, new_left_fit]))

        globals.right_fit_hist = np.array(right_fit)
        new_right_fit = np.array(right_fit)
        globals.right_fit_hist = np.vstack([globals.right_fit_hist, new_right_fit])

    #Find Lane from the previous polynomial if it is not the first frame
    else:
        globals.prev_left_fit = [np.mean(globals.left_fit_hist[:,0]), np.mean(globals.left_fit_hist[:,1]), np.mean(globals.left_fit_hist[:,2])]
        globals.prev_right_fit = [np.mean(globals.right_fit_hist[:,0]), np.mean(globals.right_fit_hist[:,1]), np.mean(globals.right_fit_hist[:,2])]
        
        leftx, lefty, rightx, righty = find_lane_pixels_using_prev_poly.find_lane_pixels_using_prev_poly(binary_warped)
        if (len(lefty) == 0 or len(righty) == 0):
            leftx, lefty, rightx, righty = find_lane_pixels_using_histogram.find_lane_pixels_using_histogram(binary_warped)
      
        left_fit, right_fit, left_fitx, right_fitx, ploty = fit_poly.fit_poly(binary_warped,leftx, lefty, rightx, righty)
        
        
        # Add new values to history
        new_left_fit = np.array(left_fit)
        globals.left_fit_hist = np.vstack([globals.left_fit_hist, new_left_fit])
        new_right_fit = np.array(right_fit)
        globals.right_fit_hist = np.vstack([globals.right_fit_hist, new_right_fit])
        
        # Remove old values from history
        if (len(globals.left_fit_hist) > 10):
            globals.left_fit_hist = np.delete(globals.left_fit_hist, 0,0)
            globals.right_fit_hist = np.delete(globals.right_fit_hist, 0,0)
                                       
    left_curverad, right_curverad =  measure_curvature_meters.measure_curvature_meters(binary_warped, left_fitx, right_fitx, ploty)
    veh_pos = position_measurement.measure_position_meters(binary_warped, left_fit, right_fit) 
    out_img,new_warp = project_lane_info.project_lane_info(img, binary_warped, ploty, left_fitx, right_fitx, M_inv, left_curverad, right_curverad, veh_pos)

    if isDebug =="1":
        #Display the output with the pipeline
        binary_thresh[binary_thresh==1]=255
        binary_thresh=cv2.cvtColor(binary_thresh,cv2.COLOR_GRAY2BGR)
        binary_thresh=cv2.resize(binary_thresh,(0,0),None,1/3,1/3)

        binary_warped[binary_warped==1]=255
        binary_warped=cv2.cvtColor(binary_warped,cv2.COLOR_GRAY2BGR)
        binary_warped=cv2.resize(binary_warped,(0,0),None,1/3,1/3)


        new_warp=cv2.resize(new_warp,(0,0),None,1/3,1/3)
        
        out_img=cv2.resize(out_img,(0,0),None,2/3,1)
        temp_img=cv2.vconcat([binary_thresh,binary_warped,new_warp])
        concatenated_out=cv2.hconcat([out_img, temp_img])

        return concatenated_out
    else:
        return out_img