def extract_text(image_bytes: bytes, lang: str = "ko") -> str:
    """
    TODO: 이미지 바이트에서 OCR 텍스트 추출 > OCR
    """
    return "DEMO OCR 텍스트"

def parse_drug_facts(text: str) -> dict:
    """
    TODO: 추출 텍스트에서 성분/효능/주의/용법 등을 파싱해 구조화 > LLM1
    """
    return {"ingredients": [], "warnings": [], "usage": "", "brand": ""}
