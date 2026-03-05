"""
Premium Sidebar Component - AI Healthcare System
=================================================
Clean, modern navigation using standard Streamlit components.
"""
import streamlit as st
from streamlit_option_menu import option_menu
from frontend.utils import api, i18n

def render_sidebar():
    """
    Renders a clean, modern sidebar with:
    1. Brand header
    2. Navigation menu
    3. User profile card
    4. Sign out button
    """
    
    # --- SIDEBAR RENDER ---
    with st.sidebar:
        # 0. Language Selector at TOP
        i18n.render_language_selector()
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
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
        
        # Use Image if available, else fallback to SVG or Emoji
        if img_b64:
            logo_html = f'<img src="data:image/png;base64,{img_b64}" style="width: 42px; height: 42px; object-fit: contain;">'
        else:
            logo_html = "🏥"

        st.markdown(f"""
<div style="display: flex; align-items: center; gap: 16px; padding: 25px 0 35px 0; font-family: 'Manrope', sans-serif;">
    <div style="background: #f0f9ff; padding: 10px; border-radius: 14px; border: 1.5px solid #d0e8ff; box-shadow: 0 4px 12px rgba(14, 165, 233, 0.1);">
        {logo_html}
    </div>
    <div style="line-height: 1.15;">
        <div style="font-size: 24px; font-weight: 800; color: #0F172A; letter-spacing: -0.04em; font-family: 'Manrope', sans-serif;">AI Health</div>
        <div style="font-size: 11px; color: #64748B; font-weight: 700; font-family: 'Manrope', sans-serif; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 2px;">Clinical Intelligence</div>
    </div>
</div>""".replace('\n', ''), unsafe_allow_html=True)
            
        st.markdown('<div style="height: 1px; background: #e2e8f0; margin-bottom: 20px;"></div>', unsafe_allow_html=True)

        # 2. User Info (Standard Streamlit Container)
        username = st.session_state.get('username', 'Guest')
        if username != 'Guest':
            with st.container():
                # Simple clean profile display
                # Simple clean profile display with Dynamic Picture
                pic = st.session_state.get('profile_picture')
                
                # Flattened HTML to prevent Markdown code block bugs
                if pic:
                    avatar_html = (
                        f'<div style="width: 38px; height: 38px; border-radius: 50%; overflow: hidden; border: 2px solid #e2e8f0;">'
                        f'<img src="{pic}" style="width: 100%; height: 100%; object-fit: cover;">'
                        f'</div>'
                    )
                else:
                    avatar_html = (
                        f'<div style="background: #f0f9ff; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #0ea5e9; border: 1.5px solid #d0e8ff;">'
                        f'{username[0].upper()}'
                        f'</div>'
                    )

                st.markdown(f"""
<div style="background-color: #f8fafc; padding: 12px; border-radius: 12px; display: flex; align-items: center; gap: 12px; margin-bottom: 25px; font-family: 'Manrope', sans-serif; border: 1px solid #e2e8f0;">
    {avatar_html}
    <div style="overflow: hidden;">
        <div style="font-weight: 700; font-size: 15px; color: #1e293b; font-family: 'Manrope', sans-serif; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{username}</div>
        <div style="font-size: 11px; color: #10B981; font-weight: 600; font-family: 'Manrope', sans-serif; display: flex; align-items: center; gap: 4px;">
            <div style="width: 6px; height: 6px; background: #10B981; border-radius: 50%;"></div> Active Profile
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        
        # 3. Navigation Menu Keys & Labels
        # We define internal keys to maintain selection when labels change (translations)
        menu_items = [
            ("dashboard", "speedometer2"),
            ("chat", "chat-dots"),
            ("diabetes_pred", "droplet"),
            ("heart_pred", "heart"),
            ("liver_pred", "clipboard2-pulse"),
            ("kidney_pred", "capsule"),
            ("lung_pred", "lungs"),
            ("profile", "person"),
            ("telemedicine", "camera-video"),
            ("about", "info-circle")
        ]
        
        # Add admin if role is admin
        user_role = st.session_state.get('role', 'patient')
        if user_role == 'admin':
            menu_items.insert(-1, ("admin", "shield-lock")) # Insert before 'about'
            
        nav_keys = [item[0] for item in menu_items]
        nav_options = [i18n.get_text(k) for k in nav_keys]
        nav_icons = [item[1] for item in menu_items]
        
        # Determine Default Index to keep selection when language switches
        # We use a secondary state 'active_nav_key' to track selection robustly
        if 'active_nav_key' not in st.session_state:
            st.session_state['active_nav_key'] = 'dashboard'
            
        try:
            default_ix = nav_keys.index(st.session_state['active_nav_key'])
        except ValueError:
            default_ix = 0

        selected_label = option_menu(
            menu_title=None,
            options=nav_options,
            icons=nav_icons,
            default_index=default_ix,
            key="main_sidebar_nav",
            styles={
                "container": {"background-color": "transparent", "padding": "0"},
                "icon": {"color": "#64748B", "font-size": "18px"}, 
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "12px",
                    "color": "#475569",
                    "font-family": "Manrope, sans-serif !important",
                    "font-weight": "500",
                },
                "nav-link-selected": {
                    "background-color": "#f0f9ff",
                    "color": "#0ea5e9",
                    "font-weight": "700",
                    "border-left": "4px solid #0ea5e9",
                    "font-family": "Manrope, sans-serif !important",
                },
            }
        )
        
        # Update hidden state with the English key of what was JUST clicked
        selected = i18n.get_english_key(selected_label)
        st.session_state['active_nav_key'] = selected
        
        # 4. Footer / Sign Out
        st.markdown("---")
        # Updated: use width='stretch' instead of deprecated use_container_width=True
        if st.button("🚪 Sign Out", key="logout_btn", type="secondary"): 
            api.clear_session()
            st.rerun()
            
        st.markdown("<div style='text-align: center; color: #334155; font-size: 11px; margin-top: 25px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;'>Hyper-Care v2.5 • Licensed Professional</div>", unsafe_allow_html=True)
    
    return selected
