from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/get_score', methods=['GET'])
def get_score():
    nickname = request.args.get('nickname')
    character_class = request.args.get('characterClass')
    total_status = request.args.get('totalStatus')
    status_special = request.args.get('statusSpecial')
    status_haste = request.args.get('statusHaste')

    print(f"▶️ 받은 요청 - 닉네임: {nickname}, 클래스: {character_class}, 총스탯: {total_status}, 특성: {status_special}, 가속: {status_haste}", flush=True)

    if not all([nickname, character_class, total_status, status_special, status_haste]):
        print("❌ 필수 파라미터 누락", flush=True)
        return jsonify({"error": "Missing required parameters", "nickname": nickname, "score": "오류 발생"})

    try:
        url = 'https://api.lopec.kr/api/character/stats'
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
        payload = {
            'nickname': nickname,
            'characterClass': character_class,
            'totalStatus': int(total_status),
            'statusSpecial': int(status_special),
            'statusHaste': int(status_haste)
        }

        print(f"📤 Lopec API 요청 전송: {url}", flush=True)
        print(f"📦 Payload: {payload}", flush=True)

        response = requests.post(url, headers=headers, json=payload)
        print(f"📥 응답 상태 코드: {response.status_code}", flush=True)

        if response.status_code != 200:
            print("❌ 응답 코드 200 아님", flush=True)
            return jsonify({"error": "Lopec API 응답 실패", "nickname": nickname, "score": "API 응답 오류"})

        data = response.json()
        print(f"📄 Lopec API 응답 데이터: {data}", flush=True)

        if isinstance(data, list) and len(data) > 0:
            score = data[0].get('totalSum')
            if score:
                score = round(score, 2)
                print(f"✅ 점수 추출 성공: {score}", flush=True)
                return jsonify({"nickname": nickname, "score": score})
            else:
                print("❌ totalSum 없음", flush=True)
                return jsonify({"nickname": nickname, "score": "totalSum 없음"})
        else:
            print("❌ 잘못된 데이터 형식 또는 빈 응답", flush=True)
            return jsonify({"nickname": nickname, "score": "점수를 찾을 수 없음"})

    except Exception as e:
        print(f"❌ 예외 발생: {e}", flush=True)
        return jsonify({"error": str(e), "nickname": nickname, "score": "오류 발생"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
