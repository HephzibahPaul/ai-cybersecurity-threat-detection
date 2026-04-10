from src.train_model import train
from src.visualize import plot_confusion

def run():
    X_test, y_test, model = train()

    y_pred = model.predict(X_test)

    plot_confusion(y_test, y_pred)

    print("✅ Training Complete")
    print("📊 Visualization Saved")

if __name__ == "__main__":
    run()