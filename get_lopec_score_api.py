from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_lopec_score(nickname):
    url = f"https://lopec.kr/search/search.html?headerCharacterName={nickname}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    # '점수 통계' 섹션을 찾음
    tags = soup.select("span.tag")
    for tag in tags:
        if tag.text.strip() == "점수 통계":
            parent = tag.find_parent("div")
            if parent:
                spans = parent.select("span.text")
                for span in spans:
                    text = span.text.strip().replace(",", "")
                    try:
                        score = float(text)
                        return str(score)
                    except ValueError:
                        continue
    return "점수를 찾을 수 없음"

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    score = get_lopec_score(nickname)
    return jsonify({'nickname': nickname, 'score': score})

# Render 포트 바인딩
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
