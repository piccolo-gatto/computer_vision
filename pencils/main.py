import os
import matplotlib.pyplot as plt
import cv2
from skimage.measure import regionprops, label

files = os.listdir('images/')
pencils = 0
for file in files:
    img = cv2.imread(f'images/{file}', cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret, binary = cv2.threshold(blur,0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary = cv2.bitwise_not(binary)
    # plt.imshow(binary)
    # plt.show()
    labeled = label(binary)
    for region in regionprops(labeled):
        if region.perimeter > 2000 and 30 > (region.major_axis_length / region.minor_axis_length) > 15:
            pencils += 1

print(pencils)
