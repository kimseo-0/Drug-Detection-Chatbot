from paddleocr import PaddleOCR
from typing import Optional
import numpy as np
from sklearn.cluster import KMeans
import base64
import torch
from transformers import AutoProcessor, AutoTokenizer, AutoModelForVision2Seq
from transformers import BitsAndBytesConfig

model_name = "NCSOFT/VARCO-VISION-2.0-1.7B"
processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)

quantization_config = BitsAndBytesConfig(
    load_in_8bit = True,
    load_in_4bit = False,
    lim_int8_threshold = 6.0,
    lim_int8_has_fp16_weight = False,

)

def _get_model():
    global _model 
    
    if _model is None:
        _model = AutoModelForVision2Seq.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            dtype=torch.bfloat16,   # torch_dtype -> dtype
        )

    return _model

def parse_drug_facts(ocr_texts: str, image_path: str) -> dict:
    """
    TODO: 추출 텍스트에서 성분/효능/주의/용법 등을 파싱해 구조화 > LLM1
    """

    model = _get_model()

    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    system_prompt = """
    당신은 보수적인 약학 전문가입니다. 약학 전문가로서, 
    사용자가 제공한 이미지와 OCR 텍스트 데이터 2가지 모두 확인해서 이미지에 적힌 정보를 정확하게 추출하는 역할을 합니다.

    규칙:
    - 제공된 데이터에 없는 항목은 **반드시 "없음"이라고 작성**할 것. 
    - 예측이나 추론을 하지 말고, 텍스트를 줄이지 말고 **원본 텍스트를 그대로 작성**할 것. 
    - **제품명**: 약의 **제품명**은 별도로 표기된 경우에만 추출하며, '원료약품 및 분량', '성분/함량' 등 **원료나 성분을 설명하는 해당 아래에 있는 텍스트는 제품명으로 간주하지 않습니다**. 
    - 제품명이 없으면 "없음"으로 작성하십시오. 
    - 성분/함량 ',' 기준으로 나누어 각각 항목으로 처리할 것. 줄바꿈 등으로 잘린 경우는 **반드시 붙여쓰기하여** 원래 단어 그대로 복원할 것. 
    - 첨가물/첨가제 ',' 기준으로 나누어 각각 항목으로 처리할 것. 줄바꿈 등으로 잘린 경우는 **반드시 붙여쓰기하여** 원래 단어 그대로 복원할 것. 
    - 출력은 반드시 JSON 형식만 출력하고, 그 외 텍스트(설명, 문장)는 절대 포함하지 말 것. 
    - **효능/효과**: '효능' 또는 '효과'로 명시된 모든 내용을 **하나도 빠짐없이** 모든 리스트를 작성하십시오.
    - OCR 줄바꿈이나 잘림으로 인해 분리된 단어는 반드시 이어 붙여 원래 단어 그대로 복원할 것.
    - JSON의 각 key는 반드시 아래 구조를 따를 것

    [출력형식] 
    {{ 
        '제품명' : "제품의 이름, 없으면 없다고 작성할 것", 
        '성분/함량' : "제품의 각 성분, 유효성분, 함량에 대한 튜플(성분명, 함량)들의 리스트, 없으면 없다고 작성할 것" 
        '첨가물' : "제품의 첨가물/첨가제들의 리스트, 없으면 없다고 작성할 것", 
        '제형/성상' : "제형, 성상, 없으면 없다고 작성할 것", 
        'KPIC/ATC' : 'KPIC/A과C에 대한 리스트, 없으면 없다고 작성할 것", 
        '구분' : "구분, 없으면 없다고 작성할 것" 
        '효능' : "여러가지 효능/효과에 대한 모든 리스트, 없으면 없다고 작성할 것", 
        '용법' : "여러가지 용법에 대한 리스트, 없으면 없다고 작성할 것", 
        '주의사항' : "주의사항 리스트, 없으면 없다고 작성할 것" 
    }}
    """

    messages = [
        [
            {
                "role": "system",
                "content":[{"type": "text", "text": system_prompt},]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": ocr_texts},  # "text": ocr_texts 와 "text" : f"{ocr_texts}" 같은 표현
                    {
                        "type": "image",
                        "source_type": "base64",
                        "data": "{image_data}",
                        "mime_type": "image/jpeg",

                    }

                ]

            
            }
        ]
    ]

    # 입력 데이터 토크나이징하기 processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True) 
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt = True,
        tokenize = True,
        return_dict = True,
        return_tensors = "pt",
    ).to(model.device, torch.float16)
    generate_ids = model.generate(
        **inputs, 
        max_new_tokens=1024,
        temperature=0.1,    # 낮출수록 보수적이고 일관된 답변 생성 
        top_p=0.1,          # 높일수록 다양한 단어 선택, 낮추면 더 보수적
        do_sample=True,     # 샘플링 활성화
        )

    generate_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generate_ids)
    ]
    output = processor.decode(generate_ids_trimmed[0], skip_special_tokens=True)
    return output
