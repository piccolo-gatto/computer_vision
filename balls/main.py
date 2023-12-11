import cv2
import numpy as np
import time
import random

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, -2)
capture.set(cv2.CAP_PROP_EXPOSURE, 1)

cv2.namedWindow('Camera')
cv2.namedWindow('Debug')


colors = [
    ((18, 80, 100), (30, 230, 255)), #yellow
    ((10, 100, 70), (80, 255, 130)), #green
    ((87, 100, 100), (107, 255, 255)), #blue
    ((0, 100, 100), (5, 255, 255)) #orange
]

end = 0
new_c = [0, 0]
random.shuffle(colors)
count = int(input('Сколько цветов загадать (3 или 4): '))
if count == 3:
    colors = colors[0:3]
elif count == 4:
    pass
print('Загаданные цвета: ', colors)
while capture.isOpened():
    ret, frame = capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    balls = []
    for color in colors:
        mask = cv2.inRange(hsv, color[0], color[1])
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        if len(cnts) > 0:
            start = time.perf_counter()
            c = max(cnts, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
            t = start-end
            S = ((center[0] - new_c[0])**2 + (center[1] - new_c[1])**2)**(1/2)
            u = S/t
            #print(u)
            if radius > 15:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 255, 255), -1)
                balls.append((center, color))
                if len(balls) == len(colors):
                    new_c = center
                    end = start
                    sort = []
                    for elem in sorted(balls, key=lambda x: x[0]):
                        sort.append(elem[1])
                    if all(ball == color for ball, color in zip(sort, colors)): 
                        print('Победа')

        cv2.imshow('Debug', mask)
        cv2.imshow('Camera', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    



capture.release()
cv2.destroyAllWindows()