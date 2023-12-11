import cv2
import keyboard
import mss as mss
import pyautogui as pytg
import numpy as np
import matplotlib.pyplot as plt
import time

object = mss.mss().monitors[0]
object['left'] = 130
object['top'] = 310
object['width'] = 40
object['height'] = 35
start_time = time.time()
sleep = 0.17
speed = 0.007

while True:
    if time.time() - start_time > 8:
        start_time = time.time()
        object['width'] += 1
        sleep -= speed

        print('sleep: ', sleep, ', speed: ', speed, ', width: ', object['width'])

    if 0.05 <= sleep <= 0.10:
        speed = 0.008
    if sleep <= 0.05:
        speed = 0

    obj = np.array(mss.mss().grab(object))
    obj = cv2.cvtColor(obj, cv2.COLOR_BGRA2GRAY)
    _, obj = cv2.threshold(obj, 127, 255, cv2.THRESH_BINARY)
    print(obj.mean())
    #pytg.keyDown('down')
    if obj.mean() < 255:
        pytg.keyDown('up')
        time.sleep(sleep)
        pytg.keyDown('down')
        time.sleep(0.0001)
        pytg.keyUp('down')

    # plt.imshow(img)
    # plt.show()

    if keyboard.is_pressed('q'):
        break
