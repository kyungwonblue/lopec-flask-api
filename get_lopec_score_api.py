from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time  # 명시적 대기용

app = Flask(__name__)

def get_lopec_score(nickname):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://lopec.kr/search/search.html?headerCharacterName={nickname}"
        driver.get(url)

        driver.implicitly_wait(10)
        html = driver.page_source
        with open("debug_lopec.html", "w", encoding="utf-8") as f:
            f.write(html)

        soup = BeautifulSoup(html, 'html.parser')

        score_spans = soup.select('span.text')
        for span in score_spans:
            text = span.text.strip()
            if text.replace('.', '', 1).isdigit():  # 점수값인지 확인
                return text

        return "점수를 찾을 수 없음"
    finally:
        driver.quit()

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname')
    if not nickname:
        return jsonify({'error': 'nickname 파라미터가 필요합니다.'}), 400

    score = get_lopec_score(nickname)
    return jsonify({'nickname': nickname, 'score': score})

if __name__ == "__main__":
    app.run(debug=True)
