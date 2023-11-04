from ultralytics import YOLO
'''
 0: crosswalk
 1: stop
 2: triangle
 3: circle
 4: brick
 5: nigger
 6: parking
 7: police
'''

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch

# Use the model
results = model.train(data="config.yaml", epochs=3)  # train the model
# , device='gpu'