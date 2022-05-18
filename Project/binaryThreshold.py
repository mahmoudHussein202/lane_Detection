from cv2 import bitwise_and
import numpy as np
import cv2

#Canny function to try to use it in Function 2
def canny(image):
    #1 convert to gray scale
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

    #2 apply gaussian blur
    blur=cv2.GaussianBlur(gray,(5,5),0)

    #3 apply the canny function to outline strong gradients
    canny=cv2.Canny(blur,50,150)

    return canny
###Function 2: Process Binary Thresholded Images ###

def binary_thresholded(img):
    # Transform image to gray scale
    gray_img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray_img",gray_img)
    # Apply sobel (derivative) in x direction, this is usefull to detect lines that tend to be vertical
    sobelx = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0)
    #cv2.imshow("sobelx",sobelx)
    abs_sobelx = np.absolute(sobelx)
    #cv2.imshow("abs_sobelx",abs_sobelx)
    # Scale result to 0-255
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
    #cv2.imshow("scaled_sobel",scaled_sobel)
    sx_binary = np.zeros_like(scaled_sobel)
    # Keep only derivative values that are in the margin of interest
    sx_binary[(scaled_sobel >= 30) & (scaled_sobel <= 255)] = 1
   

    #canny_img=canny(img)
    #sx_binary=np.zeros_like(canny_img)
    #sx_binary[(canny_img >= 30) & (canny_img <= 255)] = 1
    #sx_binary[sx_binary==1]=255
    #cv2.imshow("sx_binary",sx_binary)
    #cv2.waitKey(0)
  
    # Detect pixels that are white in the grayscale image
    white_binary = np.zeros_like(gray_img)
    white_binary[(gray_img > 200) & (gray_img <= 255)] = 1
    #cv2.imshow("white_binary",white_binary)

    # Convert image to HLS
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    # Convert image to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    H = hls[:,:,0]
    L=hls[:,:,1]
    S = hls[:,:,2]
    V=hsv[:,:,2]

    sat_binary = np.zeros_like(S)
    # Detect pixels that have a high saturation value
    sat_binary[(S > 90) & (S <= 255)] = 1

    hue_binary =  np.zeros_like(H)
    hue_binary[(H > 10)&(H<25)] = 1

    light_binary =  np.zeros_like(L)
    light_binary[(L>200)]=1

    v_binary=np.zeros_like(V)
    v_binary[(V>50)&(V<100)]=1


    # Try different combinations
    binary_1 = cv2.bitwise_or(sx_binary, white_binary)
    binary = cv2.bitwise_or(binary_1, sat_binary)
    binary2 = cv2.bitwise_or(binary, canny(img))
    """ mask = np.zeros_like(img)
    src = np.array([
        [220, 720], # bottom-left corner
        [300, 447], # top-left corner
        [1000, 447], # top-right corner
        [1125, 720] # bottom-right corner
    ])

    
    mask_x=cv2.fillPoly(mask, np.int_([src]), (0,255, 0))
    mask_xx=np.array(mask_x.nonzero()[0])
    mask_xy=np.array(mask_x.nonzero()[1])
    mask[mask_xx,mask_xy]=255 """

    #binary3=bitwise_and(binary2,mask)
    """ cv2.imshow("step1",binary*255)
    cv2.imshow("binary1",binary2*255)
    cv2.waitKey(1) """
    
    return binary
