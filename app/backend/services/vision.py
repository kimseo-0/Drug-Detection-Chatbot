def load_model():
    pass  # TODO: 모델 로딩

def detect_pills(image):
    pass  # TODO: 알약 탐지 > drug seg

def classify_pill(image_bytes: bytes) -> dict:
    """
    TODO: 이미지 바이트를 받아 알약 분류 결과 반환
    예: {"label": "조피스타정", "score": 0.92, "candidates":[...]}
    """
    return {"label": "DEMO_PILL", "score": 0.99, "candidates": []}
