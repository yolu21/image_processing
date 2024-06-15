import cv2
import numpy as np

# read images
image1 = cv2.imread('image1.jpg')
image2 = cv2.imread('image2.jpg')

# resize images
image1 = cv2.resize(image1, (640, 480))
image2 = cv2.resize(image2, (640, 480))

# put images into a vector
images = [image1, image2]

def process_image(image):
    # change color space from BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # define the range of color
    lower_color = np.array([0, 25, 110]) 
    upper_color = np.array([25, 130, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Use Otsu's method to automatically select the threshold
    _, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

     # compute the edge density
    edge_density = np.sum(binary) / (binary.shape[0] * binary.shape[1] * 255)
    
    # choose the kernel size for edge density
    if edge_density > 0.1: 
        kernel_size = 3
    else:
        kernel_size = 7

    # morphological operation
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # find contours
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # select the contour with a certain area
        if cv2.contourArea(contour) > 300:  
            # draw bounding box
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
            
            # find convex hull
            hull = cv2.convexHull(contour)
            
            # draw convex hull
            for point in hull:
                cv2.circle(image, tuple(point[0]), 2, (255, 0, 0), -1)
    
    return image

# process images and show the results
for i, img in enumerate(images):
    result = process_image(img)
    cv2.imshow(f'Result {i+1}', result)

cv2.waitKey(0)
cv2.destroyAllWindows()
