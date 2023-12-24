import cv2
import numpy as np


def blur(arr, size=(10, 10)):
    out = np.zeros_like(arr)
    stepy = out.shape[0] // size[0]
    stepx = out.shape[1] // size[1]
    for y in range(0, arr.shape[0], stepy):
        for x in range(0, arr.shape[1], stepx):
            out[y: y+stepy, x: x+stepy] = np.average(arr[y:y+stepy, x:x+stepy])
    return out
def get_coords(frame):
    w = int(frame[2] * 1.2)
    h = int(frame[3] * 1.5)
    x = frame[0] - int((frame[2] * 1.2 - frame[2]) // 2)
    y = frame[1] - int((frame[3] * 1.5 - frame[3]) // 2)
    return w, h, x, y

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cascade = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")
glasses = cv2.imread("deal_with_it.png")

while cam.isOpened():
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
    mask[:, :, :] = 255
    faces = cascade.detectMultiScale(gray, 1.1, 5)

    if (len(faces) == 2):
        w1, h1, x1, y1 = get_coords(faces[0])
        w2, h2, x2, y2 = get_coords(faces[1])
        roi = frame[y1:y2+h2, x1:x2+w2]
        glasses = cv2.resize(glasses, (roi.shape[1], roi.shape[0]))
        mask[y1:y2+h2, x1:x2+w2] = glasses
        mask[np.where(mask[:, :, 0] >= 230)] = frame[np.where(mask[:, :, 0] >= 230)]
        frame = mask
    else:
        continue
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

