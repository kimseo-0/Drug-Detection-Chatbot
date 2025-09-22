import json
import os
from drugocr import extract_text
from llm_01_02 import texts_and_image_to_json

if __name__ == "__main__":
    # 테스트할 이미지 경로
    image_path = "C:/Potenup/Drug-Detection-Chatbot/data/medicine_00451.jpeg"

    # 1. OCR
    texts = extract_text(image_path)
    print("📌 OCR 추출 결과:", texts)

    # 2. LLM
    json_result = texts_and_image_to_json(image_path, texts)
    print("📌 LLM JSON 결과:")
    print(json.dumps(json_result, ensure_ascii=False, indent=2))

    # 3. JSON 자동 저장
    # 이미지 파일명에서 확장자 제거 후 output 파일명 생성
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_file = f"output_{base_name}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_result, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON 파일 저장 완료: {output_file}")
