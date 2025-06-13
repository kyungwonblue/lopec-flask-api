from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/get_score', methods=['GET'])
def get_score():
    nickname = request.args.get('nickname')

    if not nickname:
        return jsonify({"error": "Missing nickname", "nickname": nickname, "score": "오류 발생"}), 400

    try:
        # Step 1: 캐릭터 검색 (닉네임으로)
        search_url = f"https://lopec.kr/api/search-character?headerCharacterName={nickname}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(search_url, headers=headers, timeout=10)
        if res.status_code != 200:
            return jsonify({"error": "Search failed", "nickname": nickname, "score": "캐릭터 조회 실패"}), 500

        characters = res.json()
        target = next((char for char in characters if char["nickname"] == nickname), None)

        if not target:
            return jsonify({"error": "Character not found", "nickname": nickname, "score": "캐릭터 없음"}), 404

        # Step 2: 스탯 추출
        payload = {
            "nickname": target["nickname"],
            "characterClass": target["characterClass"],
            "totalStatus": target["totalStatus"],
            "statusSpecial": target["statusSpecial"],
            "statusHaste": target["statusHaste"]
        }

        # Step 3: 점수 요청
        stat_url = "https://api.lopec.kr/api/character/stats"
        res2 = requests.post(stat_url, json=payload, headers=headers, timeout=10)
        print("🔍 POST 요청 URL:", stat_url)
        print("🔍 요청 Payload:", payload)
        print("🔍 응답 상태코드:", res2.status_code)
        print("🔍 응답 텍스트:", res2.text)
        
        if res2.status_code != 200:
            return jsonify({"error": "Stat API failed", "nickname": nickname, "score": "스탯 조회 실패"}), 500

        if not res2.text.strip():
            return jsonify({"error": "Empty response from stats API", "nickname": nickname, "score": "응답 없음"}), 500

        try:
            data = res2.json()
        except Exception as e:
            print("⚠️ JSON 파싱 에러:", str(e))
            return jsonify({"error": str(e), "nickname": nickname, "score": "JSON 파싱 실패"}), 500

        # 결과 확인
        print("✅ 파싱된 응답 데이터:", data)

        # totalSum 추출
        score = round(data[0].get("totalSum", 0), 2) if isinstance(data, list) and data and "totalSum" in data[0] else "점수를 찾을 수 없음"


        return jsonify({"nickname": nickname, "score": score})

            except Exception as e:
        return jsonify({"error": str(e), "nickname": nickname, "score": "오류 발생"}), 500

# Render 서버용 포트 바인딩
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
