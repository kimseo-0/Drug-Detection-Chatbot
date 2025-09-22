import requests

BASE_URL = "http://localhost:8000"

def analyze_pill(file_obj, image_type: str):
    url = f"{BASE_URL}/pill/analyze"
    files = {"file": (file_obj.name, file_obj, "application/octet-stream")}
    data = {"image_type": image_type}  # 👈 타입 함께 전송
    r = requests.post(url, files=files, data=data, timeout=60)
    if r.ok:
        return r.json()
    raise Exception(f"{r.status_code} {r.text}")
