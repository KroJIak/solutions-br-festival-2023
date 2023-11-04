import cv2
import Modules.customModule as ctm
import os
import time
cap = ctm.VideoCaptureMod(ctm.CAMERA_ID)
success, img = cap.read()
h, w = img.shape[:2]
FRAME_RATE = 30
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(f"media/output{len(os.listdir('../data/media')) + 1}.mp4", fourcc, FRAME_RATE, (w, h))

def main():
    prev = 0
    try:
        while True:
            time_elapsed = time.time() - prev
            ret, frame = cap.read()
            if time_elapsed > 1. / FRAME_RATE:
                prev = time.time()
                out.write(frame)
    except KeyboardInterrupt:
        pass

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()