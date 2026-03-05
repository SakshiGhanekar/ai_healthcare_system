import streamlit as st
from frontend.utils import api  # Force reload
from frontend.components import charts

def render_lungs_page():
    st.markdown("""
<div style="margin-bottom: 2.5rem;">
    <h1 style="margin:0; font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #0f172a 0%, #0ea5e9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Respiratory Health Intelligence</h1>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem;">
        <p style="color: #64748B; margin: 0; font-size: 1.1rem; letter-spacing: 0.01em;">
            Advanced risk stratification for pulmonary and respiratory health factors.
        </p>
        <div style="background: rgba(14, 165, 233, 0.08); color: #0EA5E9; padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.15); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">
            Clinical Assessment
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    with st.form("lungs_form"):
        profile = api.fetch_profile() or {}
        
        # 1. Age & Gender
        default_age = 60
        gender_idx = 0 # Default Male [Male, Female]
        
        if profile.get('dob'):
            try:
                from datetime import datetime
                birth_date = datetime.strptime(str(profile['dob']).split()[0], "%Y-%m-%d")
                today = datetime.today()
                default_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            except:
                pass
        
        if profile.get('gender') == 'Female':
            gender_idx = 1
            
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 0, 120, default_age)
            gender = st.selectbox("Gender", ["Male", "Female"], index=gender_idx)
        
        st.subheader("Symptoms & Habits")
        
        # Grid layout for many checkboxes
        c1, c2, c3 = st.columns(3)
        with c1:
            smoking = st.checkbox("Smoking History")
            yellow_fingers = st.checkbox("Yellow Fingers")
            anxiety = st.checkbox("Anxiety")
            peer_pressure = st.checkbox("Peer Pressure")
            chronic_disease = st.checkbox("Chronic Disease")
        with c2:
            fatigue = st.checkbox("Fatigue / Tiredness")
            allergy = st.checkbox("Allergies")
            wheezing = st.checkbox("Wheezing")
            alcohol = st.checkbox("Alcohol Consumption")
            coughing = st.checkbox("Persistent Coughing")
        with c3:
            shortness_of_breath = st.checkbox("Shortness of Breath")
            swallowing_difficulty = st.checkbox("Swallowing Difficulty")
            chest_pain = st.checkbox("Chest Pain")

        if st.form_submit_button("Assess Risk"):
            # Map inputs (usually 1=No, 2=Yes in some datasets, or 0/1. 
            # Reviewing my test_api.py, I used 0/1 for binary. 
            # In backend/schemas.py LungsInput uses int.
            # Assuming standard 0=No, 1=Yes)
            
            data = {
                "gender": 1 if gender == "Male" else 0,
                "age": age,
                "smoking": int(smoking),
                "yellow_fingers": int(yellow_fingers),
                "anxiety": int(anxiety),
                "peer_pressure": int(peer_pressure),
                "chronic_disease": int(chronic_disease),
                "fatigue": int(fatigue),
                "allergy": int(allergy),
                "wheezing": int(wheezing),
                "alcohol": int(alcohol),
                "coughing": int(coughing),
                "shortness_of_breath": int(shortness_of_breath),
                "swallowing_difficulty": int(swallowing_difficulty),
                "chest_pain": int(chest_pain)
            }
            
            with st.spinner("Analyzing..."):
                result = api.get_prediction("lungs", data)
                
            if "error" in result:
                st.error(result['error'])
            else:
                pred = result.get('prediction', 'Unknown')
                st.success(f"Result: **{pred}**")
                api.save_record("Lungs", data, pred)
                
                c1, c2 = st.columns(2)
                with c1: charts.render_radar_chart(data)
                with c2: 
                    html = api.get_explanation("lungs", data)
                    if html: st.components.v1.html(html, height=300, scrolling=True)
