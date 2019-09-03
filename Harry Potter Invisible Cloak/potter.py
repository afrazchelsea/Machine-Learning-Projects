# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 18:10:44 2019

@author: Afraz
"""

import numpy as np
import cv2
import time


print("Stupefy!")

cap = cv2.VideoCapture(0) # Capturing Video through Webcam

time.sleep(3) # Give time for Camera to settle and be stable 

background = 0


for i in range(60):

    ret, background = cap.read() # Capturing Static Background


# Flip the Image

background = np.flip(background, axis=1)

while(cap.isOpened()):
    
    ret, img = cap.read()

    if not ret:
        break


    img = np.flip(img, axis=1)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Converting from BGR to HSV
    
    lower_red = np.array([0, 120, 70]) # HSV Values Red= 0-10,170-180
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red) # Separating the cloak part

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red) # Everything except the cloak
    
    mask1 = mask1 + mask2 # Combining both masks 

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2) # MORPH_OPEN removes noise
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1) # For smoothness

    mask2 = cv2.bitwise_not(mask1) # Separate the cloak from the background

    res1 = cv2.bitwise_and(background, background, mask = mask1) # Used for segmentation of color
    res2 = cv2.bitwise_and(img, img, mask = mask2) # Used to substitute the cloak part (we super impose the two images)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) # Combining results

    cv2.imshow("You're a wizard, Harry!", final_output)
    k = cv2.waitKey(10)
    if k == 27:   # Triggered when escape-key is pressed and window shuts down
        break

cap.release()
cv2.destroyAllWindows()