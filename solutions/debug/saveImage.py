import modules.custom as ctm
import cv2
import os

CAMERA_ID = '/dev/video0'

def main():
    cap = ctm.VideoCaptureMod(CAMERA_ID)

    success, img = cap.read()
    cv2.imwrite(f"images/Image-{len(os.listdir('images')) + 1}.jpg", img)

if __name__ == '__main__':
    main()