from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_lopec_score(nickname):
    url = f"https://lopec.kr/search/search.html?headerCharacterName={nickname}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # '점수 통계' 태그를 찾은 후, 그 다음 'text' 클래스 값 추출
    tag_elements = soup.find_all("span", class_="tag")
    for tag in tag_elements:
        if "점수 통계" in tag.text:
            score_element = tag.find_parent().find("span", class_="text")
            if score_element:
                return score_element.text.strip()
    return None

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    score = get_lopec_score(nickname)
    if score:
        return jsonify({'nickname': nickname, 'score': score})
    else:
        return jsonify({'nickname': nickname, 'score': '점수를 찾을 수 없음'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Render가 환경변수로 포트를 지정함
    app.run(host='0.0.0.0', port=port)

