import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_dilation, binary_erosion, binary_closing, binary_opening
from skimage.measure import label


struct = [[[1, 0, 0, 0, 1], 
        [0, 1, 0, 1, 0], 
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1]],
        [[0, 0, 1, 0, 0], 
        [0, 0, 1, 0, 0], 
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]]]
image = np.load('stars.npy')
plt.imshow(image)
plt.show()
lb = label(image)
print('Всего объектов: ', lb.max())
res = 0
for k in range(1, lb.max() + 1):
    star = np.zeros_like(image)
    star[lb == k] = 1
    for j in range(len(struct)):
        get_star = binary_erosion(star, struct[j])
        new_lb = label(get_star)
        if new_lb.max() != 0:
                res += 1
print('Кол-во звёздочек: ', res)