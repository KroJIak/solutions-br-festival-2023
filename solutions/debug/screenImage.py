import customModule as ctm
import cv2
import os

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    '''
    cap.set(cv2.CAP_PROP_BRIGHTNESS, -40)
    cap.set(cv2.CAP_PROP_FOCUS, 0)
    cap.set(cv2.CAP_PROP_SATURATION, 23)
    cap.set(cv2.CAP_PROP_CONTRAST, 27)
    '''

    while True:
        success, img = cap.read()
        if not success: continue
        cv2.imshow('Image', img)
        match cv2.waitKey(1):
            case 32: cv2.imwrite(f"data/Image-{len(os.listdir('../data')) + 1}.jpg", img)
            case 27: break

if __name__ == '__main__':
    main()