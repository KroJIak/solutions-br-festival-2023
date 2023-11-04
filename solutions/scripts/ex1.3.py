from modules.arduino import Arduino
import modules.custom as ctm
from modules.utils import *
import numpy as np
import time
import cv2

NUMBER_CASE = int(input())

ctm.showConfirmToStart()

# МИНИМУМ 1430 !!!!!!!
CAR_SPEED = 1430
THRESHOLD_WHITE = 1000
ALL_COUNT_LINES = [18, 36, 13]
# 18
SIZE = ctm.SIZE
TRAP = ctm.TRAP
RECT = ctm.RECT
KP = ctm.KP
KD = ctm.KD

lr = ctm.LimiterRanges()
cap = ctm.VideoCaptureMod(ctm.CAMERA_ID)
arduino = Arduino(ctm.ARDUINO_PORT, baudrate=115200, timeout=10)
time.sleep(2)
arduino.set_angle(90)   # Первое сообщение подается, чтобы очистить буфер обмена,
time.sleep(0.05)                # оно не принимается микроконтроллером

try:
    countLines = 0
    isWhite = True
    lastErr = 0
    arduino.set_speed(CAR_SPEED)
    while True:
        success, frame = cap.read()
        if not success: continue
        img = cv2.resize(frame, SIZE)
        lower, upper = lr.road()
        binary = binarizeHSV(img, lower, upper)
        perspective = transPerspective(binary, TRAP, RECT, SIZE)
        left, right = centreMass(perspective)

        area = ctm.getArea(perspective, left)
        sumArea = np.sum(area)
        if sumArea > THRESHOLD_WHITE and not isWhite:
            countLines += 1
            isWhite = True
        elif sumArea <= THRESHOLD_WHITE:
            isWhite = False
        if countLines >= ALL_COUNT_LINES[NUMBER_CASE]: break

        err = 0 - ((left + right) // 2 - SIZE[0] // 2)
        if abs(right - left) < 100: err = lastErr
        angle = int(90 + KP * err + KD * (err - lastErr))
        lastErr = err
        angle = min(max(65, angle), 115)

        arduino.set_angle(angle)
        print(f'[sumArea]: {sumArea}')
        print(f'[countLines]: {countLines}')
        # print(f'[angle]: {angle}')
    arduino.set_speed(1500)
except KeyboardInterrupt as err:
    print(f'[WARN] Program want to stop! {err} \n')
    print('[INFO] Отключи питание моторов!!!!')

ctm.showConfirmToStop()

cap.release()
arduino.stop()
arduino.set_angle(90)
