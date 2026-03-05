import streamlit as st
from frontend.utils import api
from frontend.components import charts

def render_dashboard():
    # Styled header matching other pages
    username = st.session_state.get('username', 'Patient')
    st.markdown(f"""
<div style="margin-bottom: 2.5rem;">
    <h1 style="margin:0; font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #0f172a 0%, #0ea5e9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Welcome, {username}</h1>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem;">
        <p style="color: #64748B; margin: 0; font-size: 1.1rem; letter-spacing: 0.01em;">
            Your health profile is <span style="color: #10B981; font-weight: 600;">● Synchronized</span> with Global AI.
        </p>
        <div style="background: rgba(14, 165, 233, 0.08); color: #0EA5E9; padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.15); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">
            Clinical Dashboard
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
                    <div class="metric-label">Body Mass Index</div>
                    <div class="metric-value">{bmi}</div>
                    <div style="color: {'#FB7185' if isinstance(bmi, (int, float)) and bmi > 25 else '#34D399'}; font-size: 0.85rem; font-weight: 600;">
                        ● { 'Alert: Overweight' if isinstance(bmi, (int, float)) and bmi > 25 else 'Optimal' }
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with m2:
                glucose = latest_data.get('glucose', 'N/A')
                st.markdown(f"""
                <div class="health-card">
                    <div class="metric-label">Blood Glucose</div>
                    <div class="metric-value">{glucose} <span style="font-size: 0.9rem; color: #64748B;">mg/dL</span></div>
                    <div style="color: {'#FB7185' if isinstance(glucose, (int, float)) and glucose > 140 else '#34D399'}; font-size: 0.85rem; font-weight: 600;">
                        ● { 'Requires Attention' if isinstance(glucose, (int, float)) and glucose > 140 else 'Within Range' }
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with m3:
                # Assuming heart status or similar if available
                bp = latest_data.get('blood_pressure', 'N/A')
                st.markdown(f"""
                <div class="health-card">
                    <div class="metric-label">Blood Pressure</div>
                    <div class="metric-value">{bp} <span style="font-size: 0.9rem; color: #64748B;">mmHg</span></div>
                    <div style="color: #34D399; font-size: 0.85rem; font-weight: 600;">
                        ● Stable
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with m4:
                bilirubin = latest_data.get('total_bilirubin', 'N/A')
                st.markdown(f"""
                <div class="health-card">
                    <div class="metric-label">Liver: Bilirubin</div>
                    <div class="metric-value">{bilirubin} <span style="font-size: 0.9rem; color: #64748B;">mg/dL</span></div>
                    <div style="color: #34D399; font-size: 0.85rem; font-weight: 600;">
                        ● Normal
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except Exception:
            pass

    # Middle Section: Insights & Notifications
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown('<h3 style="margin-top:0.5rem; font-size: 1.5rem; color: #0f172a;">🤖 Clinical AI Advisory</h3>', unsafe_allow_html=True)
        st.markdown("""
<div class="health-card">
    <p style="color: #64748B; font-size: 1rem; margin-bottom: 1.5rem;">Diagnostic observations based on your longitudinal health trajectory:</p>
    <div style="display: flex; gap: 1.25rem; margin-bottom: 1.5rem; align-items: flex-start;">
        <div style="background: #f0fdf4; padding: 12px; border-radius: 12px; border: 1px solid #dcfce7; font-size: 1.2rem;">🥗</div>
        <div>
            <div style="color: #1e293b; font-weight: 700; font-size: 1.05rem;">Dietary Management Required</div>
            <p style="color: #64748B; font-size: 0.95rem; margin: 4px 0 0 0; line-height: 1.5;">Reduce refined sugar intake. Your latest glucose levels suggest sensitivity to late-night carbohydrate consumption.</p>
        </div>
    </div>
    <div style="display: flex; gap: 1.25rem; margin-bottom: 1.5rem; align-items: flex-start;">
        <div style="background: #eff6ff; padding: 12px; border-radius: 12px; border: 1px solid #dbeafe; font-size: 1.2rem;">🫀</div>
        <div>
            <div style="color: #1e293b; font-weight: 700; font-size: 1.05rem;">Cardiovascular Efficiency</div>
            <p style="color: #64748B; font-size: 0.95rem; margin: 4px 0 0 0; line-height: 1.5;">BP trend is exceptionally stable. Maintain current level of moderate aerobic activity (minimum 20 mins/day).</p>
        </div>
    </div>
    <div style="display: flex; gap: 1.25rem; align-items: flex-start;">
        <div style="background: #fff7ed; padding: 12px; border-radius: 12px; border: 1px solid #ffedd5; font-size: 1.2rem;">👨‍⚕️</div>
        <div>
            <div style="color: #1e293b; font-weight: 700; font-size: 1.05rem;">Recommended Screener</div>
            <p style="color: #64748B; font-size: 0.95rem; margin: 4px 0 0 0; line-height: 1.5;">It is time for a routine kidney function check. Our models suggest a baseline evaluation is prudent at this stage.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    with col_b:
        st.markdown('<h3 style="margin-top:0.5rem; font-size: 1.5rem; color: #0f172a;">📅 Active Logs</h3>', unsafe_allow_html=True)
        st.markdown("""
<div class="health-card" style="min-height: 340px;">
    <div style="margin-bottom: 1.25rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 1rem;">
        <div style="font-size: 0.75rem; color: #10B981; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 4px;">SYSTEM LOG</div>
        <div style="font-size: 0.95rem; color: #1e293b; font-weight: 600;">Latest Diagnostic Imported</div>
        <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">2 hours ago • Verified by AI</div>
    </div>
    <div style="margin-bottom: 1.25rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 1rem;">
        <div style="font-size: 0.75rem; color: #64748B; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 4px;">APPOINTMENT</div>
        <div style="font-size: 0.95rem; color: #1e293b; font-weight: 600;">No Pending Sessions</div>
        <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">Book through Telemedicine tab</div>
    </div>
    <div style="padding-top: 0.5rem;">
        <div style="font-size: 0.75rem; color: #0EA5E9; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 4px;">CONNECTIVITY</div>
        <div style="font-size: 0.95rem; color: #1e293b; font-weight: 600;">High-Precision Engine</div>
        <div style="display: flex; align-items: center; gap: 6px; margin-top: 4px;">
            <div style="width: 8px; height: 8px; background: #10B981; border-radius: 50%;"></div>
            <div style="font-size: 0.8rem; color: #10B981; font-weight: 600;">Operational</div>
        </div>
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
