import os
import json
import pandas as pd
from pathlib import Path

# 경로 설정
JSON_FLAT = Path("C:/project_sep/data/_flat_json")
CSV_OUT = Path("C:/project_sep/data/annotations.csv")

rows = []

# JSON -> CSV
for json_file in JSON_FLAT.glob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    img_info = data.get("images", [{}])[0]
    img_name = img_info.get(
        "file_name", json_file.stem + ".jpg"
    )  # json 파일의 file_name 과 동일한 클래스 이름임.
    img_w = img_info.get("width", 0)
    img_h = img_info.get("height", 0)

    # 이미지 메타데이터 (json 내 images 필드)
    meta = {
        "image": img_name,
        "width": img_w,
        "height": img_h,
        "drug_N": img_info.get("drug_N", ""),
        "drug_S": img_info.get("drug_S", ""),
        "back_color": img_info.get("back_color", ""),
        "drug_dir": img_info.get("drug_dir", ""),
        "light_color": img_info.get("light_color", ""),
        "camera_la": img_info.get("camera_la", ""),
        "camera_lo": img_info.get("camera_lo", ""),
        "size": img_info.get("size", ""),
        "dl_idx": img_info.get("dl_idx", ""),
        "dl_mapping_code": img_info.get("dl_mapping_code", ""),
        "dl_name": img_info.get("dl_name", ""),
        "dl_name_en": img_info.get("dl_name_en", ""),
        "dl_material": img_info.get("dl_material", ""),
        "dl_company": img_info.get("dl_company", ""),
        "item_seq": img_info.get("item_seq", ""),
        "di_class_no": img_info.get("di_class_no", ""),
        "di_etc_otc_code": img_info.get("di_etc_otc_code", ""),
        "chart": img_info.get("chart", ""),
        "drug_shape": img_info.get("drug_shape", ""),
        "thick": img_info.get("thick", ""),
        "leng_long": img_info.get("leng_long", ""),
        "leng_short": img_info.get("leng_short", ""),
        "print_front": img_info.get("print_front", ""),
        "print_back": img_info.get("print_back", ""),
        "color_class1": img_info.get("color_class1", ""),
        "color_class2": img_info.get("color_class2", ""),
        "form_code_name": img_info.get("form_code_name", ""),
    }

    # ann 부분
    for ann in data.get("annotations", []):
        bbox = ann.get("bbox", [])
        row = meta.copy()

        if bbox and len(bbox) == 4:
            row.update(
                {
                    "bbox_x": bbox[0],
                    "bbox_y": bbox[1],
                    "bbox_w": bbox[2],
                    "bbox_h": bbox[3],
                    "bbox_valid": True,
                }
            )
        else:
            # bbox가 없거나 잘못된 경우
            row.update(
                {
                    "bbox_x": None,
                    "bbox_y": None,
                    "bbox_w": None,
                    "bbox_h": None,
                    "bbox_valid": False,
                }
            )
        rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(CSV_OUT, index=False, encoding="utf-8-sig")

print(f"✅ CSV 저장 완료: {CSV_OUT}, 총 {len(df)} 라벨")
print("컬럼:", list(df.columns))
