# Lane Detection and Motion Planning Prototype

import cv2
import numpy as np


def detect_lanes(frame):
    # Preprocess the frame (grayscale, blur, edge detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Define region of interest (ROI)
    height, width = edges.shape
    roi_vertices = [(0, height), (width // 2, height // 2), (width, height)]
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, [np.array(roi_vertices)], 255)
    masked_edges = cv2.bitwise_and(edges, mask)

    # Detect lines using Hough Transform
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    # Calculate average slope and intercept for left and right lanes
    left_slope, left_intercept, right_slope, right_intercept = calculate_lane_params(lines)

    # Calculate midpoint (desired steering angle)
    midpoint_x = (left_intercept + right_intercept) // 2
    steering_angle = np.arctan(midpoint_x / height) * 180 / np.pi

    return steering_angle

def calculate_lane_params(lines):
    left_lines, right_lines = [], []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        if slope < 0:
            left_lines.append((slope, intercept))
        else:
            right_lines.append((slope, intercept))

    # Calculate average slope and intercept for left and right lanes
    left_slope, left_intercept = np.mean(left_lines, axis=0)
    right_slope, right_intercept = np.mean(left_lines, axis=0)#np.mean(right_lines, axis=0)

    return left_slope, left_intercept, right_slope, right_intercept

def main():
    cap = cv2.VideoCapture(0)  # Use the default camera (adjust if needed)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        steering_angle = detect_lanes(frame)

        # Send steering angle to Arduino
        # arduino.write(str(steering_angle).encode())

        cv2.imshow('Lane Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()