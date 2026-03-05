import streamlit as st
from frontend.utils import api
from frontend.components import charts

def render_heart_page():
    st.markdown("""
<div style="margin-bottom: 2.5rem;">
    <h1 style="margin:0; font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #0f172a 0%, #0ea5e9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Cardio-Vascular Intelligence</h1>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem;">
        <p style="color: #64748B; margin: 0; font-size: 1.1rem; letter-spacing: 0.01em;">
            Advanced risk stratification for myocardial infarction and coronary artery disease.
        </p>
        <div style="background: rgba(14, 165, 233, 0.08); color: #0EA5E9; padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.15); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">
            Cardiac Screener
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    # --- Autofill Logic ---
    profile = api.fetch_profile() or {}
    
    # 1. Age Calculation
    default_age = 45
    if profile.get('dob'):
        try:
            from datetime import datetime
            birth_date = datetime.strptime(str(profile['dob']).split()[0], "%Y-%m-%d")
            today = datetime.today()
            default_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        except:
            pass

    # 2. Gender
    p_gender = profile.get('gender', 'Male')
    gender_idx = 0 if p_gender == "Female" else 1 # [Female, Male]
    
    # 3. BMI Calculation
    default_bmi = 25.0
    if profile.get('height') and profile.get('weight'):
        try:
            h_m = float(profile['height']) / 100
            w_kg = float(profile['weight'])
            default_bmi = round(w_kg / (h_m ** 2), 1)
        except:
            pass

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h3 style="font-size: 1.3rem; margin-bottom: 1rem; color: #1e293b; font-weight: 700;">🫀 Vital Matrix</h3>', unsafe_allow_html=True)
        age = st.number_input("Age (Years)", 1, 120, default_age)
        gender = st.selectbox("Gender", ["Female", "Male"], index=gender_idx)
        bmi = st.number_input("BMI (kg/m²)", 10.0, 50.0, default_bmi)
        systolic = st.number_input("Systolic BP (mmHg)", 80, 250, 120, help="Top number of your blood pressure reading.")
        chol = st.number_input("Total Cholesterol (mg/dL)", 100, 600, 200)
    
    with col2:
        st.markdown('<h3 style="font-size: 1.3rem; margin-bottom: 1rem; color: #1e293b; font-weight: 700;">🧬 Lifestyle & Genetic Risk</h3>', unsafe_allow_html=True)
        smoker = st.selectbox("Substantial Smoking History (100+ Cigs)", ["No", "Yes"])
        stroke = st.selectbox("History of Stroke/TIA", ["No", "Yes"])
        diabetes = st.selectbox("Diabetes Mellitus Type I/II", ["No", "Yes"])
        activity = st.selectbox("Regular Physical Activity", ["No", "Yes"])
        alcohol = st.selectbox("Heavy Alcohol Consumption", ["No", "Yes"])
        general = st.slider("Subjective Health Perception", 1, 5, 3, help="1: Exceptional, 5: Poor")

    if st.button("Initiate Cardiac Analysis", type="primary", use_container_width=True):
        inputs = {
            "age": age,
            "gender": 1 if gender == "Male" else 0,
            "high_bp": 1 if systolic > 130 else 0,
            "high_chol": 1 if chol > 200 else 0,
            "bmi": bmi,
            "smoker": 1 if smoker == "Yes" else 0,
            "stroke": 1 if stroke == "Yes" else 0,
            "diabetes": 1 if diabetes == "Yes" else 0,
            "phys_activity": 1 if activity == "Yes" else 0,
            "hvy_alcohol": 1 if alcohol == "Yes" else 0,
            "gen_hlth": general
        }
        
        with st.spinner("Analyzing Heart Health..."):
            result = api.get_prediction("heart", inputs)
            
        if "error" in result:
            st.error(result['error'])
        else:
            prediction = result.get("prediction", "Unknown")
            st.success(f"Result: **{prediction}**")
            api.save_record("Heart", inputs, prediction)
            
            c1, c2 = st.columns(2)
            with c1: charts.render_radar_chart(inputs)
            with c2: 
                html = api.get_explanation("heart", inputs)
                if html: st.components.v1.html(html, height=300, scrolling=True)
