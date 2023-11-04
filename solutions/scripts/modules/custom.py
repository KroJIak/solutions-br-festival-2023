from time import sleep
import numpy as np
import cv2

class VideoCaptureMod():
    def __init__(self, CAMERA_ID, delay=4, normal=True):
        self.cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        if not normal:
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, -40)
            self.cap.set(cv2.CAP_PROP_FOCUS, 0)
            self.cap.set(cv2.CAP_PROP_SATURATION, 23)
            self.cap.set(cv2.CAP_PROP_CONTRAST, 27)
        sleep(delay)

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()

class LimiterRanges():
    def road(self):
        lower = np.array([12, 0, 178])
        upper = np.array([163, 31, 237])
        return lower, upper

def showConfirmToStop():
    sleep(1.5)
    try:
        while True: pass
    except KeyboardInterrupt as err:
        print(f'[INFO] Program has stopped! {err} \n')

def showConfirmToStart():
    sleep(1)
    try:
        while True: pass
    except KeyboardInterrupt as err:
        print(f'[INFO] Program has started! {err} \n')

def getArea(perspective, centre):
    area = perspective[SIZE[1]-INTENT:SIZE[1], centre-INTENT:centre+INTENT]
    return area

def getAreaStop(perspective, intentH, intentW):
    area = perspective[SIZE[1]-intentH:SIZE[1], intentW:SIZE[0]-intentW]
    return area

ARDUINO_PORT = '/dev/ttyUSB0'
CAMERA_ID = '/dev/video0'

KP = 0.55  # 0.22 0.32 0.42
KD = 0.25  # 0.17

SIZE = (533, 300)

INTENT = 50

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

