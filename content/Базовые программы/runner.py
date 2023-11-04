import argparse
import time
from pathlib import Path

import cv2
import numpy as np
import serial

from arduino import Arduino
from utils import *


CAR_SPEED = 1430
ARDUINO_PORT = '/dev/ttyUSB0'
CAMERA_ID = '/dev/video0'

KP = 0.55  # 0.22 0.32 0.42
KD = 0.25  # 0.17
last = 0

SIZE = (533, 300)

# Прямоугольник для выделения области перед колесами
RECT = np.float32([[0, SIZE[1]],
                   [SIZE[0], SIZE[1]],
                   [SIZE[0], 0],
                   [0, 0]])
# Трапеция для выделения области перед колесами
TRAP = np.float32([[10, 299],
                   [523, 299],
                   [440, 200],
                   [93, 200]])

arduino = Arduino(ARDUINO_PORT, baudrate=115200, timeout=10)
time.sleep(1)
arduino.set_speed(CAR_SPEED)    # Первое сообщение подается, чтобы очистить буфер обмена,
time.sleep(0.05)                # оно не принимается микроконтроллером

cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

arduino.set_speed(CAR_SPEED)

last_err = 0
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.resize(frame, SIZE)
        binary = binarize(img, 200)
        perspective = trans_perspective(binary, TRAP, RECT, SIZE)

        left, right = centre_mass(perspective)
        
        err = 0 - ((left + right) // 2 - SIZE[0] // 2)
        if abs(right - left) < 100:
            err = last_err

        angle = int(90 + KP * err + KD * (err - last_err))
        last_err = err

        if angle < 70:
            angle = 70
        elif angle > 110:
            angle = 110

        print(f'angle={angle}')
        arduino.set_angle(angle)
except KeyboardInterrupt as e:
    print('Program stopped!', e)


arduino.stop()
arduino.set_angle(90)
cap.release()
