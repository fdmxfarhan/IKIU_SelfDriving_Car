import cv2 
import numpy as np
vid = cv2.VideoCapture(0) 
  
while(True): 
    ret, image = vid.read() 
    frame_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # print(frame_HSV[int(480/2)][int(720/2)])
    frame_threshold = cv2.inRange(frame_HSV, (0, 0, 0), (180, 255, 110))
    contours0, hierarchy = cv2.findContours(frame_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    final_contours = []
    for contour in contours0:
        area = cv2.contourArea(contour)
        if area > 2000:
            final_contours.append(contour)
    for i in range(len(final_contours)):
        cv2.drawContours(image, final_contours, i, (0,255,0), 3)
    
    print(final_contours[0])
    
    cv2.imshow('image', image) 
    cv2.imshow('masked_image', frame_threshold) 
    if cv2.waitKey(1) & 0xFF == 27: 
        break
  
vid.release() 
cv2.destroyAllWindows() 