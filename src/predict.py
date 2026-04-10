import joblib

rf_model = joblib.load("models/rf_model.pkl")
iso_model = joblib.load("models/iso_model.pkl")
scaler = joblib.load("models/scaler.pkl")

def detect_threat(input_data):
    packet_size, failed_logins, request_frequency = input_data

    # 🔥 RULE-BASED (reliable)
    if failed_logins > 5:
        return "🚨 Known Attack"

    if request_frequency > 700 or packet_size > 1200:
        return "⚠️ Anomaly Detected"

    return "✅ Normal Traffic"