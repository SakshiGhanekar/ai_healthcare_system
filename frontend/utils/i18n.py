"""
Internationalization (i18n) Utilities
=====================================
Simple dictionary-based translation for the frontend.
"""
import streamlit as st

# --- Translation Dictionary ---
TRANSLATIONS = {
    "en": {
        "dashboard": "Dashboard",
        "chat": "AI Chat Assistant",
        "profile": "My Profile",
        # "pricing": "Plans & Pricing",
        "telemedicine": "Telemedicine",
        "about": "About & Legal",
        "admin": "Admin Panel",
        "welcome": "Welcome back",
        "analyze": "Analyze Risk",
        "download_pdf": "Download Report",
        "diabetes_pred": "Diabetes",
        "heart_pred": "Heart Disease",
        "liver_pred": "Liver Disease",
        "kidney_pred": "Kidney Disease",
        "lung_pred": "Lung Cancer"
    },
    "hi": {
        "dashboard": "डैशबोर्ड",
        "chat": "एआई चैट सहायक",
        "profile": "मेरी प्रोफाइल",
        "pricing": "योजनाएं और मूल्य",
        "telemedicine": "टेलीमेडिसिन",
        "about": "हमारे बारे में",
        "admin": "एडमिन पैनल",
        "welcome": "वापसी पर स्वागत है",
        "analyze": "जोखिम विश्लेषण करें",
        "download_pdf": "रिपोर्ट डाउनलोड करें",
        "diabetes_pred": "मधुमेह भविष्यवाणी",
        "heart_pred": "हृदय रोग भविष्यवाणी",
        "liver_pred": "लिवर रोग भविष्यवाणी",
        "kidney_pred": "गुर्दा रोग भविष्यवाणी",
        "lung_pred": "फेफड़ों का कैंसर भविष्यवाणी"
    },
    "mr": {
        "dashboard": "डॅशबोर्ड",
        "chat": "AI चॅट असिस्टंट",
        "profile": "माझी प्रोफाइल",
        "pricing": "योजना आणि किंमत",
        "telemedicine": "टेलिमेडिसिन",
        "about": "आमच्याबद्दल",
        "admin": "अ‍ॅडमिन पॅनेल",
        "welcome": "परत स्वागत आहे",
        "analyze": "जोखिम विश्लेषण",
        "download_pdf": "अहवाल डाउनलोड करा",
        "diabetes_pred": "मधुमेह",
        "heart_pred": "हृदयरोग",
        "liver_pred": "यकृत रोग",
        "kidney_pred": "किडनी रोग",
        "lung_pred": "फुफ्फुसाचा कर्करोग"
    }
}

def get_text(key: str) -> str:
    """Get translated text for the current language."""
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

def render_language_selector():
    """Render a sidebar widget to switch languages."""
    st.markdown("""
<style>
/* Target text selectively in the sidebar to avoid breaking icons */
[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label {
    font-family: 'Manrope', sans-serif !important;
}

/* Specific selectbox text target */
div[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div {
    font-family: 'Manrope', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)
    lang = st.session_state.get('language', 'en')
    
    # Map codes to specific display names and indices
    options = ["English", "हिंदी (Hindi)", "मराठी (Marathi)"]
    codes = ["en", "hi", "mr"]
    
    current_index = 0
    if lang == 'hi': current_index = 1
    if lang == 'mr': current_index = 2
    
    selected_name = st.sidebar.selectbox(
        "🌐 Language",
        options,
        index=current_index,
        key="lang_selector"
    )
    
    # Update session state with code
    if selected_name == "English": st.session_state['language'] = 'en'
    elif selected_name == "हिंदी (Hindi)": st.session_state['language'] = 'hi'
    elif selected_name == "मराठी (Marathi)": st.session_state['language'] = 'mr'

def get_english_key(text: str) -> str:
    """Find the English key for a given translated text."""
    # Search all languages
    for lang, mapping in TRANSLATIONS.items():
        for key, val in mapping.items():
            if val == text:
                return key
    return text.lower().replace(" ", "_") # Fallback, though likely won't work for menus
