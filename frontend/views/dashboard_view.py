import streamlit as st
from frontend.utils import api
from frontend.components import charts

def render_dashboard():
    # Styled header matching other pages
    username = st.session_state.get('username', 'Patient')
    st.markdown(f"""
<div style="margin-bottom: 2rem;">
    <h2 style="margin:0; font-size: 2.2rem; font-weight: 700;">👋 Hello, {username}</h2>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
        <p style="color: #94A3B8; margin: 0; font-size: 1.1rem;">
            Your Personal Health AI is <span style="color: #10B981; font-weight: 600;">● Active</span> & Ready to Help.
        </p>
        <div style="background: rgba(59, 130, 246, 0.1); color: #60A5FA; padding: 6px 16px; border-radius: 8px; font-size: 0.9rem; border: 1px solid rgba(59, 130, 246, 0.2); font-weight: 500;">
            Patient Portal
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # Fetch records for summary and trends
    records = api.fetch_records()
    
    # Summary Metrics Row
    if records:
        latest_record = records[0] # Assuming sorted by timestamp desc
        import json
        try:
            latest_data = json.loads(latest_record['data'])
            
            # Key Health Indicators (Summary Row)
            m1, m2, m3, m4 = st.columns(4)
            
            with m1:
                bmi = latest_data.get('bmi', 'N/A')
                st.markdown(f"""
                <div class="health-card">
                    <div class="metric-label">Latest BMI</div>
                    <div class="metric-value">{bmi}</div>
                    <div class="metric-trend trend-{'up' if isinstance(bmi, (int, float)) and bmi > 25 else 'down'}">
                        ● { 'Overweight' if isinstance(bmi, (int, float)) and bmi > 25 else 'Healthy' }
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with m2:
                glucose = latest_data.get('glucose', 'N/A')
                st.markdown(f"""
                <div class="health-card">
                    <div class="metric-label">Glucose</div>
                    <div class="metric-value">{glucose} <span style="font-size: 0.8rem; color: #94A3B8;">mg/dL</span></div>
                    <div class="metric-trend trend-{'up' if isinstance(glucose, (int, float)) and glucose > 140 else 'down'}">
                        ● { 'High' if isinstance(glucose, (int, float)) and glucose > 140 else 'Normal' }
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with m3:
                # Assuming heart status or similar if available
                bp = latest_data.get('blood_pressure', 'N/A')
                st.markdown(f"""
                <div class="health-card">
                    <div class="metric-label">Blood Pressure</div>
                    <div class="metric-value">{bp} <span style="font-size: 0.8rem; color: #94A3B8;">mmHg</span></div>
                    <div class="metric-trend trend-down">
                        ● Stable
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with m4:
                bilirubin = latest_data.get('total_bilirubin', 'N/A')
                st.markdown(f"""
                <div class="health-card">
                    <div class="metric-label">Bilirubin</div>
                    <div class="metric-value">{bilirubin} <span style="font-size: 0.8rem; color: #94A3B8;">mg/dL</span></div>
                    <div class="metric-trend trend-down">
                        ● Normal
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except Exception:
            pass

    # Middle Section: Insights & Notifications
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.subheader("💡 AI Health Insights")
        st.markdown("""
<div class="health-card" style="background: rgba(15, 23, 42, 0.4);">
    <p style="color: #cbd5e1; font-size: 1rem; margin-bottom: 1rem; font-weight: 500;">Personalized recommendations based on your latest data:</p>
    <div style="display: flex; gap: 1rem; margin-bottom: 1rem; align-items: flex-start;">
        <div style="background: rgba(16, 185, 129, 0.1); color: #10B981; padding: 10px; border-radius: 12px;">🍎</div>
        <div>
            <b style="color: #F8FAFC;">Nutrition Optimization</b>
            <p style="color: #94A3B8; font-size: 0.9rem; margin: 0;">Maintain low sodium intake to keep blood pressure in the optimal range.</p>
        </div>
    </div>
    <div style="display: flex; gap: 1rem; margin-bottom: 1rem; align-items: flex-start;">
        <div style="background: rgba(59, 130, 246, 0.1); color: #60A5FA; padding: 10px; border-radius: 12px;">🏃</div>
        <div>
            <b style="color: #F8FAFC;">Activity Goal</b>
            <p style="color: #94A3B8; font-size: 0.9rem; margin: 0;">Goal: 10,000 steps daily. You've averaged 6,500 this week. Let's push for more!</p>
        </div>
    </div>
    <div style="display: flex; gap: 1rem; align-items: flex-start;">
        <div style="background: rgba(139, 92, 246, 0.1); color: #A78BFA; padding: 10px; border-radius: 12px;">🧪</div>
        <div>
            <b style="color: #F8FAFC;">Upcoming Screenings</b>
            <p style="color: #94A3B8; font-size: 0.9rem; margin: 0;">It's been 3 months since your last Kidney function test. Consider a checkup soon.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    with col_b:
        st.subheader("🔔 Alerts")
        st.markdown("""
<div class="health-card" style="background: rgba(15, 23, 42, 0.4); min-height: 250px;">
    <div style="margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.5rem;">
        <div style="font-size: 0.85rem; color: #94A3B8;">RECENT</div>
        <div style="font-size: 0.95rem; color: #F8FAFC; margin: 4px 0;">New report generated</div>
        <div style="font-size: 0.75rem; color: #64748B;">Feb 25, 2026</div>
    </div>
    <div style="margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.5rem;">
        <div style="font-size: 0.85rem; color: #94A3B8;">APPOINTMENT</div>
        <div style="font-size: 0.95rem; color: #F8FAFC; margin: 4px 0;">No upcoming visits</div>
        <div style="font-size: 0.75rem; color: #64748B;">--</div>
    </div>
    <div style="padding-top: 0.5rem;">
        <div style="font-size: 0.85rem; color: #94A3B8;">SYSTEM</div>
        <div style="font-size: 0.95rem; color: #F8FAFC; margin: 4px 0;">Connected to Cloud AI</div>
        <div style="font-size: 0.75rem; color: #10B981;">Online</div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Analytical Health Trends")
    
    if records:
        tab1, tab2, tab3, tab4 = st.tabs(["🔥 BMI Trend", "🩸 Glucose Levels", "🧬 Bilirubin", "🫀 Vitap Map"])
        with tab1: charts.render_trend_chart(records, "bmi", "BMI")
        with tab2: charts.render_trend_chart(records, "glucose", "Glucose")
        with tab3: charts.render_trend_chart(records, "total_bilirubin", "Bilirubin")
        with tab4: 
            # Radar chart for latest snapshot
            latest_data = json.loads(records[0]['data']) if records else {}
            charts.render_radar_chart(latest_data)
    else:
        st.info("No test results found. Visit your specialist to upload new diagnostic data.")
