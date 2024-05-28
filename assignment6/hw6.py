import cv2
import numpy as np

# read image (tif format)
image = cv2.imread('wood-dowels.tif', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Binarization
_, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

# Morphological processing - erosion then dilation to remove noise
kernel = np.ones((3, 3), np.uint8)
binary = cv2.erode(binary, kernel, iterations=1)
binary = cv2.dilate(binary, kernel, iterations=1)

# Gaussian blur
blurred = cv2.GaussianBlur(gray, (9, 9), 2)

# Set parameters for detecting small circles
small_minRadius = 5
small_maxRadius = 20
small_param2 = 30

# Using HoughCircles to detect small circles
small_circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                                 param1=200, param2=small_param2, minRadius=small_minRadius, maxRadius=small_maxRadius)

# Set parameters for detecting large circles
large_minRadius = 21
large_maxRadius = 50  # Can be adjusted to detect larger circles
large_param2 = 30  # Increase the accumulator threshold to improve the detection accuracy of large wooden dowels

# Using HoughCircles to detect large circles
large_circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                                 param1=200, param2=large_param2, minRadius=large_minRadius, maxRadius=large_maxRadius)

# Confirm that the circles are detected
if small_circles is not None:
    small_circles = np.uint16(np.around(small_circles))

if large_circles is not None:
    large_circles = np.uint16(np.around(large_circles))

# Draw the detected circles
if small_circles is not None:
    for i in small_circles[0, :]:
        # Using blue color to draw small circles
        cv2.circle(image, (i[0], i[1]), i[2], (255, 0, 0), 2)
        cv2.circle(image, (i[0], i[1]), 2, (255, 0, 0), 3)  # 圓心

if large_circles is not None:
    for i in large_circles[0, :]:
        # Using green color to draw large circles
        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(image, (i[0], i[1]), 2, (0, 255, 0), 3)  # 圓心

    # Count the number of small and large wooden dowels
    num_small_circles = len(small_circles[0, :]) if small_circles is not None else 0
    num_large_circles = len(large_circles[0, :]) if large_circles is not None else 0

    print(f"大木圓榫數量: {num_large_circles}")
    print(f"小木圓榫數量: {num_small_circles}")

    # Show the number of small and large wooden dowels on the image
    cv2.putText(image, f'Large Circles: {num_large_circles}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(image, f'Small Circles: {num_small_circles}', (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Show the image with detected circles
    cv2.imshow('Detected Circles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("未偵測到圓形")
