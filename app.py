from flask import Flask, request, jsonify, send_file
from src.predict import detect_threat

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""

    # ⭐ Store values
    packet_size = ""
    failed_logins = ""
    request_frequency = ""

    if request.method == 'POST':
        packet_size = request.form.get('packet_size', '')
        failed_logins = request.form.get('failed_logins', '')
        request_frequency = request.form.get('request_frequency', '')

        if packet_size and failed_logins and request_frequency:
            features = [
                float(packet_size),
                float(failed_logins),
                float(request_frequency)
            ]

            result = detect_threat(features)

    # 🎨 Color logic
    if "Attack" in result:
        color = "#ef4444"
    elif "Anomaly" in result:
        color = "#facc15"
    else:
        color = "#22c55e"

    return f"""
    <html>
    <head>
        <title>Cyber Threat Detection</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #0f172a, #1e293b);
                color: white;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            .card {{
                background: #1e293b;
                padding: 30px;
                border-radius: 15px;
                width: 280px;
                text-align: center;
                box-shadow: 0 0 30px rgba(0,0,0,0.6);
            }}

            h1 {{
                margin-bottom: 18px;
                font-size: 20px;
            }}

            input {{
                margin: 8px 0;
                padding: 8px;
                width: 90%;
                border-radius: 6px;
                border: none;
            }}

            button {{
                margin-top: 10px;
                padding: 8px;
                width: 90%;
                background: #22c55e;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }}

            .result {{
                margin-top: 14px;
                font-size: 16px;
                font-weight: bold;
                color: {color};
            }}

            a {{
                display: block;
                margin-top: 12px;
                color: #38bdf8;
                text-decoration: none;
            }}
        </style>
    </head>

    <body>
        <div class="card">
            <h1>🔐 Cyber Threat Detection</h1>

            <form method="POST">
                <input type="number" name="packet_size" placeholder="Packet Size" value="{packet_size}" required>
                <input type="number" name="failed_logins" placeholder="Failed Logins" value="{failed_logins}" required>
                <input type="number" name="request_frequency" placeholder="Request Frequency" value="{request_frequency}" required>

                <button type="submit">Analyze</button>
            </form>

            <div class="result">{result}</div>

            <a href="/confusion">📊 View Confusion Matrix</a>
        </div>
    </body>
    </html>
    """

@app.route('/confusion')
def show_confusion():
    return send_file('outputs/confusion_matrix.png', mimetype='image/png')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    features = [
        data["packet_size"],
        data["failed_logins"],
        data["request_frequency"]
    ]

    result = detect_threat(features)

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)