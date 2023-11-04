# coding: utf-8
import numpy as np
import cv2

def binarizeHSV(img, lower, upper, ksize=5):
    imgBlur = cv2.blur(img, (ksize, ksize))
    imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
    binary = cv2.inRange(imgHSV, lower, upper)
    return binary

def transPerspective(binary, trap, rect, size):
    matrix_trans = cv2.getPerspectiveTransform(trap, rect)
    perspective = cv2.warpPerspective(binary, matrix_trans, size, flags=cv2.INTER_LINEAR)
    return perspective

def centreMass(perspective):
    hist = np.sum(perspective, axis=0)
    mid = hist.shape[0] // 2

    i, centre, sumMass = 0, 0, 0
    while i <= mid:
        centre += hist[i] * (i + 1)
        sumMass += hist[i]
        i += 1
    if sumMass > 0: midMassLeft = int(centre / sumMass)
    else: midMassLeft = int(mid - 1)

    i, centre, sumMass = mid, 0, 0
    while i < hist.shape[0]:
        centre += hist[i] * (i + 1)
        sumMass += hist[i]
        i += 1
    if sumMass > 0: midMassRight = int(centre / sumMass)
    else: midMassRight = int(mid + 1)

    return midMassLeft, midMassRight