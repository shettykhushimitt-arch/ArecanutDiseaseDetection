from ultralytics import YOLO

model = YOLO("AIModel/best.pt")

for i, layer in enumerate(model.model.model):
    print(i, layer)