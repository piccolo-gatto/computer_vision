import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


def filling_factor(region):
    return region.image.mean()


def recognize(region):
    if filling_factor(region) == 1:
        return '-'
    else:
        euler = region.euler_number
        if euler == -1:  # B or 8
            if 1 in region.image.mean(0)[:1]:
                return 'B'
            else:
                return '8'
        elif euler == 0:  # A, P, D, 0 or *
            tmp = region.image.copy()
            tmp[-1, :] = 1
            tmp_labeled = label(tmp)
            tmp_regions = regionprops(tmp_labeled)
            if 1 in region.image.mean(0)[:1]:
                tmp[:, -len(tmp[0]) // 2:] = 1
                e = tmp_regions[0].euler_number
                if e == -1:
                    return 'P'
                elif e == 0:
                    return 'D'
            if 1 in region.image.mean(1):
                return '*'
            if tmp_regions[0].euler_number == -1:
                return 'A'
            else:
                return '0'
        elif euler == 1: # 1, /, X, W or *
            if 1 in region.image.mean(0):
                if region.eccentricity < 0.5:
                    return "*"
                else:
                    return "1"
            tmp = region.image.copy()
            tmp[[0, -1], :] = 1
            tmp_label = label(tmp)
            tmp_regions = regionprops(tmp_label)
            euler = tmp_regions[0].euler_number
            if euler == -1:
                return 'X'
            elif euler == -2:
                return "W"
            if region.eccentricity > 0.5:
                return '/'
            else:
                return '*'
    return '?' # unknown symbol


image = plt.imread('symbols.png').min(2)
image[image > 0] = 1
labeled = label(image)
print('count: ', np.max(labeled))

regions = regionprops(labeled)

counts = {}

for region in regions:
    symbol = recognize(region)
    if symbol not in counts:
        counts[symbol] = 0
    counts[symbol] += 1

print(counts)

print('recognized symbols: ', (1 - counts.get("?", 0) / np.max(labeled)) * 100, '%')
