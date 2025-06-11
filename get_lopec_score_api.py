from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def fetch_basic(nickname):
    url = "https://api.lopec.kr/api/character/basic"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, params={"nickname": nickname}, headers=headers, timeout=5)
    if resp.status_code != 200:
        return None
    data = resp.json()
    if isinstance(data, list) and data:
        return {
            "characterClass": data[0].get("characterClass"),
            "totalStatus": data[0].get("totalStatus"),
            "statusSpecial": data[0].get("statusSpecial"),
            "statusHaste": data[0].get("statusHaste")
        }
    return None

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    basic = fetch_basic(nickname)
    if not basic:
        return jsonify({"nickname": nickname, "score": "스탯 조회 실패"}), 500

    payload = {
        "nickname": nickname,
        **basic
    }
    resp = requests.post("https://api.lopec.kr/api/character/stats",
                         json=payload,
                         headers={
                             'Content-Type': 'application/json',
                             'User-Agent': 'Mozilla/5.0',
                             'Origin': 'https://lopec.kr',
                             'Referer': 'https://lopec.kr/'
                         }, timeout=10)
    if resp.status_code != 200:
        return jsonify({"nickname": nickname, "score": "totalSum API 오류", "status": resp.status_code}), 500

    data = resp.json()
    if isinstance(data, list) and data:
        total_sum = data[0].get('totalSum')
        if total_sum:
            return jsonify({"nickname": nickname, "score": round(total_sum, 2)})
    return jsonify({"nickname": nickname, "score": "totalSum 없음"}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
