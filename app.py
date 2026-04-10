from flask import Flask, request, jsonify, send_file
from src.predict import detect_threat

app = Flask(__name__)

# 🔥 DASHBOARD UI
@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""

    if request.method == 'POST':
        packet_size = float(request.form['packet_size'])
        failed_logins = float(request.form['failed_logins'])
        request_frequency = float(request.form['request_frequency'])

        result = detect_threat([packet_size, failed_logins, request_frequency])

    # Color logic
    if "Attack" in result:
        color = "#ef4444"   # red
    elif "Anomaly" in result:
        color = "#facc15"   # yellow
    else:
        color = "#22c55e"   # green

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
                width: 350px;
                text-align: center;
                box-shadow: 0 0 30px rgba(0,0,0,0.6);
            }}

            h1 {{
                margin-bottom: 20px;
            }}

            input {{
                margin: 10px 0;
                padding: 10px;
                width: 100%;
                border-radius: 8px;
                border: none;
            }}

            button {{
                margin-top: 10px;
                padding: 10px;
                width: 100%;
                background: #22c55e;
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }}

            .result {{
                margin-top: 20px;
                font-size: 18px;
                font-weight: bold;
                color: {color};
            }}

            a {{
                display: block;
                margin-top: 15px;
                color: #38bdf8;
                text-decoration: none;
            }}
        </style>
    </head>

    <body>
        <div class="card">
            <h1>🔐 Cyber Threat Detection</h1>

            <form method="POST">
                <input type="number" name="packet_size" placeholder="Packet Size" required>
                <input type="number" name="failed_logins" placeholder="Failed Logins" required>
                <input type="number" name="request_frequency" placeholder="Request Frequency" required>

                <button type="submit">Analyze</button>
            </form>

            <div class="result">{result}</div>

            <a href="/confusion">📊 View Confusion Matrix</a>
        </div>
    </body>
    </html>
    """

# 🔥 CONFUSION MATRIX ROUTE
@app.route('/confusion')
def show_confusion():
    return send_file('outputs/confusion_matrix.png', mimetype='image/png')

# 🔥 API ENDPOINT (POSTMAN / CURL)
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

# 🔥 RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)