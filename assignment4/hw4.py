import cv2
import numpy as np
import matplotlib.pyplot as plt

# calculate the intersection over union (IoU) of two masks
def intersection_over_union(mask1, mask2):
    intersection = np.logical_and(mask1, mask2)
    union = np.logical_or(mask1, mask2)
    iou_score = np.sum(intersection) / np.sum(union)
    return iou_score

iou_scores = []  # store the IoU scores

for i in range(1, 7):  # get the image file name

    file_name = "pic" + str(i) + ".jpg"

    # read original image anf groundtruth image
    image = cv2.imread("image/photo/" + file_name)
    GroundTruth = cv2.imread("image/GroundTruth/" + file_name.replace('.jpg', '.png'))

    plt.figure(figsize=(15, 5))  # set the size of the figure
    # change the color space from BGR to RGB
    plt.subplot(131), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title('Original Image')  
    plt.subplot(132), plt.imshow(GroundTruth), plt.title('GroundTruth')

    # change the color range, the value is based on the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Hue (H): 0 to 20 (In OpenCV, the range of hue is 0 to 180).
    # Saturation (S): 48 to 255.
    # Value (V): 80 to 255.
    lower_skin = np.array([0, 40, 120], dtype=np.uint8)
    upper_skin = np.array([30, 200, 255], dtype=np.uint8)

    # apply the skin mask to the HSV image
    skin_mask = cv2.inRange(hsv_image, lower_skin, upper_skin)

    # apply morphological operations to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)

    # create a blank image to store the result
    result_image = np.zeros_like(image)
    # set the color of the skin area to white
    result_image[skin_mask != 0] = (255, 255, 255)

    # calculate IOU
    iou = intersection_over_union(GroundTruth > 0, result_image > 0)
    print("IoU for", file_name, ":", iou)
    iou_scores.append(iou)

    # show the result
    plt.subplot(133), plt.imshow(result_image), plt.title('Skin Detection')
    plt.show()

# calculate the average IoU
average_iou = np.mean(iou_scores)
print("Average IoU:", average_iou)


