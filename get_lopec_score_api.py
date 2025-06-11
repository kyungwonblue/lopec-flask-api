from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    url = "https://api.lopec.kr/api/character/stats"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
        'Origin': 'https://lopec.kr',
        'Referer': 'https://lopec.kr/'
    }
    payload = {
        "nickname": nickname
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)

        if resp.status_code != 200:
            return jsonify({'nickname': nickname, 'score': 'API 응답 오류', 'error': resp.status_code})

        data = resp.json()

        if not isinstance(data, list) or not data:
            return jsonify({'nickname': nickname, 'score': '데이터 없음'})

        total_sum = data[0].get('totalSum')
        if total_sum is None:
            return jsonify({'nickname': nickname, 'score': '점수를 찾을 수 없음'})

        return jsonify({'nickname': nickname, 'score': total_sum})

    except Exception as e:
        return jsonify({'nickname': nickname, 'score': '오류 발생', 'error': str(e)})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
