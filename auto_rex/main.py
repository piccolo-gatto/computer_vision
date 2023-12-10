import cv2
import keyboard
import mss as mss
import pyautogui as pytg
import numpy as np
import matplotlib.pyplot as plt
import time


start_time = time.time()
speed = 0.035

while True:
    if time.time() - start_time > 1.3:
        start_time = time.time()
        speed /= 4

    object = mss.mss().monitors[0]
    object['left'] = 125
    object['top'] = 310
    object['width'] = 25
    object['height'] = 35

    obj = np.array(mss.mss().grab(object))
    obj = cv2.cvtColor(obj, cv2.COLOR_BGRA2GRAY)
    _, obj = cv2.threshold(obj, 127, 255, cv2.THRESH_BINARY)
    print(obj.mean())
    #pytg.keyDown('down')
    if obj.mean() < 255:
        pytg.keyDown('up')
        time.sleep(0.17)
        pytg.keyDown('down')
        pytg.sleep(speed)
        pytg.keyUp('down')

    # plt.imshow(img)
    # plt.show()

    if keyboard.is_pressed('q'):
        break
