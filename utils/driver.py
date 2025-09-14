import random, time
from itertools import cycle
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import json
import requests

PROXIES = [
    "http://user:pass@1.2.3.4:3128",
    "http://user:pass@5.6.7.8:8000",
]
UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]
proxy_pool = cycle(PROXIES)

def make_driver():
    opts = Options()
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("accept-language=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36")
    driver = uc.Chrome(options=opts)
    return driver

def polite_sleep(base=1):
    time.sleep(base + random.random() * base)

def get_status_code(driver, url):
    logs = driver.get_log("performance")
    for entry in logs:
        msg = json.loads(entry["message"])["message"]
        if msg["method"] == "Network.responseReceived":
            status = msg["params"]["response"]["status"]
            resp_url = msg["params"]["response"]["url"]
            if resp_url.startswith(url):  # 메인 요청의 응답만 체크
                return status
    return None

def move_url(driver , url, max_retry=5, sleep_sec=10):
    for attempt in range(1, max_retry + 1):    
        driver.get(url)

        status = get_status_code(driver, url)
        print(status)
        if status == 200:
            return driver  # driver 반환해서 이후 크롤링에 사용
        else:
            print(f"[시도 {attempt}] 실패: {status}, 드라이버 재시작 후 {sleep_sec}초 대기")
            if driver:
                driver.quit()  # 이전 드라이버 닫기
            time.sleep(sleep_sec)
            driver = make_driver()

    raise Exception("최대 횟수 초과")
