import cv2
import numpy as np

# 讀取影像
image1 = cv2.imread('image1.jpg')
image2 = cv2.imread('image2.jpg')

# 調整影像大小
image1 = cv2.resize(image1, (640, 480))
image2 = cv2.resize(image2, (640, 480))

# 將影像放入向量
images = [image1, image2]

def process_image(image):
    # 轉換影像為 HSV 色彩空間
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 定義顏色範圍並建立遮罩
    lower_color = np.array([0, 25, 110])  # 這裡的範圍需要根據桌子的顏色進行調整
    upper_color = np.array([25, 130, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # 二值化處理，使用 Otsu 閥值法
    _, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 形態學操作（閉操作）
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # 檢測輪廓
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # 篩選輪廓（根據面積大小）
        if cv2.contourArea(contour) > 500:  # 根據需要調整此閾值
            # 畫出輪廓的矩形邊界框
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
            
            # 找到輪廓的凸包
            hull = cv2.convexHull(contour)
            
            # 畫出凸包
            # cv2.drawContours(image, [hull], -1, (0, 0, 255), 2)
            
            # 標示桌角（凸包的點）
            for point in hull:
                cv2.circle(image, tuple(point[0]), 3, (255, 0, 0), -1)
    
    return image

# 處理並顯示每張影像
for i, img in enumerate(images):
    result = process_image(img)
    cv2.imshow(f'Result {i+1}', result)

cv2.waitKey(0)
cv2.destroyAllWindows()
