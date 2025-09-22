import requests

BASE_URL = "http://localhost:8000"  # FastAPI 주소

def save_user_profile(profile: dict):
    url = f"{BASE_URL}/user/info"
    r = requests.post(url, json=profile)
    if r.ok:
        return r.json()
    raise Exception(f"API Error: {r.status_code} {r.text}")

def get_user_profile(user_id: str):
    url = f"{BASE_URL}/user/info/{user_id}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    if r.status_code == 404:
        return None
    raise Exception(f"API Error: {r.status_code} {r.text}")

def analyze_pill(image, image_type):
    pass

def check_drug(payload):
    pass

def ask_chat(query):
    pass
