import numpy as np
import cv2

global temp

###Description: Project Lane Delimitations Back on Image Plane and Add Text for Lane Info ###

def project_lane_info(img, binary_warped, ploty, left_fitx, right_fitx, M_inv, left_curverad, right_curverad, veh_pos):
    # Create an image to draw the lines on
    warp_zero = np.zeros_like(binary_warped).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

    # Recast the x and y points into usable format for cv2.fillPoly()
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])


    pts = np.hstack((pts_left, pts_right))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (255,255, 0))

    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    newwarp = cv2.warpPerspective(color_warp, M_inv, (img.shape[1], img.shape[0]))
    newwarp=newwarp&temp
    ####################3##################
    #cv2.imshow("newwarp",newwarp)
    #cv2.waitKey(0)
    ####################3##################

    # Combine the result with the original image
    out_img = cv2.addWeighted(img, 1, newwarp, 0.3, 0)

    cv2.putText(out_img,'Curve Radius [m]: '+str((left_curverad+right_curverad)/2)[:7],(15,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0),2,cv2.LINE_AA)
    cv2.putText(out_img,'Center Offset [m]: '+str(veh_pos)[:7],(15,90), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(0,0,0),2,cv2.LINE_AA)

    return out_img,newwarp
