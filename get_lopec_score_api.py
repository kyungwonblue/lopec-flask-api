from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_score', methods=['GET'])
def get_score():
    nickname = request.args.get('nickname')
    character_class = request.args.get('characterClass')
    total_status = request.args.get('totalStatus', type=int)
    status_special = request.args.get('statusSpecial', type=int)
    status_haste = request.args.get('statusHaste', type=int)

    if not all([nickname, character_class, total_status, status_special, status_haste]):
        return jsonify({
            'nickname': nickname or '',
            'score': '파라미터 누락'
        })

    url = 'https://api.lopec.kr/api/character/stats'
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://lopec.kr',
        'Referer': 'https://lopec.kr/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    payload = {
        'nickname': nickname,
        'characterClass': character_class,
        'totalStatus': total_status,
        'statusSpecial': status_special,
        'statusHaste': status_haste
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        app.logger.info("🔎 Raw response JSON: %s", response.text)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list) and data and 'totalSum' in data[0]:
                    return jsonify({
                        'nickname': nickname,
                        'score': round(data[0]['totalSum'], 2)
                    })
                else:
                    return jsonify({
                        'nickname': nickname,
                        'score': 'totalSum 없음'
                    })
            except ValueError:
                return jsonify({
                    'nickname': nickname,
                    'score': 'JSON 파싱 오류'
                })
        else:
            return jsonify({
                'nickname': nickname,
                'score': f'API 응답 오류 (status {response.status_code})'
            })

    except Exception as e:
        return jsonify({
            'nickname': nickname,
            'score': '요청 실패',
            'error': str(e)
        })


# Render에서 배포하려면 아래 코드 필요
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
