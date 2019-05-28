from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import numpy as np

#optional argument
def nothing(x):
    pass
cap = cv2.VideoCapture(0)
cv2.namedWindow('image')
cv2.namedWindow('bars')

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (480, 360)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(480, 360))

switch2 = 'GAUSSIAN'
cv2.createTrackbar(switch2, 'bars', 0, 1, nothing)
switch3 = 'BOX'
cv2.createTrackbar(switch3, 'bars', 0, 1, nothing)
switch4 = 'MEDIAN'
cv2.createTrackbar(switch4, 'bars', 0, 1, nothing)
switch5 = 'BILATERAL'
cv2.createTrackbar(switch5, 'bars', 0, 1, nothing)

#easy assigments
hh='Hue High'
hl='Hue Low'
sh='Saturation High'
sl='Saturation Low'
vh='Value High'
vl='Value Low'

cv2.createTrackbar(hl, 'bars',0,179,nothing)
cv2.createTrackbar(hh, 'bars',0,179,nothing)
cv2.createTrackbar(sl, 'bars',0,255,nothing)
cv2.createTrackbar(sh, 'bars',0,255,nothing)
cv2.createTrackbar(vl, 'bars',0,255,nothing)
cv2.createTrackbar(vh, 'bars',0,255,nothing)

cv2.createTrackbar('erode', 'bars', 0, 20, nothing)
cv2.createTrackbar('dilate', 'bars', 0, 20, nothing)
cv2.createTrackbar('kernel', 'bars', 1, 20, nothing)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    #read trackbar positions for all
    hul=cv2.getTrackbarPos(hl, 'bars')
    huh=cv2.getTrackbarPos(hh, 'bars')
    sal=cv2.getTrackbarPos(sl, 'bars')
    sah=cv2.getTrackbarPos(sh, 'bars')
    val=cv2.getTrackbarPos(vl, 'bars')
    vah=cv2.getTrackbarPos(vh, 'bars')
    #make array for final values
    HSVLOW=np.array([hul,sal,val])
    HSVHIGH=np.array([huh,sah,vah])


    erodeIter = cv2.getTrackbarPos('erode', 'bars')
    dilateIter = cv2.getTrackbarPos('dilate', 'bars')
    kernel = cv2.getTrackbarPos('kernel', 'bars')

    gaussian = cv2.getTrackbarPos(switch2, 'bars')
    box = cv2.getTrackbarPos(switch3, 'bars')
    median = cv2.getTrackbarPos(switch4, 'bars')
    bilateral = cv2.getTrackbarPos(switch5, 'bars')

    if gaussian == 1:
        hsv = cv2.GaussianBlur(hsv, (kernel, kernel), 0)       
    if box == 1:
        hsv = cv2.blur(hsv, (kernel, kernel))
    if median == 1:
        hsv = cv2.medianBlur(hsv, kernel)
    if bilateral == 1:
        hsv = cv2.bilateralFilter(hsv, kernel, 75, 75)

    hsv = cv2.erode(hsv, None, iterations=erodeIter)
    hsv = cv2.dilate(hsv, None, iterations=dilateIter)

    #apply the range on a mask
    mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
    res = cv2.bitwise_and(image, image, mask = mask)

    # show the image to our screen
    cv2.imshow('image', res)
    cv2.imshow('original', image)
    # cv2.imshow("image", image)

    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
