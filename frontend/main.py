"""
AI Healthcare System - Frontend Application
============================================

Main entry point. Orchestrates the UI using the Sidebar Navigation pattern.
Delegates logic to Views and Utilities.

Author: Sakshi Ghanekar
"""
import streamlit as st
import os
import sys

# Add project root to path to allow imports from frontend package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from streamlit_lottie import st_lottie
import requests
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx

# --- Import Custom Modules ---
from frontend.utils import api
from frontend.views import (
    auth_view, 
    dashboard_view, 
    profile_view, 
    chat_view, 
    diabetes_view, 
    heart_view, 
    liver_view,
    kidney_view,
    lungs_view
)

# --- Configuration ---
# Get logo path for favicon
import os as _os
_logo_path = _os.path.join(_os.path.dirname(__file__), "static", "logo.png")

st.set_page_config(
    page_title="AI Healthcare System",
    page_icon=_logo_path if _os.path.exists(_logo_path) else "🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Font Loader ---
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# --- CSS Injection ---
def local_css(file_name):
    # Early Font Load
    st.markdown('<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap" rel="stylesheet">', unsafe_allow_html=True)
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Style file not found: {file_name}")

# Adjust path relative to this script
css_path = os.path.join(os.path.dirname(__file__), "static", "style.css")
local_css(css_path)

# --- Animation Loader ---
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

from frontend.components import sidebar

# --- Main App Orchestrator ---
def main():
    # Initialize Cookie Manager for session persistence
    # Use a stable key across all calls
    if 'cookie_manager' not in st.session_state:
        st.session_state['cookie_manager'] = stx.CookieManager(key="auth_cookie_manager")
    
    # Attempt to restore session from cookies
    if 'token' not in st.session_state:
        session = api.load_session()
        
        # Streamlit-specific: The cookie manager might return None on the very first script run 
        # because the frontend component hasn't reported back yet. 
        # We check if cookies are set OR if we should wait.
        if session:
            st.session_state['token'] = session.get('token')
            st.session_state['username'] = session.get('username')
            
            # Fetch profile to restore Role/Pic if possible
            # This makes the UI feel consistent immediately after refresh
            try:
                prof = api.fetch_profile()
                if prof:
                    st.session_state['role'] = prof.get('role', 'patient')
                    st.session_state['profile_picture'] = prof.get('profile_picture')
            except:
                pass
            st.rerun() # Ensure sidebar is updated with the new state
    
    # If not logged in, show Auth Screen
    if 'token' not in st.session_state:
        # Before showing auth, wait a tiny bit for CookieManager if it's the first run
        # This prevents flickering to login page if cookies are just being slow
        import time
        if 'init_wait' not in st.session_state:
            st.session_state['init_wait'] = True
            time.sleep(0.5)
            st.rerun()
            
        auth_view.render_auth_page()
        return

    # Render Sidebar and get selection
    selected_label = sidebar.render_sidebar()
    
    # Resolve to English key for routing
    from frontend.utils import i18n
    selected = i18n.get_english_key(selected_label)

    
    
    # Routing Logic
    if selected == "dashboard":
        dashboard_view.render_dashboard()
    elif selected == "chat":
        chat_view.render_chat_page()
    elif selected == "diabetes_pred":
        diabetes_view.render_diabetes_page()
    elif selected == "heart_pred":
        heart_view.render_heart_page()
    elif selected == "liver_pred":
        liver_view.render_liver_page()
    elif selected == "kidney_pred":
        kidney_view.render_kidney_page()
    elif selected == "lung_pred":
        # Note: Module is named lungs_view
        lungs_view.render_lungs_page()
    elif selected == "profile":
        profile_view.render_profile_page()
    # elif selected == "pricing":
    #     from frontend.views import pricing_view
    #     pricing_view.render_pricing_page()
    elif selected == "telemedicine":
        from frontend.views import telemedicine_view
        telemedicine_view.render_telemedicine_page()
    elif selected == "about":
        from frontend.views import about_view
        about_view.render_about_page()
    elif selected == "admin":
        from frontend.views import admin_view
        admin_view.render_admin_page()

if __name__ == '__main__':
    main()
