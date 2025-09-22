from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services import vision, ocr

router = APIRouter(prefix="/pill", tags=["pill"])

@router.post("/analyze")
async def analyze_pill(
    file: UploadFile = File(...),
    image_type: str = Form(...),  # "pill" | "package"
):
    content = await file.read()

    if image_type not in {"pill", "package"}:
        raise HTTPException(status_code=400, detail="invalid image_type")

    if image_type == "pill":
        # 알약 사진 → 분류기 경로
        # (필요시 detect → crop → classify 파이프라인으로 확장)
        cls = vision.classify_pill(content)   # placeholder
        return {"mode": "pill", "classification": cls}

    else:
        # 포장지/설명서 → OCR 경로
        text = ocr.extract_text(content, lang="ko")
        facts = ocr.parse_drug_facts(text)
        return {"mode": "package", "ocr": {"raw_text": text, "facts": facts}}
