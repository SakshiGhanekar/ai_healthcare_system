import os
import pickle

# --- Configuration ---
# Robust path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "..", "data", "processed", "diabetes.parquet")
MODEL_PATH = os.path.join(BASE_DIR, "diabetes_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "diabetes_scaler.pkl")

def train_diabetes_model():
    print("Starting Diabetes Model Training...")
    
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    # 1. Load Data
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Dataset not found at {DATASET_PATH}")
        return

    df = pd.read_parquet(DATASET_PATH)
    print(f"Loaded Dataset: {len(df)} records")

    # 2. Preprocessing (BRFSS 2015)
    # Target: 'diabetes' (already renamed in data_processing.py)
    # Features of interest (mapping for prediction.py compatibility)
    features = ['HighBP', 'HighChol', 'BMI', 'Smoker', 'HeartDiseaseorAttack', 'PhysActivity', 'GenHlth', 'Sex', 'Age']
    
    # Ensure all required features exist
    missing = [f for f in features if f not in df.columns]
    if missing:
        print(f"Error: Missing columns {missing}")
        return

    # Keep only target and selected features
    df = df[['diabetes'] + features].copy()
    
    # Drop NaNs
    df.dropna(inplace=True)

    print("Preprocessing Complete")

    # 3. Features & Target
    X = df.drop("diabetes", axis=1)
    Y = df["diabetes"]

    # 4. Train/Test Split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # 5. Training (RandomForest)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, Y_train)

    # 6. Evaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(Y_test, y_pred)
    print(f"Model Trained. Accuracy: {acc:.4f}")

    # 7. Save Model
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model Saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_diabetes_model()
