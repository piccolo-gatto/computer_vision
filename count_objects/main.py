import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_erosion
from skimage.measure import label


masks = {"rectangle":np.array([
                                [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1],
          [1,1, 1, 1, 1, 1]
                                ]),
           "top":np.array([[0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [1, 1, 0, 0, 1, 1],
          [1, 1, 0, 0, 1, 1],
          [1, 1, 1, 1, 1, 1],
          [1,1, 1, 1, 1, 1]]),
           "bottom":np.array([[1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1],
          [1, 1, 0, 0, 1, 1],
          [1, 1, 0, 0, 1, 1],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0]]),
           "right":np.array([[1, 1, 1, 1, 0, 0],
          [1, 1, 1, 1, 0, 0],
          [1, 1, 0, 0, 0, 0],
          [1, 1, 0, 0, 0, 0],
          [1, 1, 1, 1, 0, 0],
          [1, 1, 1, 1, 0, 0]]),
           "left":np.array([[0, 0, 1, 1, 1, 1],
          [0, 0, 1, 1, 1, 1],
          [0, 0, 0, 0, 1, 1],
          [0, 0, 0, 0, 1, 1],
          [0, 0, 1, 1, 1, 1],
          [0, 0, 1, 1, 1, 1]])}
figures = {
    "rectangle": 0,
    "top": 0,
    "right": 0,
    "left": 0,
    "bottom": 0
}
image = np.load('ps.npy.txt')
lb = label(image)
lb_max = lb.max()
for name, struct in masks.items():
  erosion = binary_erosion(image, struct)
  lb_elem = label(erosion)
  if name in ('rectangle', 'left', 'right'):
    figures[name] = lb_elem.max()
  else:
    figures[name] = lb_elem.max() - figures['rectangle']
plt.imshow(image)
plt.show()
print('All:', lb_max)
print(figures)