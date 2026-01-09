import os
import cv2
import numpy as np
from typing import List, Optional
from ultralytics import YOLO
import base64
from services import detect

def classify_pill(image_bytes: bytes) -> dict:
    """
    TODO: 이미지 바이트를 받아 알약 분류 결과 반환
    예: {"label": "조피스타정", "score": 0.92, "candidates":[...]}
    """
    images_ndarray = detect.detect_pills(image_bytes)

    # 분류모델 가져와서
    # 예측하고
    # 결과를 result 담아

    # 아래는 크롭된 이미지를 스트림릿으로 보내는 코드
    images_b64 = []
    for img in images_ndarray:
        # cv2.imencode로 메모리에 JPEG 저장
        success, buf = cv2.imencode(".jpg", img)
        if not success:
            continue
        b64 = base64.b64encode(buf.tobytes()).decode("utf-8")
        images_b64.append(b64)

    result = {"label": "DEMO_PILL", "score": 0.99, "candidates": [], "images": images_b64}
    return result
