import cv2
import matplotlib.pyplot as plt


count = 0
all_images = 0
video = cv2.VideoCapture('output.avi')
img = cv2.imread('img.jpg', cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# plt.imshow(img)
# plt.show()
while True:
    _, frame = video.read()
    if _ == 0:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    match = cv2.matchTemplate(frame, img, cv2.TM_CCOEFF_NORMED)
    loc = cv2.minMaxLoc(match)
    # print(loc)
    all_images += 1
    if loc[0] <= 1.0 and loc[1] >= 0.7:
        count += 1
video.release()

print(f"Всего {all_images} изображений")
print(f"Моё изображение встречается {count} раз")

