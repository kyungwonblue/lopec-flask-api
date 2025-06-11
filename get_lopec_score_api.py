from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    url = f"https://lopec.kr/api/character/ranking?nickname={nickname}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()

        if data and isinstance(data, list) and 'totalSum' in data[0]:
            score = round(float(data[0]['totalSum']), 2)  # 소수점 둘째 자리까지만 표시
            return jsonify({'nickname': nickname, 'score': score})
        else:
            return jsonify({'nickname': nickname, 'score': '점수를 찾을 수 없음'})
    except Exception as e:
        return jsonify({'nickname': nickname, 'score': '오류 발생', 'error': str(e)})
