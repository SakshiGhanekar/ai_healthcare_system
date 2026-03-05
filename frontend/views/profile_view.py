import streamlit as st
from frontend.utils import api

def render_profile_page():
    # Global CSS for theme polishing
    st.markdown("""
    <style>
    div[data-testid="stFormSubmitButton"] > button {
      background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
      border: none;
    }
    .stTabs [aria-selected="true"] {
      border-bottom: 2.5px solid #0ea5e9 !important;
      color: #0ea5e9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    username = st.session_state.get('username', 'Patient')
    st.markdown(f"""
<div style="margin-bottom: 2.5rem;">
    <h1 style="margin:0; font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #0f172a 0%, #0ea5e9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">My Health Passport</h1>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem;">
        <p style="color: #64748B; margin: 0; font-size: 1.1rem; letter-spacing: 0.01em;">
            Your central hub for personal health data and clinical system preferences.
        </p>
        <div style="background: rgba(14, 165, 233, 0.08); color: #0EA5E9; padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.15); font-weight: 700; text-transform: uppercase;">
            Profile Settings
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    profile = api.fetch_profile()
    if not profile:
        st.error("Could not load profile.")
        return

    with st.expander("📝 Edit Profile Details", expanded=False):
        with st.form("profile_update"):
            # Profile Picture Upload
            st.markdown("#### Profile Picture")
            col_img, col_inputs = st.columns([1, 2])
            
            with col_img:
                current_pic = profile.get("profile_picture")
                if current_pic:
                    # Fix: Use HTML to bypass Streamlit MediaFileManager bugs with Base64
                    # Flattened HTML to prevent Markdown code block bugs
                    st.markdown(f'''
<div style="text-align: center;">
    <img src="{current_pic}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%; border: 4px solid #ffffff; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
    <p style="font-size: 0.85rem; color: #64748B; margin-top: 8px; font-weight: 600;">Current Photo</p>
</div>
''', unsafe_allow_html=True)
                else:
                    st.info("No photo uploaded")
                
                uploaded_file = st.file_uploader("Upload New Photo", type=['png', 'jpg', 'jpeg'])
            
            with col_inputs:
                col1, col2 = st.columns(2)
                with col1:
                    height = st.number_input("Height (cm)", value=int(profile.get("height") or 170), format="%d", step=1)
                    weight = st.number_input("Weight (kg)", value=float(profile.get("weight") or 70.0), format="%.1f", step=0.1)
                    diet = st.selectbox("Diet", ["Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Other"], index=0 if not profile.get("diet") else ["Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Other"].index(profile.get("diet")))
                    
                    # Date of Birth
                    from datetime import datetime, date
                    dob_val = datetime.today()
                    if profile.get("dob"):
                        try:
                            # Handle potential format variants
                            dob_str = str(profile.get("dob")).split()[0]
                            dob_val = datetime.strptime(dob_str, "%Y-%m-%d")
                        except:
                            pass
                    
                    dob = st.date_input("Date of Birth", value=dob_val, min_value=date(1900, 1, 1), max_value=date.today())
                with col2:
                    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"], index=0)
                    sleep = st.slider("Sleep (Hours)", 4.0, 12.0, float(profile.get("sleep_hours") or 7.0), step=0.5, format="%.1f")
                    stress = st.selectbox("Stress Level", ["Low", "Moderate", "High"], index=1)
                
                allow_data = st.checkbox("Allow Data Collection for AI Improvement", value=profile.get("allow_data_collection", True))
            
            if st.form_submit_button("Update Profile"):
                import base64
                pic_data = current_pic # Keep old if no new upload
                
                if uploaded_file:
                    try:
                        bytes_data = uploaded_file.getvalue()
                        b64_str = base64.b64encode(bytes_data).decode()
                        mime = uploaded_file.type
                        pic_data = f"data:{mime};base64,{b64_str}"
                    except Exception as e:
                        st.error(f"Error processing image: {e}")

                payload = {
                    "height": height, "weight": weight, "diet": diet,
                    "activity_level": activity, "sleep_hours": sleep,
                    "stress_level": stress, "allow_data_collection": allow_data,
                    "profile_picture": pic_data,
                    "dob": str(dob)
                }
                if api.update_profile(payload):
                    # Update Session State immediately for Sidebar sync
                    st.session_state['profile_picture'] = pic_data
                    st.rerun()

    # Display Metrics
    st.markdown("### My Stats")
    c1, c2, c3 = st.columns(3)
    c1.metric("Height", f"{profile.get('height') or 0} cm")
    c2.metric("Weight", f"{profile.get('weight') or 0} kg")
    
    # Calculate BMI
    height_val = profile.get('height') or 170
    weight_val = profile.get('weight') or 70
    
    h_m = float(height_val) / 100
    w_kg = float(weight_val)
    bmi = round(w_kg / (h_m ** 2), 2)
    c3.metric("BMI", bmi, delta="Normal" if 18.5 <= bmi <= 25 else "Check", delta_color="normal" if 18.5 <= bmi <= 25 else "inverse")

    # --- PDF Health Report Download ---
    st.markdown("---")
    st.markdown("### 📄 Download Health Report")
    st.markdown("""
    <p style="color: #94A3B8; font-size: 0.9rem;">
        Download a PDF summary of your health profile and assessment history.
    </p>
    """, unsafe_allow_html=True)
    
    # Authenticated Download Button
    c1, c2 = st.columns([1, 2])
    
    with c1:
        # We use a callback pattern or direct fetch if it's fast enough.
        # Since generating PDF might take a second, we'll make it direct for now.
        report_data = api.fetch_health_report()
        
        if report_data:
            st.download_button(
                label="📥 Download PDF Report",
                data=report_data,
                file_name=f"Health_Report_{username}.pdf",
                mime="application/pdf",
                key="dl_pdf_btn",
                use_container_width=True,
            )
        else:
            st.warning("Report unavailable (check connection)")
            
    with c2:
        st.info("💡 **Tip:** The PDF includes your profile, recent health assessments, and personalized recommendations.")

    # --- Personalized Health Tips ---
    st.markdown("---")
    st.markdown("### 💡 Your Personalized Tips")
    
    tips = []
    if bmi < 18.5:
        tips.append("🍎 Your BMI suggests you're underweight. Consider consulting a nutritionist for a healthy weight gain plan.")
    elif bmi > 25:
        tips.append("🏃 Your BMI is above normal. Regular cardio exercise and a balanced diet can help maintain a healthy weight.")
    else:
        tips.append("✅ Great job! Your BMI is in the healthy range. Keep up your good habits!")
    
    if profile.get('sleep_hours') and float(profile.get('sleep_hours', 7)) < 7:
        tips.append("😴 You're getting less than 7 hours of sleep. Quality sleep is crucial for heart health and immune function.")
    
    if profile.get('stress_level') == 'High':
        tips.append("🧘 High stress can impact your health. Consider meditation, deep breathing, or regular walks.")
    
    tips.append("💧 Remember to drink 8 glasses of water daily for optimal health.")
    tips.append("🩺 Schedule regular check-ups with your healthcare provider.")
    
    for tip in tips:
        st.markdown(f"- {tip}")

