from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_score', methods=['GET'])
def get_score():
    nickname = request.args.get('nickname')
    characterClass = request.args.get('characterClass')
    totalStatus = request.args.get('totalStatus')
    statusSpecial = request.args.get('statusSpecial')
    statusHaste = request.args.get('statusHaste')

    if not all([nickname, characterClass, totalStatus, statusSpecial, statusHaste]):
        return jsonify({
            "nickname": nickname,
            "score": "필수 파라미터 누락"
        })

    # 요청 Payload 구성
    payload = {
        "nickname": nickname,
        "characterClass": characterClass,
        "totalStatus": int(totalStatus),
        "statusSpecial": int(statusSpecial),
        "statusHaste": int(statusHaste)
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://lopec.kr",
        "Referer": "https://lopec.kr/",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post("https://api.lopec.kr/api/character/stats", json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                score = data[0].get("totalSum")
                if score:
                    return jsonify({
                        "nickname": nickname,
                        "score": round(score, 2)  # 소수점 2자리까지
                    })
                else:
                    return jsonify({
                        "nickname": nickname,
                        "score": "점수를 찾을 수 없음"
                    })
            else:
                return jsonify({
                    "nickname": nickname,
                    "score": "스탯 조회 실패"
                })
        else:
            return jsonify({
                "nickname": nickname,
                "score": "API 응답 오류",
                "error": response.status_code
            })
    except Exception as e:
        return jsonify({
            "nickname": nickname,
            "score": "오류 발생",
            "error": str(e)
        })

# Render 배포용 포트 바인딩
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
