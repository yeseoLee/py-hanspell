import tempfile
import os
import re
import requests


class TokenManager:
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = tempfile.gettempdir()

        # 패키지명으로 고정된 파일명 사용
        self.filename = os.path.join(base_dir, "token.txt")

        # 파일이 없으면 빈 파일 생성
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                f.write("")

    def read_token(self):
        try:
            with open(self.filename, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""

    def update_token(self):
        url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=네이버+맞춤법+검사기"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Referer": "https://search.naver.com/",
        }

        res = requests.get(
            url,
            headers=headers,
        )
        html_text = res.text

        match = re.search(r'passportKey=([^&"}]+)', html_text)
        if not match:
            raise Exception("update_token error: passportKey not found")
        TOKEN = match.group(1)

        with open(self.filename, "w") as f:
            f.write(TOKEN)
        return TOKEN
