from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    url = f"https://lopec.kr/search/search.html?headerCharacterName={nickname}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    spans = soup.select('span.text')
    for span in spans:
        score = span.text.strip().replace(',', '')
        try:
            float(score)
            return jsonify({'nickname': nickname, 'score': score})
        except ValueError:
            continue
    return jsonify({'nickname': nickname, 'score': '점수를 찾을 수 없음'})

