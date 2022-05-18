import numpy as np
import cv2

###Description: Fit a second order polynomial to each line ###

def fit_poly(binary_warped,leftx, lefty, rightx, righty):
    ### Fit a second order polynomial to each with np.polyfit() ###
    left_fit = np.polyfit(lefty, leftx, 2) # معادلة درجة تانية لللاين الشمال
    right_fit = np.polyfit(righty, rightx, 2)   #معادلة درجة تانية لللاين اليمين
    # Generate x and y values for plotting
    ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] ) #هيعملي اراي بتبدأ من صفر و تخلص عند719 
    try:
        left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
        right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
    except TypeError:
        # Avoids an error if `left` and `right_fit` are still none or incorrect
        print('The function failed to fit a line!')
        left_fitx = 1*ploty**2 + 1*ploty
        right_fitx = 1*ploty**2 + 1*ploty
    
    """ image = np.zeros([720,1290])
    left_fitxx=(np.floor(left_fitx)).astype(int)
    left_fitxx[left_fitxx > 1280]=1280
    left_fitxx[left_fitxx < 0]=0


    right_fitxx=(np.floor(right_fitx)).astype(int)
    right_fitxx[right_fitxx > 1280]=1280  
    right_fitxx[right_fitxx < 0]=0


    image[ploty.astype(int),left_fitxx]=255
    image[ploty.astype(int),right_fitxx]=255
 
    cv2.imshow("leftx",image)
    cv2.waitKey(1) """ 


    return left_fit, right_fit, left_fitx, right_fitx, ploty

    #left_fit , right_fit : المعادلة المناسبة لللاين 
    #left_fitx , right_fit x : التعويض بتاع المعادلة و حطيتها في اراي 
    #ploty : y النقط بتاعت ال 
    #           من صفر لحد 719
