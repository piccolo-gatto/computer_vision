import socket
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


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
        pos1 = np.unravel_index(np.argmax(img), img.shape)
        bin_img = img
        bin_img[bin_img > 0] = 1
        plt.imshow(img)
        plt.pause(1)
        img_label = label(bin_img)
        label1 = img_label[pos1]
        img[img_label == label1] = 0
        pos2 = np.unravel_index(np.argmax(img), img.shape)

        print(pos1, pos2)
        res = round(((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)**(0.5), 2)
        print(res)

        sock.send(f'{res}'.encode())
        sock.recv(4)

