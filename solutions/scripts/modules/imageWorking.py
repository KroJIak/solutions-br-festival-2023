import numpy as np
import cv2

def encodeImage(img):
    if not len(img): return None
    success, img = cv2.imencode('.jpg', img)
    imgString = img.tobytes()
    return imgString

def decodeImage(imgString):
    if not len(imgString): return None
    imgArray = np.frombuffer(imgString, np.uint8)
    img = cv2.imdecode(imgArray, cv2.IMREAD_COLOR)
    return img