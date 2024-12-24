import cv2
import torch
from torchvision import models, transforms
from PIL import Image

# Load YOLO model
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # For car detection

# Load CNN model for brand classification
cnn_model = models.resnet18(pretrained=True)
cnn_model.fc = torch.nn.Linear(cnn_model.fc.in_features, num_brands)  # Replace final layer
cnn_model.load_state_dict(torch.load("car_brand_classifier.pth"))
cnn_model.eval()

# Image transformation for CNN
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def detect_and_classify(image_path):
    # YOLO detection
    img = Image.open(image_path)
    results = yolo_model(img)
    detections = results.pandas().xyxy[0]  # YOLO results
    
    for index, row in detections.iterrows():
        if row['name'] == 'car' and row['confidence'] > 0.5:
            # Crop detected car
            car_crop = img.crop((row['xmin'], row['ymin'], row['xmax'], row['ymax']))
            car_crop = transform(car_crop).unsqueeze(0)
            
            # Brand classification
            output = cnn_model(car_crop)
            _, predicted = torch.max(output, 1)
            brand = car_brands[predicted.item()]
            print(f"Detected car brand: {brand}")

# Run the detection and classification
detect_and_classify("test_image.jpg")
