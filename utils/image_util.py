import requests

def download_image(url: str, save_path: str, chunk_size: int = 1024) -> bool:
    try:
        resp = requests.get(url, stream=True, timeout=10)
        if resp.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size):
                    if chunk:  # keep-alive chunks 건너뛰기
                        f.write(chunk)
            print(f"다운로드 완료: {save_path}")
            return True
        else:
            print(f"다운로드 실패: HTTP {resp.status_code}")
            return False
    except Exception as e:
        print(f"오류 발생: {e}")
        return False