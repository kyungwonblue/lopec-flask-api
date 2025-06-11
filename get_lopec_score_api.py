from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_score', methods=['GET'])
def get_score():
    nickname = request.args.get('nickname', '')
    character_class = request.args.get('characterClass', '')
    total_status = request.args.get('totalStatus', '')
    status_special = request.args.get('statusSpecial', '')
    status_haste = request.args.get('statusHaste', '')

    # 필수 파라미터가 빠졌는지 확인
    if not all([nickname, character_class, total_status, status_special, status_haste]):
        return jsonify({
            'nickname': nickname,
            'score': '필수 파라미터 누락'
        }), 400

    url = "https://api.lopec.kr/api/character/stats"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
        'Origin': 'https://lopec.kr',
        'Referer': 'https://lopec.kr/'
    }
    payload = {
        "nickname": nickname,
        "characterClass": character_class,
        "totalStatus": int(total_status),
        "statusSpecial": int(status_special),
        "statusHaste": int(status_haste)
    }

    try:
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()  # 200 아니면 예외 발생

        data = resp.json()
        if isinstance(data, list) and len(data) > 0:
            score = data[0].get('totalSum', '점수를 찾을 수 없음')
            return jsonify({'nickname': nickname, 'score': score})
        else:
            return jsonify({'nickname': nickname, 'score': '점수를 찾을 수 없음'})

    except Exception as e:
        return jsonify({
            'nickname': nickname,
            'score': '오류 발생',
            'error': str(e)
        }), 500

# Render 배포용 설정
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
