import shutil
from pathlib import Path

# 경로 설정
BASE_DIR = Path(
    "C:/project_sep/data/166.약품식별_인공지능_개발을_위한_경구약제_이미지_데이터/01.데이터/2.Validation"
)

IMG_SRC = BASE_DIR / "원천데이터"
JSON_SRC = BASE_DIR / "라벨링데이터"

IMG_FLAT = Path("C:/project_sep/data/_flat_images")
JSON_FLAT = Path("C:/project_sep/data/_flat_json")

IMG_FLAT.mkdir(parents=True, exist_ok=True)
JSON_FLAT.mkdir(parents=True, exist_ok=True)


def flatten_files(src_dir, img_out, json_out):
    # 전체 파일 수 계산
    all_files = list(src_dir.rglob("*"))
    total = len([f for f in all_files if f.is_file()])
    count = 0

    for path in all_files:
        if path.is_file():
            count += 1
            if path.suffix.lower() in [".jpg", ".png"]:
                k_code = path.parent.name  # k-어쩌고 이게
                new_name = f"{k_code}_{path.name}"
                shutil.move(str(path), str(img_out / new_name))
            elif path.suffix.lower() == ".json":
                k_code = path.parent.name
                new_name = f"{k_code}_{path.name}"
                shutil.move(str(path), str(json_out / new_name))

            # 진행 상황 출력
            if count % 100 == 0 or count == total:
                print(f"진행 중: {count}/{total} 파일 이동 완료")

    print(f"Flatten 완료: 총 {total}개 파일 이동 from {src_dir.name}")


# 실행 (원천데이터 + 라벨링데이터 모두)
flatten_files(IMG_SRC, IMG_FLAT, JSON_FLAT)
flatten_files(JSON_SRC, IMG_FLAT, JSON_FLAT)
