import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label


def neighbours4(y, x):
    return (y, x+1), (y, x-1), (y-1, x), (y+1, x)

def neighbours8(y, x):
    return [
        (y, x + 1), (y + 1, x + 1), (y + 1, x), (y + 1, x - 1), 
        (y, x - 1), (y - 1, x - 1), (y - 1, x), (y - 1, x + 1)
    ]

def get_boundaries(image_labeled, lbl=1, connectivity=neighbours4):
    pos = np.where(image_labeled == lbl)
    bounds = []
    for y, x in zip(*pos):
        for yn, xn in connectivity(y, x):
            if yn < 0 or yn > image_labeled.shape[0] - 1:
                bounds.append((y, x))
                break
            elif xn < 0 or xn > image_labeled.shape[1] - 1:
                bounds.append((y, x))
                break
            elif image_labeled[yn, xn] == 0:
                bounds.append((y, x))
                break
    return bounds

def chain(img):
    chain = []
    bnd = get_boundaries(img, 1)
    start = bnd[0]
    point = bnd[1]
    while point != start:
        neighbours = neighbours8(point[0], point[1])
        for neighbour in neighbours:
            if bnd.count(neighbour):
                chain.append(neighbours.index(neighbour))
                bnd.remove((point[0], point[1]))
                point = neighbour
                break
    chain.append(0)
    return chain


test = np.array(
    [   [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
    ] 
)
test2 = np.array(
    [   [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
)


test_lb = label(test)
print(f"Test 1: {chain(test_lb)}")
plt.imshow(test)
plt.show()

test2_lb = label(test2)
print(f"Test 2: {chain(test2_lb)}")
plt.imshow(test2)
plt.show()

image = np.load("similar.npy")
image_labeled = label(image)
max_lbl = np.max(image_labeled)
for i in range(1, max_lbl + 1):
    lb = np.zeros_like(image)
    lb[image_labeled == i] = 1
    print(f"Figure {i}: {chain(image_labeled)}")
plt.imshow(image)
plt.show()