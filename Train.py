from ultralytics import YOLO

# Load pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")

# Train the model with your dataset
model.train(data="config.yaml", epochs=50)

# Save the trained model
model.export(format="onnx")  # Optional: Export to ONNX format
