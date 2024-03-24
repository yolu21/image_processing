import cv2           # import OpenCV Function Library
import os

t_lower = 100  # set the lower threshold
t_upper = 200  # set the upper threshold


def process_img(folder_path, img, lower, upper):
    try:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        Blur_img = cv2.GaussianBlur(gray_img, (3, 3), 0) # Applying the Gaussian Blur filter, be sure to use an odd number for the kernel size
        
        edges = cv2.Canny(Blur_img, lower, upper) # Applying the Canny Edge filter 

        return edges
    except Exception as e:
        print("Error:", e)
        print("Please check the file path and try again.")

def save_function(folder_path, edge):
    if edge is not None:
        filename = os.path.join(folder_path, '1093338HW1.jpg')
        cv2.imwrite(filename, edge)  # save image
        print('Save image successfully')
    else:
        print('Save image failed')

def trackbar_callback(value, folder_path, img, other_threshold):
    global t_lower, t_upper

    if other_threshold == 'lower':
        t_lower = value
        t_upper = cv2.getTrackbarPos('t_Upper', 'Original Image')
    else:
        t_lower = cv2.getTrackbarPos('t_Lower', 'Original Image')
        t_upper = value

    edges = process_img(folder_path, img, t_lower, t_upper)
    if edges is not None:
        cv2.imshow('Canny Edges', edges)
                
# def main():
folder_path = str(input('input image folder path:'))  # folder path

file_name = str(input('input image filename:'))

img = cv2.imread(folder_path + file_name)  # read image
if img is None:
    raise FileNotFoundError("Cannot find the image file. Please check the file path and try again.")
img = cv2.resize(img, (800,600), interpolation = cv2.INTER_AREA) # resize image
cv2.imshow('Original Image', img)

cv2.createTrackbar('t_Lower', 'Original Image', 100, 254, lambda x: trackbar_callback(x, folder_path, img, 'lower'))
cv2.createTrackbar('t_Upper', 'Original Image', 200, 254, lambda y: trackbar_callback(y, folder_path, img, 'upper'))

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'): 
        edges = process_img(folder_path, img, t_lower, t_upper)
        save_function(folder_path, edges)
    elif key == ord('q'):  # Press 'q' to quit
        break
cv2.destroyAllWindows()