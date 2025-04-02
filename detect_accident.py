import glob
from ultralytics import YOLO
import cv2

# Load the trained model
model = YOLO('runs/detect/train/weights/best.pt')

# Get all images from the folder
image_paths = glob.glob('test_images/*.jpg')  # Update the extension if needed

for img_path in image_paths:
    results = model(img_path)
    results.show()
