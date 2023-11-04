import os

from ultralytics import YOLO
import cv2


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

model_path = 'train3/weights/last.pt'
# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.5
# frame = cv2.imread('KHkLG4Jv-RWUl-Z2Ej-VHq0-cfymvCOEw6xI.jpg')
while True:
    ret, frame = cap.read()
    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, f'{results.names[int(class_id)].upper()} [{score}]', (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow('Image', frame)
    match cv2.waitKey(1):
        case 27: break

cap.release()
cv2.destroyAllWindows()
