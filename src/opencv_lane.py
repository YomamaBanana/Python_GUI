import cv2
import matplotlib.pyplot as plt
import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
from matplotlib.colors import hsv_to_rgb


import cv2 # Import the OpenCV library to enable computer vision
import numpy as np
from numpy.lib.histograms import histogram # Import the NumPy scientific computing library
 
# Author: Addison Sears-Collins
# https://automaticaddison.com
# Description: A collection of methods to detect help with edge detection
# https://automaticaddison.com/the-ultimate-guide-to-real-time-lane-detection-using-opencv/
 
def binary_array(array, thresh, value=0):
  """
  Return a 2D binary array (mask) in which all pixels are either 0 or 1
     
  :param array: NumPy 2D array that we want to convert to binary values
  :param thresh: Values used for thresholding (inclusive)
  :param value: Output value when between the supplied threshold
  :return: Binary 2D array...
           number of rows x number of columns = 
           number of pixels from top to bottom x number of pixels from
             left to right 
  """
  if value == 0:
    # Create an array of ones with the same shape and type as 
    # the input 2D array.
    binary = np.ones_like(array) 
         
  else:
    # Creates an array of zeros with the same shape and type as 
    # the input 2D array.
    binary = np.zeros_like(array)  
    value = 1
 
  # If value == 0, make all values in binary equal to 0 if the 
  # corresponding value in the input array is between the threshold 
  # (inclusive). Otherwise, the value remains as 1. Therefore, the pixels 
  # with the high Sobel derivative values (i.e. sharp pixel intensity 
  # discontinuities) will have 0 in the corresponding cell of binary.
  binary[(array >= thresh[0]) & (array <= thresh[1])] = value
 
  return binary
 
def blur_gaussian(channel, ksize=3):
  """
  Implementation for Gaussian blur to reduce noise and detail in the image
     
  :param image: 2D or 3D array to be blurred
  :param ksize: Size of the small matrix (i.e. kernel) used to blur
                i.e. number of rows and number of columns
  :return: Blurred 2D image
  """
  return cv2.GaussianBlur(channel, (ksize, ksize), 0)
         
def mag_thresh(image, sobel_kernel=3, thresh=(0, 255)):
  """
  Implementation of Sobel edge detection
 
  :param image: 2D or 3D array to be blurred
  :param sobel_kernel: Size of the small matrix (i.e. kernel) 
                       i.e. number of rows and columns
  :return: Binary (black and white) 2D mask image
  """
  # Get the magnitude of the edges that are vertically aligned on the image
  sobelx = np.absolute(sobel(image, orient='x', sobel_kernel=sobel_kernel))
         
  # Get the magnitude of the edges that are horizontally aligned on the image
  sobely = np.absolute(sobel(image, orient='y', sobel_kernel=sobel_kernel))
 
  # Find areas of the image that have the strongest pixel intensity changes
  # in both the x and y directions. These have the strongest gradients and 
  # represent the strongest edges in the image (i.e. potential lane lines)
  # mag is a 2D array .. number of rows x number of columns = number of pixels
  # from top to bottom x number of pixels from left to right
  mag = np.sqrt(sobelx ** 2 + sobely ** 2)
 
  # Return a 2D array that contains 0s and 1s   
  return binary_array(mag, thresh)
 
def sobel(img_channel, orient='x', sobel_kernel=3):
  """
  Find edges that are aligned vertically and horizontally on the image
     
  :param img_channel: Channel from an image
  :param orient: Across which axis of the image are we detecting edges?
  :sobel_kernel: No. of rows and columns of the kernel (i.e. 3x3 small matrix)
  :return: Image with Sobel edge detection applied
  """
  # cv2.Sobel(input image, data type, prder of the derivative x, order of the
  # derivative y, small matrix used to calculate the derivative)
  if orient == 'x':
    # Will detect differences in pixel intensities going from 
        # left to right on the image (i.e. edges that are vertically aligned)
    sobel = cv2.Sobel(img_channel, cv2.CV_64F, 1, 0, sobel_kernel)
  if orient == 'y':
    # Will detect differences in pixel intensities going from 
    # top to bottom on the image (i.e. edges that are horizontally aligned)
    sobel = cv2.Sobel(img_channel, cv2.CV_64F, 0, 1, sobel_kernel)
 
  return sobel
 
def threshold(channel, thresh=(128,255), thresh_type=cv2.THRESH_BINARY):
  """
  Apply a threshold to the input channel
     
  :param channel: 2D array of the channel data of an image/video frame
  :param thresh: 2D tuple of min and max threshold values
  :param thresh_type: The technique of the threshold to apply
  :return: Two outputs are returned:
             ret: Threshold that was used
             thresholded_image: 2D thresholded data.
  """
  # If pixel intensity is greater than thresh[0], make that value
  # white (255), else set it to black (0)
  return cv2.threshold(channel, thresh[0], thresh[1], thresh_type)

img_path = r"C:/Users/Adrian/Desktop/Shinmei/lane_sample/rgb/2021-04-22-10-36-56_rgb_00020.png"

img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)

plt.show()

hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)


_, sxbinary = threshold(hls[:, :, 1], thresh=(100, 255))
sxbinary =blur_gaussian(sxbinary, ksize=3)
sxbinary = mag_thresh(sxbinary, sobel_kernel=3, thresh=(110, 255))
s_channel = hls[:, :, 2] # use only the saturation channel data
_, s_binary = threshold(s_channel, (80, 255))
_, r_thresh = threshold(img[:, :, 2], thresh=(120, 255))


      
rs_binary = cv2.bitwise_and(s_binary, r_thresh)
 

tmp = cv2.bitwise_or(rs_binary, sxbinary.astype(
                              np.uint8))  



hist = np.sum(tmp[int(tmp.shape[0]/2):,:], axis=0)

figure, (ax1, ax2) = plt.subplots(2,1) # 2 row, 1 columns
# figure.set_size_inches(10, 5)
ax1.imshow(tmp, cmap='gray')
ax1.set_title("Warped Binary Frame")
ax2.plot(hist)
ax2.set_title("Histogram Peaks")
plt.show()

plt.imshow(tmp)
plt.show()















exit()

hsv_nemo = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
# plt.imshow(hsv_nemo)

light_orange = (0, 24, 100)
dark_orange = (120, 255, 255)

lo_square = np.full((10, 10, 3), light_orange, dtype=np.uint8) / 255.0
do_square = np.full((10, 10, 3), dark_orange, dtype=np.uint8) / 255.0

plt.subplot(1, 2, 1)
plt.imshow(hsv_to_rgb(do_square))
plt.subplot(1, 2, 2)
plt.imshow(hsv_to_rgb(lo_square))

plt.show()

mask = cv2.inRange(hsv_nemo, light_orange, dark_orange)
result = cv2.bitwise_and(img, img, mask=mask)

plt.imshow(img)


plt.subplot(1, 2, 1)
plt.imshow(mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result)
# r, g, b = cv2.split(img)
# fig = plt.figure()
# axis = fig.add_subplot(1, 1, 1, projection="3d")

# pixel_colors = img.reshape((np.shape(img)[0]*np.shape(img)[1], 3))
# norm = colors.Normalize(vmin=-1.,vmax=1.)
# norm.autoscale(pixel_colors)
# pixel_colors = norm(pixel_colors).tolist()

# axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
# axis.set_xlabel("Red")
# axis.set_ylabel("Green")
# axis.set_zlabel("Blue")
plt.show()