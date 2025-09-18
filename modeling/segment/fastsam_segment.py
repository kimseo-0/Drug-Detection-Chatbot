import os
import cv2
import numpy as np
from ultralytics import FastSAM

def enhance_pill_bilateral(img, d=9, sigmaColor=50, sigmaSpace=50, local_gain=0.8, blend=0.6):
    bf = cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)
    gauss = cv2.GaussianBlur(bf, (0, 0), 3.0)
    local = cv2.addWeighted(bf, 1 + local_gain, gauss, -local_gain, 0)
    return cv2.addWeighted(local, blend, img, 1.0 - blend, 0)

def segment_images_with_fastsam(input_dir: str, result_dir: str):
    os.makedirs(result_dir, exist_ok=True)

    # FastSAM 모델 로드
    model_name = "FastSAM-s.pt"
    model = FastSAM(r"C:\Potenup\Drug-Detection-Chatbot\modeling\segment\models\\" + model_name)
    
    # 입력 디렉토리 내 모든 이미지 처리
    for fname in os.listdir(input_dir):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue  # 이미지 확장자만 처리

        source_path = os.path.join(input_dir, fname)

        if not os.path.exists(source_path):
            print(f"Error: {source_path} 경로의 파일을 찾을 수 없습니다.")
            continue

        # 1. 이미지 불러오기
        original_image = cv2.imread(source_path)
        # if original_image is None:
        #     print(f"Error: {source_path} 파일을 불러올 수 없습니다.")
        #     continue
            
        # # 2. 이미지 전처리
        # image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        image = enhance_pill_bilateral(original_image)

        # 3. FastSAM으로 Segmentation 수행
        results = model(image, device="cpu", retina_masks=True, conf=0.8, iou=0.8)
        
        # 'everything' 프롬프트로 모든 객체 마스크 추출
        # masks = results[0].masks.data if hasattr(results[0], "masks") else []

        masks = []
        if hasattr(results[0], "masks") and results[0].masks is not None:
            if hasattr(results[0].masks, "data") and results[0].masks.data is not None:
                masks = results[0].masks.data

        # 4. 마스크 통합 및 배경 제거
        if len(masks) == 0:
            print(f"Info: {fname}에서 객체가 탐지되지 않아 마스크를 생성하지 않습니다.")
            # 저장 경로
            output_fname = os.path.splitext(fname)[0] + ".png"
            output_path = os.path.join(result_dir, output_fname)
            cv2.imwrite(output_path, original_image)
            print(f"Image with transparent background saved to {output_path}")
        else:
            combined_mask = np.zeros(original_image.shape[:2], dtype=np.uint8)
            for mask_tensor in masks:
                mask_array = mask_tensor.cpu().numpy().astype(np.uint8)
                combined_mask = cv2.bitwise_or(combined_mask, mask_array)

            # 배경 제거 및 투명 배경 PNG 저장
            image_rgba = cv2.cvtColor(original_image, cv2.COLOR_BGR2BGRA)
            image_rgba[:, :, 3] = combined_mask * 255

            # 저장 경로
            output_fname = os.path.splitext(fname)[0] + ".png"
            output_path = os.path.join(result_dir, output_fname)
            cv2.imwrite(output_path, image_rgba)
            print(f"Image with transparent background saved to {output_path}")

# 사용 예시
if __name__ == "__main__":
    image_base_path = "C:\Potenup\Drug-Detection-Chatbot\modeling\segment\images/results_yolo_crop/"
    result_base_path = "C:\Potenup\Drug-Detection-Chatbot\modeling\segment\images\\results_fastsam/"
    
    segment_images_with_fastsam(image_base_path, result_base_path)