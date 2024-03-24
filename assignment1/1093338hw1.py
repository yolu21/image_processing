import cv2           # import OpenCV Function Library
import numpy as np   # import Numpy Function Library

folder_path = str(input('input image folder path:'))  # folder path
file_name = str(input('input image filename:'))
target_width = int(input('target image Width:'))  #set the target image width
target_height = int(input('target image Height:')) #set the target image height

scale_factor = 0.2  # set the scale factor
img = cv2.imread(folder_path + file_name)  # read image
img = cv2.resize(img, None, fx = scale_factor, fy = scale_factor, interpolation = cv2.INTER_AREA) # resize image
cv2.imshow('1093338HW1_preview',img)        # open window to show the image

copy_img = img.copy()  # copy the image
width = copy_img.shape[1]
height = copy_img.shape[0]
set_X = 0
set_Y = 0

def crop_function(scale, angle):
    global copy_img, width, height, set_X, set_Y, target_height, target_width
    if scale == 0:
        scale = 1
    copy_img = cv2.resize(img, None, fx = scale/10, fy = scale/10) #Zoom in or out image
    
    width = copy_img.shape[1]
    height = copy_img.shape[0]
    if angle != 0:
        center = (width // 2, height // 2) #Get the center of the image
        GetRotate = cv2.getRotationMatrix2D(center, angle, 1.0) #Rotate image
        copy_img = cv2.warpAffine(copy_img , GetRotate, (width, height))
    
    # Draw rectangle
    clear_img = copy_img.copy()
    color = (0, 255, 0)  # Green color
    thickness = 2
    if (set_X + target_width > width):
        set_X = width - target_width
        
    if (set_Y + target_height > height):
        set_Y = height - target_height
        
    cv2.rectangle(clear_img, (set_X, set_Y), (set_X + target_width, set_Y + target_height), color, thickness)
    cv2.imshow('1093338HW1_crop', clear_img)

def draw_rect(x, y):
    global set_X, set_Y
    set_X = x
    set_Y = y
    crop_function(cv2.getTrackbarPos('Zoom', '1093338HW1_preview'), cv2.getTrackbarPos('Rotate', '1093338HW1_preview'))


def save_function(save):
    global copy_img, set_X, set_Y
    crop_img = copy_img[set_Y:set_Y + target_height, set_X:set_X + target_width]  # crop image
    if save == 1 :
        cv2.imwrite(folder_path + '1093338HW1_crop.jpg', crop_img)  # save image
        print('Save image successfully')
    else:
        print('Save image failed')

cv2.createTrackbar('Zoom', '1093338HW1_preview', 0, 15, lambda scale: crop_function(scale, cv2.getTrackbarPos('Rotate', '1093338HW1_preview')))
cv2.setTrackbarPos('Zoom', '1093338HW1_preview', 10)
cv2.createTrackbar('Rotate', '1093338HW1_preview', 0, 359, lambda angle: crop_function(cv2.getTrackbarPos('Zoom', '1093338HW1_preview'), angle))
cv2.setTrackbarPos('Rotate', '1093338HW1_preview', 0)

cv2.createTrackbar('intX', '1093338HW1_preview', 0, width, lambda x: draw_rect(x, cv2.getTrackbarPos('intY', '1093338HW1_preview')))
cv2.createTrackbar('intY', '1093338HW1_preview', 0, height, lambda y: draw_rect(cv2.getTrackbarPos('intX', '1093338HW1_preview'), y))
    
cv2.createTrackbar('Save', '1093338HW1_preview', 0, 1, lambda save :save_function(save))
cv2.setTrackbarPos('Save', '1093338HW1_preview', 0)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'): # press 's' to save the image
        save_function(1)
    elif key == 27:  # press 'ESC' to exit
        break  
cv2.destroyAllWindows()  # close all windows