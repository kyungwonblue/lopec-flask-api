from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    url = "https://api.lopec.kr/api/character/stats"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    payload = {
        "nickname": nickname
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            return jsonify({"nickname": nickname, "score": "API 응답 오류", "error": response.status_code})

        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            total_sum = data[0].get("totalSum", None)
            if total_sum:
                return jsonify({"nickname": nickname, "score": total_sum})
            else:
                return jsonify({"nickname": nickname, "score": "점수 없음"})
        else:
            return jsonify({"nickname": nickname, "score": "데이터 없음"})

    except Exception as e:
        return jsonify({"nickname": nickname, "score": "오류 발생", "error": str(e)})


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
