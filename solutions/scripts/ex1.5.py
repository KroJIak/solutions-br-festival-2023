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
CAR_SLOW_SPEED = 1445
THRESHOLD_WHITE = 1000
THRESHOLD_STOP_WHITE = 3_400_000
ALL_COUNT_LINES = [20, 23, 50]


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
            if countLines >= ALL_COUNT_LINES[NUMBER_CASE]: raise Exception('Done')

            area = ctm.getAreaStop(perspective, 220, 50)
            resCount = np.sum(area)
            if resCount > THRESHOLD_STOP_WHITE: break

            err = 0 - ((left + right) // 2 - SIZE[0] // 2)
            if abs(right - left) < 100: err = lastErr
            angle = int(90 + KP * err + KD * (err - lastErr))
            lastErr = err
            angle = min(max(65, angle), 115)

            print(f'[sumArea]: {sumArea}')
            print(f'[countLines]: {countLines}')
            arduino.set_angle(angle)
            #print(f'[angle]: {angle}')

        arduino.set_speed(CAR_SLOW_SPEED)
        arduino.set_angle(100)
        lastTime = time.time() + 0.7
        while time.time() < lastTime: pass

        arduino.set_angle(60)
        lastTime = time.time() + 6.8
        while time.time() < lastTime: pass

        arduino.set_speed(CAR_SPEED)
        lastTime = time.time() + 1
        while time.time() < lastTime:
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
            if countLines >= ALL_COUNT_LINES[NUMBER_CASE]: raise Exception('Done')

            err = 0 - ((left + right) // 2 - SIZE[0] // 2)
            if abs(right - left) < 100: err = lastErr
            angle = int(90 + KP * err + KD * (err - lastErr))
            lastErr = err
            angle = min(max(65, angle), 115)

            print(f'[sumArea]: {sumArea}')
            print(f'[countLines]: {countLines}')
            print('WAIT')
            arduino.set_angle(angle)
            #print(f'[angle]: {angle}')

except KeyboardInterrupt as err:
    print(f'[WARN] Program want to stop! {err} \n')
    print('[INFO] Отключи питание моторов!!!!')

arduino.set_speed(1500)
ctm.showConfirmToStop()

arduino.stop()
arduino.set_angle(90)
cap.release()
