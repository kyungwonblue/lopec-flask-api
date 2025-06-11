from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_lopec_score(nickname):
    url = f"https://lopec.kr/search/search.html?headerCharacterName={nickname}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    # '점수 통계' 바로 아래의 <span class="text">를 찾음
    tags = soup.select("span.tag")
    for tag in tags:
        if tag.text.strip() == "점수 통계":
            parent = tag.find_parent("div")
            if parent:
                text_span = parent.select_one("span.text")
                if text_span:
                    return text_span.text.strip()

    return "점수를 찾을 수 없음"

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    score = get_lopec_score(nickname)
    return jsonify({'nickname': nickname, 'score': score})

# Render용 포트 바인딩
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
