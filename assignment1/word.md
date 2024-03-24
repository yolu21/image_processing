1122 Digital Image Processing Assignment #1 報告
主題：圖像感興趣區域裁切、旋轉與縮放
- 專案目標：
    使用者輸入目標尺寸對圖片進行裁切，透過拖拉滑桿可以旋轉與縮放圖片，並將截取圖片儲存至裝置。

- 開發環境：
    - 用的作業系統：Windows
    - 開發環境：VScode
    - 用的套件：OpenCV version: 4.9.0
    - 程式語言：Python 3.12.0
    - 程式架構與功能說明：

　　使用者在 console 輸入圖片路徑及檔名，並設定目標圖片大小後，顯示preview window與crop window，利用 trackbar 調整 Zoom, Rotate, iniX（矩形左上角 x 座標）, iniY（矩形左上角 y座標） 等參數，可以從crop window中看到選取的圖像區域，利用 trackbar 調整 Save 從 0 到 1 或按下鍵盤 's' 即可儲存截取圖片至指定路徑，並在 console 印出 "Save image successfully"。按下鍵盤 'esc' 可關閉 windows。 

Zoom 可以透過 cv2.resize 來改變圖片大小，縮放比例從原圖的 0.1 ~ 1.5倍。fx 、fy 分別代表水平方向和垂直方向的缩放比例。

- fx 、fy = 1，圖片大小不變
- fx 、fy < 1，圖片變小
- fx 、fy > 1，圖片變大

除以 10 是為了讓可調性變多，可以調到小數點的倍數。 
copy_img = cv2.resize(img, None, fx = scale/10, fy = scale/10)
Rotate 是先找到圖片的中心點，利用 cv2.getRotationMatrix2D 以中心點旋轉，返回一個旋轉矩陣。再利用 cv2.warpAffine，可以將圖片根據指定的「仿射矩陣」，輸出成轉換後的新圖片。

```
center = (width // 2, height // 2) #Get the center of the image
```

```
GetRotate = cv2.getRotationMatrix2D(center, angle, 1.0) #Rotate image
copy_img = cv2.warpAffine(copy_img , GetRotate, (width, height)) 
```

畫框是用 cv2.rectangle，寫的過程發現會一直重複畫框，所以 copy 一個新的圖片（clear_img）覆蓋上，讓框是畫在 clear_img 的那張。

```
clear_img = copy_img.copy()
```

- 成果展示與討論：

使用者在console輸入的範例

```
input image folder path:image/  
input image filename:yzu2.jpg
target image Width:600
target image Height:400
```


執行範例 1. 
使用 preview window 的 Zoom, iniX, iniY trackbar 調整選取矩形區域，利用 Save 或按下鍵盤 's' 存檔，得到目標 600×400 輸出圖像 1093338HW1_crop.jpg。

執行範例 2. 
使用 preview window 的 Zoom, Rotate, iniX, iniY trackbar 調整選取矩形區域，利用 Save 或按下鍵盤 's' 存檔，得到目標 600×400 輸出圖像 1093338HW1_crop.jpg。

執行範例 3. 
使用 preview window 的 Zoom, Rotate, iniX, iniY trackbar 調整選取矩形區域，利用 Save 或按下鍵盤 's' 存檔，得到目標 300×600 輸出圖像 1093338HW1_crop.jpg。

執行範例 4. 
使用 preview window 的 Zoom, Rotate, iniX, iniY trackbar 調整選取矩形區域，可以來回操作 Zoom 和 Rotate 的trackbar ，調整至覺得適合的圖片，利用 Save 或按下鍵盤 's' 存檔，得到目標 600×400 輸出圖像 1093338HW1_crop.jpg。
