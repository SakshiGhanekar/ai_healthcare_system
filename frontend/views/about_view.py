"""
Terms, Privacy & About Page
===========================
Static legal/info pages for compliance.
"""
import streamlit as st


def render_about_page():
    """Render the About/Terms/Privacy page."""
    
    st.markdown("""
<div style="margin-bottom: 2.5rem;">
    <h1 style="margin:0; font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #0f172a 0%, #0ea5e9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Clinical Guidelines & Legal</h1>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem;">
        <p style="color: #64748B; margin: 0; font-size: 1.1rem; letter-spacing: 0.01em;">
            Terms of Service, Privacy Policy, and System Information.
        </p>
        <div style="background: rgba(148, 163, 184, 0.08); color: #64748B; padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(148, 163, 184, 0.15); font-weight: 700; text-transform: uppercase;">
            Policy Hub
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["About Us", "Terms of Service", "Privacy Policy"])
    
    with tab1:
        st.markdown("""
        ## 🏥 AI Healthcare System
        
        **Version:** 3.0 Portal Edition  
        **Powered by:** Your Diagnostic Center & Google Gemini
        
        ### Our Mission
        
        **Bridging the gap between Lab Results and Patient Understanding.**
        
        We partner with leading diagnostic centers to give you more than just paper reports. We give you an intelligent companion that helps you live healthier.
        
        **How it works:**
        1.  **Your Lab** uploads your test results securely.
        2.  **Our AI** analyzes variables like Glucose, BMI, and Liver Enzymes.
        3.  **You** get a personalized dashboard and a 24/7 Chat Assistant.
        
        ### Disclaimer
        
        ⚠️ **Not a Doctor:** The AI interprets data based on standard medical protocols but cannot diagnose you. Always verify critical concerns with your real doctor.
        
        ---
        
        **Support:** sakshighanekardev@gmail.com  
        
        **License:** Patient Personal Use License  
        **Privacy:** HIPAA Compliant Data Vault
        """)
    
    with tab2:
        st.markdown("""
        ## Terms of Service
        
        **Effective Date:** January 1, 2026
        
        ### 1. Acceptance of Terms
        
        By accessing or using the AI Healthcare System ("Service"), you agree to be 
        bound by these Terms of Service.
        
        ### 2. Description of Service
        
        The Service provides AI-powered health risk assessments and general health 
        information. The Service is intended for informational purposes only.
        
        ### 3. Medical Disclaimer
        
        **THE SERVICE DOES NOT PROVIDE MEDICAL ADVICE.** The information provided 
        is for general informational purposes only and is not intended to be a 
        substitute for professional medical advice, diagnosis, or treatment.
        
        ### 4. User Accounts
        
        - You are responsible for maintaining the confidentiality of your account
        - You must provide accurate information
        - You are responsible for all activities under your account
        
        ### 5. Acceptable Use
        
        You agree NOT to:
        - Use the Service for emergency medical situations (call 112/108)
        - Share your account with others
        - Attempt to reverse-engineer the Service
        - Use the Service for commercial purposes without permission
        
        ### 6. Limitation of Liability
        
        THE SERVICE IS PROVIDED "AS IS" WITHOUT WARRANTIES OF ANY KIND. WE ARE NOT 
        LIABLE FOR ANY DECISIONS MADE BASED ON THE INFORMATION PROVIDED.
        
        ### 7. Changes to Terms
        
        We reserve the right to modify these terms at any time. Continued use 
        constitutes acceptance of new terms.
        
        ---
        
        **Last Updated:** January 2026
        """)
    
    with tab3:
        st.markdown("""
        ## Privacy Policy
        
        **Effective Date:** March 1, 2026
        
        ### 1. Information We Collect
        
        **Account Information:**
        - Username, email (if provided)
        - Profile data (age, height, weight, health conditions)
        
        **Health Data:**
        - Health assessment inputs and results
        - Chat conversations with our AI
        
        **Technical Data:**
        - IP address, browser type
        - Usage patterns and timestamps
        
        ### 2. How We Use Your Information
        
        - To provide personalized health insights
        - To improve our AI models and service
        - To maintain and secure your account
        - To communicate important updates
        
        ### 3. Data Storage & Security
        
        - Your data is stored securely on cloud servers
        - We use encryption for sensitive health data
        - We do not sell your personal information
        
        ### 4. Your Rights
        
        You have the right to:
        - **Access** your personal data
        - **Download** your health records (PDF export available)
        - **Delete** your account and associated data
        - **Opt-out** of data collection for AI training
        
        ### 5. Data Retention
        
        We retain your data as long as your account is active. You may request 
        deletion at any time through your profile settings.
        
        ### 6. Third-Party Services
        
        We use:
        - **Google Gemini AI** for chatbot responses
        - **Tavily** for real-time health information search
        
        These services have their own privacy policies.
        
        ### 7. Contact Us
        
        For privacy concerns: sakshighanekardev@gmail.com
        
        ---
        
        **Last Updated:** January 2026
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748B; font-size: 0.85rem;">
        © 2026 AI Healthcare System. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
