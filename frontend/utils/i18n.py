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
        "telemedicine": "टेलीमेडिसिन",
        "about": "हमारे बारे में",
        "admin": "एडमिन पैनल",
        "welcome": "वापसी पर स्वागत है",
        "analyze": "जोखिम विश्लेषण करें",
        "download_pdf": "रिपोर्ट डाउनलोड करें",
        "diabetes_pred": "मधुमेह",
        "heart_pred": "हृदय रोग",
        "liver_pred": "यकृत रोग",
        "kidney_pred": "किडनी रोग",
        "lung_pred": "फेफड़ों का कैंसर"
    },
    "mr": {
        "dashboard": "डॅशबोर्ड",
        "chat": "AI चॅट असिस्टंट",
        "profile": "माझी प्रोफाइल",
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

def on_language_change():
    """Callback to handle language changes smoothly."""
    selected_name = st.session_state.lang_selector
    if selected_name == "English": 
        st.session_state['language'] = 'en'
    elif selected_name == "हिंदी (Hindi)": 
        st.session_state['language'] = 'hi'
    elif selected_name == "मराठी (Marathi)": 
        st.session_state['language'] = 'mr'
    st.rerun()

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
    
    # Initialize language if not present
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'
        
    lang = st.session_state['language']
    
    # Map codes to specific display names and indices
    options = ["English", "हिंदी (Hindi)", "मराठी (Marathi)"]
    
    current_index = 0
    if lang == 'hi': current_index = 1
    elif lang == 'mr': current_index = 2
    
    st.sidebar.selectbox(
        "🌐 Language",
        options,
        index=current_index,
        key="lang_selector",
        on_change=on_language_change
    )

def get_english_key(text: str) -> str:
    """Find the English key for a given translated text."""
    if not text:
        return "dashboard"
        
    # Search all languages in translation dictionary
    for lang_code, mapping in TRANSLATIONS.items():
        for key, val in mapping.items():
            if val == text:
                return key
                
    # If not found in primary translations, try lowercase conversion
    # This handles cases where the text might have been manipulated or is missing
    clean_text = text.lower().strip()
    
    # Check if it matches any English keys directly
    for key in TRANSLATIONS['en'].keys():
        if key == clean_text:
            return key
            
    return clean_text.replace(" ", "_")
