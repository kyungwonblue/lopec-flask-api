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

    print("📥 요청 받은 닉네임:", nickname)
    print("📥 클래스:", character_class)
    print("📥 totalStatus:", total_status)
    print("📥 statusSpecial:", status_special)
    print("📥 statusHaste:", status_haste)

    # 파라미터 누락 여부 확인
    if not all([nickname, character_class, total_status, status_special, status_haste]):
        print("❌ 필수 파라미터 누락")
        return jsonify({"error": "Missing required parameters", "nickname": nickname, "score": "오류 발생"}), 400

    # API 요청 준비
    stat_url = "https://api.lopec.kr/api/character/stats"
    payload = {
        "nickname": nickname,
        "characterClass": character_class,
        "totalStatus": int(total_status),
        "statusSpecial": int(status_special),
        "statusHaste": int(status_haste)
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    print("🚀 POST 요청 URL:", stat_url)
    print("🚀 요청 Payload:", payload)

    try:
        res2 = requests.post(stat_url, json=payload, headers=headers, timeout=10)
        print("📨 응답 상태코드:", res2.status_code)
        print("📨 응답 본문:", res2.text)
    except Exception as e:
        print("❌ 요청 예외:", str(e))
        return jsonify({"error": str(e), "nickname": nickname, "score": "API 요청 실패"}), 500

    if res2.status_code != 200:
        print("❌ API 응답 오류 코드:", res2.status_code)
        return jsonify({"error": "API 응답 오류", "nickname": nickname, "score": "API 응답 오류"}), 400

    try:
        data = res2.json()
        print("📦 JSON 파싱 결과:", data)
    except Exception as e:
        print("❌ JSON 파싱 실패:", str(e))
        return jsonify({"error": str(e), "nickname": nickname, "score": "JSON 파싱 실패"}), 500

    if isinstance(data, list) and len(data) > 0:
        total_sum = data[0].get('totalSum')
        print("🔍 totalSum 추출:", total_sum)
        if total_sum is not None:
            return jsonify({"nickname": nickname, "score": round(total_sum, 2)})
        else:
            print("❌ totalSum 없음")
            return jsonify({"nickname": nickname, "score": "totalSum 없음"}), 404
    else:
        print("❌ 예상치 못한 응답 형식:", data)
        return jsonify({"nickname": nickname, "score": "점수를 찾을 수 없음"}), 404

# Render에서 실행될 때 포트 설정
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
