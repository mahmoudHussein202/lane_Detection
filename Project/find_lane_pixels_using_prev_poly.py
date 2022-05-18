import numpy as np
import cv2
import globals

def find_lane_pixels_using_prev_poly(binary_warped):
    """
    Find lane pixels using the polynomial
    """


    # width of the margin around the previous polynomial to search
    margin = 100
    # Grab activated pixels
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])    
    ### Set the area of search based on activated x-values ###
    ### within the +/- margin of our polynomial function ###
    left_lane_inds = ((nonzerox > (globals.prev_left_fit[0]*(nonzeroy**2) + globals.prev_left_fit[1]*nonzeroy + 
                    globals.prev_left_fit[2] - margin)) & (nonzerox < (globals.prev_left_fit[0]*(nonzeroy**2) + 
                    globals.prev_left_fit[1]*nonzeroy + globals.prev_left_fit[2] + margin))).nonzero()[0]
    right_lane_inds = ((nonzerox > (globals.prev_right_fit[0]*(nonzeroy**2) + globals.prev_right_fit[1]*nonzeroy + 
                    globals.prev_right_fit[2] - margin)) & (nonzerox < (globals.prev_right_fit[0]*(nonzeroy**2) + 
                    globals.prev_right_fit[1]*nonzeroy + globals.prev_right_fit[2] + margin))).nonzero()[0]
    # Again, extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds] 
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    return leftx, lefty, rightx, righty
