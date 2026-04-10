import joblib
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from src.preprocessing import load_and_preprocess

def train():
    X, y, scaler = load_and_preprocess()  # 🔥 no file needed

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    rf_model = RandomForestClassifier(n_estimators=100)
    rf_model.fit(X_train, y_train)

    # Train only on NORMAL data
    X_normal = X[y == 0]

    iso_model = IsolationForest(contamination=0.05, random_state=42)
    iso_model.fit(X_normal)

    joblib.dump(rf_model, "models/rf_model.pkl")
    joblib.dump(iso_model, "models/iso_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")

    return X_test, y_test, rf_model