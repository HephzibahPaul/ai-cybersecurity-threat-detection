import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.generate_data import generate_dataset

def load_and_preprocess(path=None):
    
    # 🔥 If no dataset → generate one
    if path is None:
        data = generate_dataset(2000)
    else:
        try:
            data = pd.read_csv(path)
            if data.empty:
                raise Exception("Empty dataset")
        except:
            print("⚠️ Using generated dataset instead...")
            data = generate_dataset(2000)

    # Label handling
    if "Attack_Label" in data.columns:
        label_col = "Attack_Label"
    elif "Label" in data.columns:
        label_col = "Label"
    else:
        raise Exception("No label column found")

    X = data.drop(label_col, axis=1)
    y = data[label_col]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler