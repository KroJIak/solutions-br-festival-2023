import customModule as ctm
from ModuleConnect import connectGetTrackingObjects
import cv2

def main():
    cap = ctm.VideoCaptureMod(ctm.CAMERA_ID)
    con = connectGetTrackingObjects()

    while True:
        success, img = cap.read()
        if not success: continue
        data = con.postImage(img)
        print(data)
        cv2.imshow('Image', img)

        match cv2.waitKey(1):
            case 27: break

if __name__ == '__main__':
    main()