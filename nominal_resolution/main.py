import numpy as np

for i in range(1, 7):
    resolution = 0
    max_size = np.loadtxt(f'img/figure{i}.txt', max_rows=1)
    img = np.loadtxt(f'img/figure{i}.txt', skiprows=2)
    max_sum = max(np.sum(img, axis=1))
    if max_sum != 0:
        print(f'Image {i}: resolution {max_size/max_sum}')
    else:
        print(f'Image {i}: not found')
