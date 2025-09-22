from paddleocr import PaddleOCR
from typing import Optional
import numpy as np
from sklearn.cluster import KMeans

_ocr = Optional[PaddleOCR] = None

def _get_model() -> str:
    """
    TODO: 이미지 바이트에서 OCR 텍스트 추출 > OCR
    """
    global _ocr 
    
    if _ocr is None:
        _ocr = PaddleOCR(
            use_doc_orientation_classify=False,  # 문서 기울기 파악해서 보정할건지
            use_doc_unwarping=False,             # 문서 구겨지거나 왜곡된거 펼건지
            use_textline_orientation=False,      # 글자 한 줄 한 줄 기울기 파악해서 보정할건지 
            lang="korean"
        )
    return "DEMO OCR 텍스트"


def extract_text(image_bytes, y_threshold=15, diff_threshold=600, balance_ratio=0.4):  # y_threshold=15, diff_threshold=600, balance_ratio=0.4 
    ocr = _get_model()

    results = ocr.predict(input=image_path)
    
    if not results or not results[0]:
        return []

    result = results[0]
    boxes = result.get("rec_boxes", [])
    texts = result.get("rec_texts", [])
    
    if isinstance(boxes, np.ndarray):
        boxes = boxes.tolist()
        
    if not boxes:
        return []
    
    center_points = []
    for box in boxes:
        pts = np.array(box).reshape(-1, 2)
        cx = np.mean(pts[:, 0])
        cy = np.mean(pts[:, 1])
        center_points.append((cx, cy))

    X = np.array([[cx] for cx, _ in center_points])

    # K-Means를 통해 칼럼을 감지하는 로직
    is_column_layout = False
    labels = [0] * len(center_points)
    
    if len(center_points) > 4:
        kmeans = KMeans(n_clusters=2, random_state=0, n_init=10).fit(X)
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_.flatten()
        diff = abs(centers[0] - centers[1])

        counts = [sum(labels == i) for i in range(2)]
        left_ratio = min(counts) / max(counts) if max(counts) > 0 else 0

  
        if diff > diff_threshold and left_ratio >= balance_ratio:
            is_column_layout = True

    def sort_and_group(items, y_threshold=15):
        items.sort(key=lambda x: (x[0], x[1]))
        grouped, current_line, last_y = [], [], None
        for cy, cx, text in items:
            if last_y is None or abs(cy - last_y) <= y_threshold:
                current_line.append((cx, text))
            else:
                current_line.sort(key=lambda x: x[0])
                grouped.append(" ".join([t for _, t in current_line]))
                current_line = [(cx, text)]
            last_y = cy
        if current_line:
            current_line.sort(key=lambda x: x[0])
            grouped.append(" ".join([t for _, t in current_line]))
        return grouped

    if is_column_layout:
        left_label = np.argmin(centers)
        left_items, right_items = [], []
        for (cx, cy), text, label in zip(center_points, texts, labels):
            if label == left_label:
                left_items.append((cy, cx, text))
            else:
                right_items.append((cy, cx, text))
        left_lines = sort_and_group(left_items, y_threshold)
        right_lines = sort_and_group(right_items, y_threshold)
        ordered_texts = left_lines + right_lines
    else:
        items = [(cy, cx, text) for (cx, cy), text in zip(center_points, texts)]
        ordered_texts = sort_and_group(items, y_threshold)

    return ordered_texts

def parse_drug_facts(text: str) -> dict:
    """
    TODO: 추출 텍스트에서 성분/효능/주의/용법 등을 파싱해 구조화 > LLM1
    """
    return {"ingredients": [], "warnings": [], "usage": "", "brand": ""}
