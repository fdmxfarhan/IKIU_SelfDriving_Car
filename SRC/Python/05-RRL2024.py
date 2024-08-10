import cv2 
import numpy as np
import math
vid = cv2.VideoCapture(0) 
steer = 0

def getRightLine(x, y):
    foundRightLine = False
    while not foundRightLine:
        if x >= 640:
            # print('Not found!!')
            break
        if(frame_threshold[y][x] == 255):
            foundRightLine = True
        x += 1
    return x, y
def getLeftLine(x, y):
    foundLeftLine = False
    while not foundLeftLine:
        if x <= 0:
            # print('Not found!!')
            break
        if(frame_threshold[y][x] == 255):
            foundLeftLine = True
        x -= 1
    return x, y
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
while(True): 
    ret, image = vid.read() 
    frame_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # print(frame_HSV[int(480/2)][int(720/2)])
    frame_threshold = cv2.inRange(frame_HSV, (0, 0, 200), (180, 255, 255))
    height = len(frame_threshold)
    width = len(frame_threshold[0])

    rightLines = []
    leftLines = []
    for i in range(1, 160, 1):
        xR, yR = getRightLine(int(width/2), height - i)
        xL, yL = getLeftLine(int(width/2), height - i)
        d = distance([xR, yR], [xL, yL])
        if d < 640 - i*0.6:
            rightLines.append([xR, yR])
            leftLines.append([xL, yL])
            image = cv2.rectangle(image, (xR - 5, yR-5), (xR+5, yR+5), (255, 0, 0), 2) 
            image = cv2.rectangle(image, (xL - 5, yL-5), (xL+5, yL+5), (255, 0, 0), 2) 
    
    if len(rightLines) > 1:
        x1 = int((rightLines[0][0] + leftLines[0][0])/2)
        y1 = int((rightLines[0][1] + leftLines[0][1])/2)
        x2 = int((rightLines[len(rightLines) - 1][0] + leftLines[len(leftLines) - 1][0])/2)
        y2 = int((rightLines[len(rightLines) - 1][1] + leftLines[len(leftLines) - 1][1])/2)
        image = cv2.line(image, (x1, y1), (x2, y2), (0,255,0), 2) 
        steer = math.atan2((x1 - x2), (y1 - y2))
        print(math.degrees(steer))




    # contours0, hierarchy = cv2.findContours(frame_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # final_contours = []
    # for contour in contours0:
    #     area = cv2.contourArea(contour)
    #     if area > 100:
    #         final_contours.append(contour)
    # for i in range(len(final_contours)):
    #     cv2.drawContours(image, final_contours, i, (0,255,0), 3)
    
    # print(final_contours[0])
    
    cv2.imshow('image', image) 
    cv2.imshow('masked_image', frame_threshold) 
    if cv2.waitKey(1) & 0xFF == 27: 
        break
  
vid.release() 
cv2.destroyAllWindows() 