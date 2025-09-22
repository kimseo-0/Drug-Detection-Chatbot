import os
import cv2
import numpy as np
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

def crop_image_with_yolo(input_dir: str,
                         output_dir: str,
                         model_path: str,
                         conf: float = 0.5,
                         pad: int = 8,
                         apply_enhance: bool = True):
    os.makedirs(output_dir, exist_ok=True)

    # YOLO 모델 한 번만 로드
    model = YOLO(model_path)

    exts = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    for fname in os.listdir(input_dir):
        if not fname.lower().endswith(exts):
            continue

        image_path = os.path.join(input_dir, fname)
        image = cv2.imread(image_path)
        if image is None:
            print(f"[Skip] 이미지 로드 실패: {image_path}")
            continue

        # 선택 전처리
        proc = enhance_pill_bilateral(image) if apply_enhance else image

        # 예측 (numpy 배열 입력 가능)
        results = model.predict(source=proc, conf=conf, verbose=False)

        # 파일명/확장자 분리
        stem, _ = os.path.splitext(fname)
        saved = 0

        for r in results:
            if r.boxes is None or r.boxes.xyxy is None or len(r.boxes) == 0:
                continue

            # 박스: (N, 4) [x1, y1, x2, y2]
            boxes = r.boxes.xyxy.cpu().numpy()
            for i, (x1, y1, x2, y2) in enumerate(boxes):
                crop = crop_image(image, x1, y1, x2, y2, pad=pad)  # 원본 기준 크롭
                if crop is None or crop.size == 0:
                    continue
                out_name = f"{stem}_crop_{i+1}.jpg"
                out_path = os.path.join(output_dir, out_name)
                cv2.imwrite(out_path, crop)
                saved += 1

        if saved == 0:
            print(f"[Info] 객체 없음: {fname}")
        else:
            print(f"[OK] {fname}: {saved}개 크롭 저장")

    print(f"크롭 결과가 '{output_dir}' 폴더에 저장되었습니다.")

if __name__ == "__main__":
    image_base_path = "C:\Potenup\Drug-Detection-Chatbot\modeling\segment\images/original/"
    result_base_path = "C:\Potenup\Drug-Detection-Chatbot\modeling\segment\images\\results_yolo_crop/"
    best_model_path = r"C:\\Potenup\Drug-Detection-Chatbot\\modeling\segment\\runs\\pill-detect-1\\train\weights\best.pt"

    crop_image_with_yolo(
        input_dir=image_base_path,
        output_dir=result_base_path,
        model_path=best_model_path,
        conf=0.5,
        pad=8,
        apply_enhance=True
    )
