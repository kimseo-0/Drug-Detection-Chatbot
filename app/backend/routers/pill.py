from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
import os
from services import vision, ocr, extract

router = APIRouter(prefix="/pill", tags=["pill"])

SAVE_DIR = "app/uploaded_images"  # 저장 폴더

@router.post("/analyze")
async def analyze_pill(
    file: UploadFile = File(...),
    image_type: str = Form(...),  # "pill" | "package"
):
    content = await file.read()
    
    # 저장할 파일명 생성 (타임스탬프 + 원본 파일명)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    save_path = os.path.join(SAVE_DIR, filename)

    # 로컬에 저장
    with open(save_path, "wb") as f:
        f.write(content)

    if image_type not in {"pill", "package"}:
        raise HTTPException(status_code=400, detail="invalid image_type")

    if image_type == "pill":
        # 알약 사진 → 분류기 경로
        cls = vision.classify_pill(content)   # placeholder
        return {"mode": "pill", "classification": cls}

    else:
        # 포장지/설명서 → OCR 경로
        text_list = ocr.extract_text(save_path, lang="ko")
        text = ' '.join(text_list)
        facts = extract.parse_drug_facts(text)
        return {"mode": "package", "ocr": {"raw_text": text, "facts": facts}}
