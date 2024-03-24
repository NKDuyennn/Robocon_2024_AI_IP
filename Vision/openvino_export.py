from ultralytics import YOLO

# Load a YOLOv8n PyTorch model
model = YOLO('ball_silo_detect.pt')

# Export the model
model.export(format='openvino')  # creates 'yolov8n_openvino_model/'

# object detection model
det_model_path = "ball_silo_detect_openvino_model/ball_silo_detect.xml"
if not det_model_path.exists():
    det_model.export(format="openvino", dynamic=True, half=False)
