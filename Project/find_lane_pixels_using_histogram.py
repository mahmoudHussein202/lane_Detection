
import numpy as np
import cv2

def find_lane_pixels_using_histogram(binary_warped):
    """
    Detection of Lane Lines Using Histograms. 
    -----------------------------------------
    An image histogram is a graphical representation of the number of pixels in an image as a 
    function of their intensity. 
    ----------------------------------------
    Histograms are made up of bins, each bin representing a certain intensity value range.
    """

    # Take a histogram of the bottom half of the image
    histogram = np.sum(binary_warped[binary_warped.shape[0]//2:,:], axis=0)
    """cv2.imshow("file",binary_warped*255)
    cv2.imshow("file2",binary_warped[binary_warped.shape[0]//2:,:]*255)
    cv2.waitKey(1) """
   # histogram = histogram.reshape(1280,1)
    #print(histogram.shape)
    #print("---------------------------")
    
    # Find the peak of the left and right halves of the histogram
    # These will be the starting point for the left and right lines
    midpoint = np.int(histogram.shape[0]//2)
    #print(midpoint)
    leftx_base = np.argmax(histogram[:midpoint])
    #print(leftx_base)
    #print("---------------------------")
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint

    # Choose the number of sliding windows
    nwindows = 9
    # Set the width of the windows +/- margin
    margin = 100
    # Set minimum number of pixels found to recenter window
    minpix = 50

    # Set height of windows - based on nwindows above and image shape
    window_height = np.int(binary_warped.shape[0]//nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0]) #(مكانها في الصف) القيم الي جواها هي اماكن البيكسلز الي مش صفر #
    nonzerox = np.array(nonzero[1]) #(مكانها في العمود) القيم الي جواها هي اماكن البيكسلز الي مش صفر #
    # Current positions to be updated later for each window in nwindows
    leftx_current = leftx_base
    rightx_current = rightx_base

    # Create empty lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []

    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = binary_warped.shape[0] - (window+1)*window_height
        win_y_high = binary_warped.shape[0] - window*window_height
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        
        # Identify the nonzero pixels in x and y within the window #
        check_white_pixels_left = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
        (nonzerox >= win_xleft_low) &  (nonzerox < win_xleft_high)) #بالحركة دي هصفر كل الي برا الويندو الصغيرة الي شغال عليها 
        #print(nonzeroy.shape)
        good_left_inds= check_white_pixels_left.nonzero()[0] #اماكن الي مش زيرو بتاعت الاراي الي صفرت بيها الي مش عايزه
        #print(white_pixels_left.nonzero())
        #print("--------------------------------")
        #print(white_pixels_left.nonzero()[0])
        #print("--------------------------------")

        check_white_pixels_right = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
        (nonzerox >= win_xright_low) &  (nonzerox < win_xright_high))
        good_right_inds=check_white_pixels_right.nonzero()[0]
        
        # Append these indices to the lists
        left_lane_inds.append(good_left_inds)#كدا معايا ليست القيم الي جواها هي قيم اللين في الشمال و اليمين
        right_lane_inds.append(good_right_inds)
        
        # If you found > minpix pixels, recenter next window on their mean position
        if len(good_left_inds) > minpix:
            leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:        
            rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

    # Concatenate the arrays of indices (previously was a list of lists of pixels)
    try:
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)
    except ValueError:
        # Avoids an error if the above is not implemented fully
        pass

    # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]      #اماكن اللاين الشمال في الاكس
    lefty = nonzeroy[left_lane_inds]     # اماكن اللاين الشمال في الواي
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    """ image = np.zeros([720,1280])
    image[lefty,leftx]=255
    image[righty,rightx]=255
 
    cv2.imshow("leftx",image)
    cv2.waitKey(1) """

    return leftx, lefty, rightx, righty
    #الي طلعلي في الاخر هو اللين بتاعي 