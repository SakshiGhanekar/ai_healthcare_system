"""
Auth View - Balanced Design
===========================
Fits in viewport with proper sizing - not too cramped.
"""
import streamlit as st
from frontend.utils import api

def render_auth_page():
    """Auth page with balanced design."""
    
    st.markdown("""
<style>
/* No scrolling */
html, body, [data-testid="stAppViewContainer"], .main {
    overflow: hidden !important;
    height: 100vh !important;
    font-family: 'Manrope', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%) !important;
}

.block-container {
    padding: 2rem 2rem !important;
    height: 100vh !important;
    overflow: hidden !important;
}

[data-testid="stHorizontalBlock"] {
    height: calc(100vh - 4rem) !important;
    align-items: center !important;
}

/* Form styling - proper sizing */
div.stForm {
    padding: 1.5rem !important;
    border-radius: 20px !important;
    background: #ffffff !important;
    border: 1px solid rgba(14, 165, 233, 0.1) !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #e2e8f0 !important;
    margin-bottom: 1.5rem !important;
}

.stTabs [data-baseweb="tab"] {
    padding: 0.75rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #64748b !important;
}

.stTabs [aria-selected="true"] {
    color: #0ea5e9 !important;
    border-bottom: 2px solid #0ea5e9 !important;
}

/* Input styling */
div[data-testid="stTextInput"],
div[data-testid="stPasswordInput"] {
    margin-bottom: 0.75rem !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stPasswordInput"] input {
    padding: 0.6rem 0.8rem !important;
    font-size: 0.95rem !important;
    border-radius: 10px !important;
}

div[data-testid="stFormSubmitButton"] button {
    padding: 0.75rem 1.5rem !important;
    font-size: 1rem !important;
    border-radius: 12px !important;
    margin-top: 0.5rem !important;
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(14, 165, 233, 0.3) !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4) !important;
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
}

div[data-testid="stFormSubmitButton"] button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(14, 165, 233, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

    # Logo Import & Encoding
    import base64
    import os
    
    def get_img_as_base64(file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except: return None

    logo_path = os.path.join(os.path.dirname(__file__), "..", "static", "logo.png")
    img_b64 = get_img_as_base64(logo_path)
    
    if img_b64:
        logo_html = f'<img src="data:image/png;base64,{img_b64}" style="width: 80px; height: 80px; object-fit: contain; filter: drop-shadow(0 0 15px rgba(255,255,255,0.1));">'
    else:
        logo_html = '<div style="font-size: 60px;">🏥</div>'
    
    col1, col2 = st.columns([1.2, 1])
    
    # Left - Branding
    with col1:
        st.markdown(f"""
<div style="padding: 2rem;">
    <div style="margin-bottom: 1.5rem;">
        {logo_html}
    </div>
    <h1 style="font-size: 3rem; margin: 0 0 1rem 0; color: #0f172a; line-height: 1.1; font-weight: 800;">
        AI<br>
        <span style="background: linear-gradient(90deg, #0ea5e9, #082f49); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Clinical Portal</span>
    </h1>
    <p style="font-size: 1.15rem; color: #475569; margin: 0 0 2rem 0; line-height: 1.6; max-width: 450px;">
        Advanced health intelligence for patients and professionals. Precise diagnostics, secure data, and real-time clinical advisory.
    </p>
    <div style="display: flex; gap: 1rem;">
        <div style="background: #ffffff; padding: 1rem 1.25rem; border-radius: 16px; border: 1px solid #e2e8f0; text-align: center; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);">
            <div style="font-size: 1.25rem; font-weight: 800; color: #0EA5E9;">99.8%</div>
            <div style="font-size: 0.8rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Precision</div>
        </div>
        <div style="background: #ffffff; padding: 1rem 1.25rem; border-radius: 16px; border: 1px solid #e2e8f0; text-align: center; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);">
            <div style="font-size: 1.25rem; font-weight: 800; color: #10B981;">Secured</div>
            <div style="font-size: 0.8rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">HIPAA/GDPR</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # Right - Auth Form
    with col2:
        st.markdown("""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <h2 style="font-size: 1.8rem; margin: 0; color: #0f172a; font-weight: 800;">Patient Access</h2>
    <p style="font-size: 1rem; color: #64748B; margin: 0.5rem 0 0 0; font-weight: 500;">Secure gateway for clinical services</p>
</div>
""", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])
        
        with tab1:
            with st.form("login", border=False):
                u = st.text_input("Username", placeholder="Enter username", label_visibility="collapsed")
                p = st.text_input("Password", type="password", placeholder="Enter password", label_visibility="collapsed")
                if st.form_submit_button("Sign In →", type="primary", width="stretch"):
                    if api.login(u, p): st.rerun()
                        
        with tab2:
            with st.form("signup", border=False):
                us = st.text_input("Username", placeholder="Choose a username", label_visibility="collapsed")
                em = st.text_input("Email", placeholder="Your email", label_visibility="collapsed")
                pw = st.text_input("Password", type="password", placeholder="Create password", label_visibility="collapsed")
                if st.form_submit_button("Register", type="primary", width="stretch"):
                    if api.signup(us, pw, em, us, "2000-01-01"):
                        if api.login(us, pw): st.rerun()
        
        st.markdown('<p style="text-align: center; font-size: 0.8rem; color: #475569; margin-top: 1rem;">Powered by Advanced AI</p>', unsafe_allow_html=True)
