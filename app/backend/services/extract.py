from paddleocr import PaddleOCR
from typing import Optional
import numpy as np
from sklearn.cluster import KMeans
import base64
import torch
from transformers import AutoProcessor, AutoTokenizer, AutoModelForVision2Seq
from transformers import BitsAndBytesConfig
from services import openai
import json 

def parse_drug_facts(ocr_texts: str, image_path: str) -> dict:
    """
    TODO: 추출 텍스트에서 성분/효능/주의/용법 등을 파싱해 구조화 > LLM1
    """

    system_prompt = """
    당신은 보수적인 약학 전문가입니다. 약학 전문가로서, 
    사용자가 제공한 OCR 텍스트 데이터 확인해서 JSON 형식의 서식을 작성해 주세요.


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
    answer = openai.chat(system_prompt, "user")

    answer = json.loads(answer.choices[0].message.content)
    return answer
