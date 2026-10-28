import os
import base64
import cv2
import numpy as np

from ultralytics import YOLO
from django.conf import settings

from .heatmap import generate_eigen_cam

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "AIModel",
    "best.pt"
)
PERSON_MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "AIModel",
    "yolov8n.pt"
)

model = YOLO(MODEL_PATH)
person_model = YOLO(PERSON_MODEL_PATH)


class PersonDetectedError(ValueError):
    """Raised when a frame contains a person instead of a plant target."""


def _reject_person_frames(source):
    """Prevent the disease model from assigning plant labels to people."""
    result = person_model.predict(source=source, classes=[0], conf=0.40, verbose=False)[0]
    if result.boxes is not None and len(result.boxes) > 0:
        raise PersonDetectedError(
            "A person was detected. Point the camera at one leaf, nut, bud, or trunk area without people in the frame."
        )


def _best_detection(result):
    """Return the highest-confidence detection from a YOLO result."""
    disease = "No_Detection"
    confidence = None

    if result.boxes is not None and len(result.boxes) > 0:
        best_box = max(result.boxes, key=lambda box: float(box.conf[0]))
        class_id = int(best_box.cls[0])
        confidence = float(best_box.conf[0]) * 100
        disease = result.names[class_id]

    return disease, round(confidence, 2) if confidence is not None else None


def detect_disease(image_path):

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    _reject_person_frames(image_path)

    # -------------------------
    # Disease prediction
    # -------------------------

    results = model.predict(
        source=image_path,
        conf=0.25,
        verbose=False
    )

    result = results[0]

    # -------------------------
    # Save Prediction Image
    # -------------------------

    prediction_folder = os.path.join(
        settings.MEDIA_ROOT,
        "predictions"
    )

    os.makedirs(
        prediction_folder,
        exist_ok=True
    )

    filename = os.path.basename(image_path)

    prediction_path = os.path.join(
        prediction_folder,
        filename
    )

    prediction_image = result.plot()

    cv2.imwrite(
        prediction_path,
        prediction_image
    )

    # -------------------------
    # Disease prediction
    # -------------------------

    disease, confidence = _best_detection(result)

    # -------------------------
    # Create EigenCAM only when YOLO made a valid detection
    # -------------------------

    heatmap_folder = os.path.join(
        settings.MEDIA_ROOT,
        "heatmaps"
    )

    os.makedirs(
        heatmap_folder,
        exist_ok=True
    )

    heatmap_path = None
    if confidence is not None:
        heatmap_path = os.path.join(
            heatmap_folder,
            filename
        )
        generate_eigen_cam(
            image_path,
            model.model,
            heatmap_path
        )

    return (
        disease,
        confidence,
        prediction_path,
        heatmap_path
    )


def detect_live_frame(uploaded_file):
    """Analyze one in-memory camera frame without saving it to user history."""
    image_bytes = uploaded_file.read()
    image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("The camera frame could not be read.")

    _reject_person_frames(image)
    result = model.predict(source=image, conf=0.25, verbose=False)[0]
    disease, confidence = _best_detection(result)

    success, encoded_image = cv2.imencode('.jpg', result.plot())
    if not success:
        raise ValueError("The annotated camera frame could not be created.")

    return disease, confidence, base64.b64encode(encoded_image.tobytes()).decode('ascii')
