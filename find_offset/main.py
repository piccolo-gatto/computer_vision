import numpy as np


img1 = np.loadtxt(f'img/img1.txt', skiprows=2)
img2 = np.loadtxt(f'img/img2.txt', skiprows=2)

max_index1 = np.unravel_index(np.argmax(img1), img1.shape)
max_index2 = np.unravel_index(np.argmax(img2), img2.shape)

print(f"Смещение по x: {max_index1[0] - max_index2[0]}, y: {max_index1[1] - max_index2[1]}")
