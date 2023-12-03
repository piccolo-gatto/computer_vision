import os

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

files = os.listdir('out/')
coords = []

for i in range(len(files)):
    img = np.load(f'out/h_{i}.npy')
    lbl = label(img)
    regions = regionprops(lbl)
    area = lambda region: region.area
    sort = sorted(regions, key=area)
    for j in range(len(regions)):
        coords.append(sort[j].centroid)
coords = np.array(coords)

for i in range(len(regions)):
    plt.plot(coords[i::3, 0], coords[i::3, 1])

plt.show()