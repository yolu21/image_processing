import cv2
import numpy as np
import matplotlib.pyplot as plt
# read the damaged image

plt.figure(figsize=(15, 5))  # 設置 plt 視窗大小
file_name = str(input('input image filename:'))
damaged_img = cv2.imread(file_name, 0)  # grayscale mode
plt.subplot(143), plt.imshow(damaged_img, cmap='gray'), plt.title('Damaged Image')

# do the Fourier Transform
f_transform = np.fft.fft2(damaged_img)
fshift = np.fft.fftshift(f_transform) # shift the zero frequency component to the center

# gain the magnitude and phase spectrum
magnitude_spectrum = np.log(np.abs(fshift))
plt.subplot(141), plt.imshow(magnitude_spectrum, cmap='gray'), plt.title('Magnitude Spectrum')

phase_spectrum = np.angle(fshift)
plt.subplot(142), plt.imshow(phase_spectrum, cmap='gray'), plt.title('Phase Spectrum')

# apply the low pass filter
rows, cols = damaged_img.shape
crow, ccol = rows // 2 , cols // 2  # find the center of the image
radius = 45  # set the radius of the circle
lpf_mask = np.zeros((rows, cols), np.uint8)
cv2.circle(lpf_mask, (ccol, crow), radius, 1, -1)
magnitude_spectrum_filtered = magnitude_spectrum * lpf_mask

#mix the magnitude and phase spectrum
restored_f_transform = np.exp(magnitude_spectrum_filtered + 1j * phase_spectrum)

# reverse the Fourier Transform
restored_img = np.fft.ifftshift(restored_f_transform)
restored_img = np.fft.ifft2(restored_img)
restored_img = np.abs(restored_img)
restored_img = np.uint8(restored_img)

plt.subplot(144), plt.imshow(restored_img, cmap='gray'), plt.title('Restored Image')

plt.subplots_adjust(hspace=0.5, wspace=0.5) #set the space between the subplots
plt.show()
