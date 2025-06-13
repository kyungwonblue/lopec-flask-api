from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

# 로깅 설정
logging.basicConfig(level=logging.INFO)

@app.route('/get_score', methods=['GET'])
def get_score():
    nickname = request.args.get('nickname')
    character_class = request.args.get('characterClass')
    total_status = request.args.get('totalStatus')
    status_special = request.args.get('statusSpecial')
    status_haste = request.args.get('statusHaste')

    if not all([nickname, character_class, total_status, status_special, status_haste]):
        return jsonify({"error": "Missing required parameters", "nickname": nickname, "score": "오류 발생"})

    url = "https://api.lopec.kr/api/character/stats"

    payload = {
        "nickname": nickname,
        "characterClass": character_class,
        "totalStatus": int(total_status),
        "statusSpecial": int(status_special),
        "statusHaste": int(status_haste)
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Origin": "https://lopec.kr",
        "Referer": "https://lopec.kr/"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        logging.info(f"📡 POST {url} | Payload: {payload} | Status: {response.status_code}")

        if response.status_code != 200:
            return jsonify({"error": response.status_code, "nickname": nickname, "score": "API 응답 오류"})

        response_json = response.json()
        logging.info(f"🔎 Raw response JSON: {response_json}")

        # 리스트 응답 처리
        if isinstance(response_json, list) and len(response_json) > 0:
            first_item = response_json[0]
            total_sum = first_item.get("totalSum", None)
        elif isinstance(response_json, dict):
            total_sum = response_json.get("totalSum", None)
        else:
            total_sum = None

        if total_sum is not None:
            return jsonify({"nickname": nickname, "score": round(total_sum, 2)})
        else:
            return jsonify({"nickname": nickname, "score": "totalSum 없음"})

    except Exception as e:
        logging.exception("🔥 Exception occurred during API request")
        return jsonify({"error": str(e), "nickname": nickname, "score": "오류 발생"})

# 포트 설정 (Render 등 배포 환경 대응)
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
