from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_score')
def get_score():
    nickname = request.args.get('nickname', '')
    
    # 정확한 API 주소로 바꿔야 함 (아래 URL은 예시입니다. 실제 URL로 대체 필요)
    url = f"https://lopec.kr/api/search-character?headerCharacterName={nickname}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }

    resp = requests.get(url, headers=headers)

    # ✅ 응답 코드가 200인지 확인
    if resp.status_code != 200:
        return jsonify({
            'nickname': nickname,
            'score': '서버 응답 오류',
            'status_code': resp.status_code
        })

    try:
        data = resp.json()
    except ValueError as e:
        return jsonify({
            'nickname': nickname,
            'score': 'JSON 파싱 오류',
            'error': str(e)
        })

    if not data or not isinstance(data, list):
        return jsonify({'nickname': nickname, 'score': '점수를 찾을 수 없음'})

    try:
        score = float(data[0].get("totalSum", 0))
        return jsonify({'nickname': nickname, 'score': round(score, 2)})
    except (KeyError, ValueError, TypeError):
        return jsonify({'nickname': nickname, 'score': '점수 추출 실패'})

# ✅ Render에서 작동시키기 위한 포트 바인딩
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
