import os
import cv2
import numpy as np
from typing import List, Optional
from ultralytics import YOLO

def enhance_pill_bilateral(img, d=9, sigmaColor=50, sigmaSpace=50, local_gain=0.8, blend=0.6):
    bf = cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)
    gauss = cv2.GaussianBlur(bf, (0, 0), 3.0)
    local = cv2.addWeighted(bf, 1 + local_gain, gauss, -local_gain, 0)
    return cv2.addWeighted(local, blend, img, 1.0 - blend, 0)

def crop_image(image, x1, y1, x2, y2, pad: int = 0):
    h, w = image.shape[:2]
    x1 = max(0, int(x1) - pad)
    y1 = max(0, int(y1) - pad)
    x2 = min(w, int(x2) + pad)
    y2 = min(h, int(y2) + pad)
    if x2 <= x1 or y2 <= y1:
        return None
    return image[y1:y2, x1:x2]

YOLO_WEIGHTS = os.getenv("YOLO_WEIGHTS", r"C:\\Potenup\Drug-Detection-Chatbot\\modeling\segment\\runs\\pill-detect-1\\train\weights\best.pt")
YOLO_CONF = float(os.getenv("YOLO_CONF", "0.5"))
YOLO_PAD = int(os.getenv("YOLO_PAD", "8"))
APPLY_ENHANCE = os.getenv("YOLO_APPLY_ENHANCE", "true").lower() in {"1", "true", "yes"}

_model: Optional[YOLO] = None

def _get_model() -> YOLO:
    """YOLO 모델을 1회만 로드해 재사용"""
    global _model
    if _model is None:
        if not os.path.exists(YOLO_WEIGHTS):
            raise FileNotFoundError(f"YOLO weights not found: {YOLO_WEIGHTS}")
        _model = YOLO(YOLO_WEIGHTS)
    return _model

def _bytes_to_bgr(image_bytes: bytes) -> np.ndarray:
    """UploadFile.read() 결과(bytes) → OpenCV BGR 이미지로 디코딩"""
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode image bytes")
    return img

def detect_pills(image_bytes: bytes) -> List[np.ndarray]:
    """
    입력: 이미지 바이트 (예: FastAPI UploadFile.read())
    출력: YOLO로 탐지한 바운딩박스들을 원본 기준으로 크롭한 이미지 리스트(np.ndarray)
    """
    img = _bytes_to_bgr(image_bytes)

    proc = enhance_pill_bilateral(img) if APPLY_ENHANCE else img

    model = _get_model()
    results = model.predict(source=proc, conf=YOLO_CONF, verbose=False)

    crops: List[np.ndarray] = []

    for r in results:
        if getattr(r, "boxes", None) is None or getattr(r.boxes, "xyxy", None) is None or len(r.boxes) == 0:
            continue

        boxes = r.boxes.xyxy.cpu().numpy()  # shape: (N, 4) [x1, y1, x2, y2]
        for (x1, y1, x2, y2) in boxes:
            crop = crop_image(img, x1, y1, x2, y2, pad=YOLO_PAD)  # 원본 기준 크롭
            if crop is not None and crop.size > 0:
                crops.append(crop)

    return crops