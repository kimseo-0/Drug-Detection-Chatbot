from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
import os
from io import BytesIO
from PIL import Image
from services import vision, ocr, extract

router = APIRouter(prefix="/pill", tags=["pill"])

SAVE_DIR = "app/uploaded_images"  # 저장 폴더

@router.post("/analyze")
async def analyze_pill(
    file: UploadFile = File(...),
    image_type: str = Form(...),  # "pill" | "package"
):
    content = await file.read()

    # PIL로 로딩 (+ EXIF 회전 보정, 알파 제거)
    img = Image.open(BytesIO(content))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # 저장할 파일명 생성 (타임스탬프 + 원본 파일명)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = os.path.splitext(os.path.basename(file.filename))[0]
    filename = f"{timestamp}_{safe_name}.jpg"  # 원하는 포맷으로 강제
    save_path = os.path.join(SAVE_DIR, filename)

    os.makedirs(SAVE_DIR, exist_ok=True)
    img.save(save_path, format="JPEG", quality=90)

    if image_type not in {"pill", "package"}:
        raise HTTPException(status_code=400, detail="invalid image_type")

    if image_type == "pill":
        # 알약 사진 → 분류기 경로
        cls = vision.classify_pill(content)   # placeholder
        return {"mode": "pill", "classification": cls}

    else:
        # 포장지/설명서 → OCR 경로
        # text_list = ocr.extract_text(save_path)
        # text = ' ,'.join(text_list)
        text = """
    [원료약품 및 분량] 이 약 1캡슐 중 유효성분:두타스테리드(USP)0.5mg ·첨가제(동물유래성분):젤라틴(기원동물:소,사용 부위:가죽) 기타 첨가제:농글리세린,부틸히드록시톨루엔,숙 신산젤라틴,폴리옥실40경화피마자유,프로필렌글 리콜모노라우레이트,폴록사머124,D-소르비톨액 [성상] 무색 투명한 내용물이 들어있는 미황색의 투명한 타원형 연질캡슐 [효능·효과] 양성 전립선 비대증 증상의 개선,급성 요저류 위 험성 감소,양성 전립선 1 비대증과 관련된 수술 필요성 감소, 성인 남성(만18~50세)의 남성형 탈모(androgenetic alopecia)의 치료 [용법·용량] 이 약의 권장용량은 1일 1회 1캡슐(0.5mg)이다. 캡슐 내용물에 노출시 구강 인두점막의 자극을 초래 할 수 있으므로 이 약을 쉽거나 쪼개지 않고 통째로 삼켜 복용해야 한다. 이 약은 식사와 관계없이 복용할 수 있다.신장애 환자 또는 노인 환자에서 이 약의 용량을  조절할 필요는 없다.간장애 환자에게 이 약을 투여한 자료가 없기 때문에 간장애 환자에서의 이 약의 권장용량은 확립되어 있지 요 않다. [사용상의 주의사항] 1.경고 1)여성에게 노출시 남자 태아에 미치는 위험성 이 약은 피부를 통해서 흡수된다.따라서 이 약의 흡수> 가능성과 남자 태아에게 미치는 태자 기형의 위험 가능성 때문에 임신했거나 임신 가능성이 있는 여성이 이 약을 취급해서는 안 된다.또, 여 성은0 이 약을 취급할 때마다 주의해야 하고 누출되는 캡슐 과의 접촉을 피해야 한다. 만약 캡슐이 새어 이 약과 접촉한 경우에는 접촉부위를 즉시들 |물과 비누로 세척해야 한다. 이하 첨부문서 참조 [저장방법] 밀폐용기,30°C이하 보관 [제조의뢰자](주)제뉴원사이언스 세종특별자치시 전의면 큰 산단길 245 [제조자](주)유유제약 충북 제천시 바이오밸리 1로 94
    """
        facts = extract.parse_drug_facts(text, save_path)
        return {"mode": "package", "ocr": {"raw_text": text, "facts": facts}}
