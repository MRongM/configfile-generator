from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/demo-api/', methods=['POST', 'GET'])
def demo_api():
    raw_data = request.get_data()
    try:
        body = request.get_json(force=True)
    except Exception:
        body = raw_data.decode('utf-8', errors='replace')
    params = request.args.to_dict()

    print("Received body (parsed):", body)
    print("Received query params:", params)

    return jsonify({
        'received_body': body,
        'received_params': params
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)