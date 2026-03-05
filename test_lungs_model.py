import joblib
import pandas as pd

# Load model and scaler
model = joblib.load("backend/lungs_model.pkl")
scaler = joblib.load("backend/lungs_scaler.pkl")

# Profile: 53y Female, All symptoms YES
# feature_names = ['GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC_DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING', 'ALCOHOL_CONSUMING', 'COUGHING', 'SHORTNESS_OF_BREATH', 'SWALLOWING_DIFFICULTY', 'CHEST_PAIN']
# gender: 0 (Female)
# symptoms: 1 (Yes)
input_data = [0, 53, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
df = pd.DataFrame([input_data], columns=['GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC_DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING', 'ALCOHOL_CONSUMING', 'COUGHING', 'SHORTNESS_OF_BREATH', 'SWALLOWING_DIFFICULTY', 'CHEST_PAIN'])
input_scaled = scaler.transform(df)
pred = model.predict(input_scaled)
print(f"Prediction: {pred[0]}")
