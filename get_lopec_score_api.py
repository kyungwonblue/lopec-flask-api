from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/get_score', methods=['GET'])
def get_score():
    nickname = request.args.get('nickname')

    print(f"▶️ 받은 요청 - 닉네임: {nickname}")

    if not nickname:
        print("❌ 닉네임 누락")
        return jsonify({
            "error": "Missing nickname parameter",
            "score": "오류 발생"
        })

    try:
        # 스탯 정보 자동 수집
        search_url = f"https://lopec.kr/character/search?nickname={nickname}"
        res = requests.get(search_url)
        soup = BeautifulSoup(res.text, 'html.parser')

        info_box = soup.select_one(".css-d4l2k6")  # 캐릭터 정보 박스
        if not info_box:
            print("❌ 캐릭터 정보 박스를 찾을 수 없음")
            return jsonify({"nickname": nickname, "score": "캐릭터 정보 없음"})

        character_class = info_box.select_one(".css-1wzj5tw").text.strip()
        total_status = int(info_box.select_one(".css-jo3fq0").text.strip())
        status_special = int(info_box.select(".css-jo3fq0")[1].text.strip())
        status_haste = int(info_box.select(".css-jo3fq0")[2].text.strip())

        print(f"📋 스탯 자동 수집 완료 - 클래스: {character_class}, 총스탯: {total_status}, 특성: {status_special}, 가속: {status_haste}")

        # 점수 요청
        payload = {
            "nickname": nickname,
            "characterClass": character_class,
            "totalStatus": total_status,
            "statusSpecial": status_special,
            "statusHaste": status_haste
        }

        print(f"📤 Lopec API 요청 전송: https://api.lopec.kr/api/character/stats")
        print(f"📦 Payload: {payload}")

        res = requests.post("https://api.lopec.kr/api/character/stats", json=payload)
        print(f"📥 응답 상태 코드: {res.status_code}")

        if res.status_code == 200:
            data = res.json()
            print(f"📄 Lopec API 응답 데이터: {data}")
            total_sum = data.get("totalSum")

            if total_sum:
                return jsonify({
                    "nickname": nickname,
                    "score": round(total_sum, 2)
                })
            else:
                print("❌ totalSum 없음")
                return jsonify({"nickname": nickname, "score": "점수를 찾을 수 없음"})
        else:
            print("❌ Lopec API 응답 실패")
            return jsonify({"nickname": nickname, "score": "Lopec API 오류"})

    except Exception as e:
        print(f"❌ 예외 발생: {str(e)}")
        return jsonify({
            "nickname": nickname,
            "score": "오류 발생",
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
