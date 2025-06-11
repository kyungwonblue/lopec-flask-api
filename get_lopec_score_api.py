from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    try:
        url = f'https://lopec.kr/api/ranking?nickname={nickname}'
        headers = {
            'User-Agent': 'Mozilla/5.0',  # 브라우저처럼 보이게
            'Accept': 'application/json',
        }
        response = requests.get(url, headers=headers)
        data = response.json()  # ← 여기서 에러 나면 catch로 넘어감

        if not data:
            return jsonify({'nickname': nickname, 'score': '점수를 찾을 수 없음'})

        score = data[0].get('totalSum', '점수를 찾을 수 없음')
        return jsonify({'nickname': nickname, 'score': score})

    except Exception as e:
        return jsonify({'nickname': nickname, 'score': '오류 발생', 'error': str(e)})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
