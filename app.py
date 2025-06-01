from flask import Flask, render_template, request, jsonify
import requests, re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-token', methods=['POST'])
def get_token():
    cookie = request.form.get('cookie')
    try:
        response = requests.get(
            'https://business.facebook.com/business_locations',
            headers={
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36',
                'referer': 'https://www.facebook.com/',
                'host': 'business.facebook.com',
                'origin': 'https://business.facebook.com',
                'upgrade-insecure-requests': '1',
                'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'content-type': 'text/html; charset=utf-8'
            },
            cookies={'cookie': cookie}
        )
        match = re.search(r'(EAAG\w+)', response.text)
        if match:
            return jsonify({'status': 'success', 'token': match.group(1)})
        else:
            return jsonify({'status': 'fail', 'message': 'Invalid or expired cookie'})
    except requests.exceptions.ConnectionError:
        return jsonify({'status': 'fail', 'message': 'No internet connection'})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'Unknown error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
