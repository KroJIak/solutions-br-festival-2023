from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import custom as ctm
import os

class signDetector():
    def __init__(self, modelPath, labelsPath):
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)
        # Load the model
        self.model = load_model(modelPath, compile=False)
        # Load the labels
        self.class_names = open(labelsPath, 'r', encoding='utf-8').readlines()

    def findObjects(self, img):
        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        # Normalize the image array
        image = (image / 127.5) - 1
        # Predicts the model
        prediction = self.model.predict(image)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        classObject = class_name[2:]
        scoreObject = float(confidence_score)

        return classObject, scoreObject

def main():
    cap = ctm.VideoCaptureMod(ctm.CAMERA_ID)
    sd = signDetector('traficSignModel/keras_model.h5', 'traficSignModel/labels.txt')
    while True:
        success, img = cap.read()
        if not success: continue
        classObject, scoreObject = sd.findObjects(img)
        print(classObject, scoreObject)
        cv2.imshow('Image', img)

        match cv2.waitKey(1):
            case 27: break

if __name__ == '__main__':
    main()