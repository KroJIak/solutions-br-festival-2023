import cv2
from utils import *
import customModule as ctm
import numpy as np

frame = cv2.imread('data/images/Image-9.jpg')

SIZE = ctm.SIZE
TRAP = ctm.TRAP
RECT = ctm.RECT

lr = ctm.LimiterRanges()

img = cv2.resize(frame, SIZE)
lower, upper = lr.road()
binary = binarizeHSV(img, lower, upper)
perspective = transPerspective(binary, TRAP, RECT, SIZE)
left, right = centreMass(perspective)
area = ctm.getArea(perspective, left)
resCount = np.sum(area)

print(f'[resCount]: {resCount}')
while True:
    cv2.imshow('Image', img)
    cv2.imshow('Binary', binary)
    cv2.imshow('Perspective', perspective)
    cv2.imshow('Area', area)
    match cv2.waitKey(1):
        case 27: break

cv2.destroyAllWindows()