from ultralytics import YOLO

model = YOLO("AIModel/best.pt")

print(model)
print(type(model.model))