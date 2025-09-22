import json
import ollama
import os

def texts_and_image_to_json(image_path, ordered_texts, model="qwen2-vl:14b"):
    prompt = f"""
    아래는 OCR로 추출된 텍스트 목록입니다:
    {ordered_texts}

    위의 텍스트와 이미지({os.path.basename(image_path)})를 참고하여
    의약품 설명서 형식의 key-value JSON을 만들어주세요.

    조건:
    1. 반드시 JSON만 출력
    2. key는 의미 단위로 추론 (예: "제품명", "성분", "용법", "보관법")
    3. value는 원문을 유지
    """

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt, "images": [image_path]}
        ]
    )

    try:
        return json.loads(response["message"]["content"])
    except Exception as e:
        print("⚠️ JSON 변환 오류:", e)
        return {}
