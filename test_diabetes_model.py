import os
import joblib
import numpy as np

# Path to the model
MODEL_PATH = "backend/diabetes_model.pkl"

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded: {type(model)}")
        
        # Features: ['HighBP', 'HighChol', 'BMI', 'Smoker', 'HeartDiseaseorAttack', 'PhysActivity', 'GenHlth', 'Sex', 'Age']
        
        # Test case 1: Healthy Young (30y)
        healthy = [0, 0, 24, 0, 0, 1, 1, 1, 3] 
        print(f"Healthy Young: {model.predict([healthy])}")
        
        # Test case 2: Very Unhealthy Old (70y, BMI 45, High BP, High Chol, Stroke)
        unhealthy_old = [1, 1, 45, 1, 1, 0, 5, 1, 11]
        print(f"Unhealthy Old: {model.predict([unhealthy_old])}")
        
        # Test case 3: Just Age 70
        age_70 = [0, 0, 24, 0, 0, 1, 1, 1, 11]
        print(f"Just Age 70: {model.predict([age_70])}")
        
    except Exception as e:
        print(f"Error: {e}")
