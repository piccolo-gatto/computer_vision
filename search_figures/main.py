import zmq
import cv2
import numpy as np

flimit = 85
slimit = 25

def fupdate(value):
    global flimit
    flimit = value

def supdate(value):
    global slimit
    slimit = value

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect("tcp://192.168.0.104:6556")

cv2.namedWindow("Camera")
cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)
cv2.createTrackbar("F", "Mask", flimit, 255, fupdate)
cv2.createTrackbar("S", "Mask", slimit, 255, supdate)
cv2.setTrackbarPos("F", "Mask", flimit)
cv2.setTrackbarPos("S", "Mask", slimit)



while True:
    circles = 0
    squares = 0
    buffer = socket.recv()
    arr = np.frombuffer(buffer, np.uint8)
    frame = cv2.imdecode(arr, -1)
    # frame = cv2.imread('img.jpg')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    contours = cv2.Canny(gray, flimit, slimit)
    mask = cv2.dilate(contours, None, iterations=8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        x, y, width, height = cv2.boundingRect(approx)
        print(cv2.contourArea(approx) / (width * height))

        if cv2.contourArea(approx) / (width * height) < 0.2 or cv2.contourArea(approx) / (width * height) > 0.7:
            cv2.putText(frame, "Circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2)
            circles += 1
        else:
            cv2.putText(frame, "Square", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2)
            squares += 1
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 255), 2)

    cv2.putText(frame, f"All figures: {len(contours)}; Squares: {squares}; Circles: {circles}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", mask)
    print("------------------")
    key = cv2.waitKey(500)
    if key == ord("q"):
        break

