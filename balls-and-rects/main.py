import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops


image = plt.imread('balls_and_rects.png')
hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
binary = image.mean(2) > 0
labeled = label(binary)

print("All figures:", np.max(labeled))

regions = regionprops(labeled)
colors = []
circles = []
rects = []
h = hsv[:, :, 0]

for region in regions:
    pixels = h[region.coords]
    r = h[region.bbox[0]:region.bbox[2], region.bbox[1]:region.bbox[3]]
    colors.extend(np.unique(r)[1:])
    if np.min(r) == 0.0:
        circles.append(r)
    else:
        rects.append(r)

print("Rectangles:", len(rects))
print("Circles:", len(circles))

clusters = []
while colors:
    color1 = colors.pop(0)
    clusters.append([color1])
    for color2 in colors.copy():
        if abs(color1 - color2) < 5:
            clusters[-1].append(color2)
            colors.pop(colors.index(color2))

shades = {}

for cluster in clusters:
  shades[int(np.mean(cluster))] = {
      'circles': 0,
      'rects': 0
  }

for shade in shades.keys():
  for i in range(len(circles)):
    if (shade-1) <= int(np.max(circles[i])) <= (shade+1):
      shades[shade]['circles'] += 1

  for i in range(len(rects)):
    if (shade-1) <= int(np.max(rects[i])) <= (shade+1):
      shades[shade]['rects'] += 1

  print(f"Shade {shade}: circles {shades[shade]['circles']}, rectangles {shades[shade]['rects']}")


plt.imshow(image)
plt.show()