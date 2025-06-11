from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    url = f"https://lopec.kr/search/search.html?headerCharacterName={nickname}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    # 디버깅: '점수 통계' div 블록만 추출해 전달
    tag = soup.find("span", class_="tag", string="점수 통계")
    if not tag:
        return "DEBUG: '점수 통계' 태그를 못 찾았어요"
    parent_div = tag.find_parent("div")
    if not parent_div:
        parent_div = tag.find_parent()
    html_block = str(parent_div)

    return html_block  # 디버깅용 전체 HTML 반환
