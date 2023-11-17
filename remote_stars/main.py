import socket
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def get_centroid(img_label, lbl = 1):
    pos = np.where(img_label == lbl)
    return [pos[0].mean(), pos[1].mean()]


host = "84.237.21.36"
port = 5152

plt.ion()
plt.figure()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    beat = b"nope"
    sock.connect((host, port))
    while beat != b"yep":
        sock.send(b"get")

        bts = recvall(sock, 40002)
        print(len(bts))

        img = np.frombuffer(bts[2:], dtype="uint8").reshape(bts[0], bts[1])
        bin_img = img
        bin_img[bin_img > 0] = 1
        img_label = label(bin_img)

        reg = regionprops(label(bin_img))
        pos1 = get_centroid(img_label, 1)
        pos2 = get_centroid(img_label, 2)

        print(pos1, pos2)

        res = round(((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)**(0.5), 2)
        print(res)
        plt.title(str(pos1))
        plt.imshow(img)
        plt.pause(1)
