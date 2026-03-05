"""
Pricing & Plans View
====================
Showcase subscription tiers to demonstrate commercial value.
Currently mostly static/mock updates, but essential for "sellability".
"""
import streamlit as st
import streamlit.components.v1 as components
from frontend.utils import api

def render_pricing_page():
    # --- STATE MANAGEMENT ---
    if 'show_payment' not in st.session_state:
        st.session_state.show_payment = False
        
    # --- PAYMENT VIEW (Modal-like "Middle Gateway") ---
    if st.session_state.show_payment:
        # Full width container for the payment experience
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h2 style="color: #0f172a; margin-bottom: 0.5rem; font-weight: 800;">Secure Payment Gateway</h2>
            <p style="color: #64748B; font-weight: 500;">Completing transaction for <b style="color: #0ea5e9;">Diagnostic Center License</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Centered Layout
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.info("Initializing Secure Connection to Razorpay...")
            
            # Create Order
            with st.spinner("Contacting Banking Servers..."):
                resp = api.create_payment_order(249900, "diagnostic_tier")
            
            if resp:
                order_id = resp['id']
                key_id = resp['key_id']
                amount = resp['amount']
                curr = resp['currency']
                
                # Full-size Payment Interface
                html_code = f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                <div style="background: #ffffff; padding: 30px; border-radius: 20px; text-align: center; color: #1e293b; border: 1.5px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                    <h3 style="margin-top:0; font-weight: 800; color: #0f172a;">Confirm Payment</h3>
                    <p style="font-size: 2rem; font-weight: 800; color: #0ea5e9;">₹2,499.00</p>
                    <p style="color: #64748b; margin-bottom: 25px; font-weight: 600;">Secure SSL Connection</p>
                    
                    <button id="rzp-button1" style="
                        background: linear-gradient(135deg, #0ea5e9, #0284c7); 
                        color: #ffffff; 
                        border: none; 
                        padding: 14px 24px; 
                        border-radius: 12px; 
                        font-weight: 700; 
                        font-size: 1.1rem;
                        cursor: pointer;
                        transition: all 0.2s;
                        width: 100%;
                        max-width: 300px;
                        box-shadow: 0 4px 14px rgba(14, 165, 233, 0.3);
                    ">Authorize Payment</button>
                    
                    <div id="payment-status" style="margin-top: 20px;"></div>
                </div>
                
                <script>
                    var options = {{
                        "key": "{key_id}", 
                        "amount": "{amount}", 
                        "currency": "{curr}",
                        "name": "AI Healthcare System",
                        "description": "Diagnostic Center License",
                        "image": "https://cdn-icons-png.flaticon.com/512/3063/3063823.png",
                        "order_id": "{order_id}",
                        "handler": function (response){{
                            document.getElementById('payment-status').innerHTML = '<p style="color:#4ADE80; font-weight:bold;">✅ Payment Successful! Redirecting...</p>';
                            // You could trigger a streamlit rerun/callback here if embedded differently
                            alert("Payment Successful! ID: " + response.razorpay_payment_id);
                        }},
                        "prefill": {{
                            "name": "Clinic Admin",
                            "email": "admin@clinic.com"
                        }},
                        "theme": {{
                            "color": "#3B82F6"
                        }},
                        "modal": {{
                            "ondismiss": function() {{
                                console.log('Checkout form closed');
                            }}
                        }}
                    }};
                    
                    var rzp1 = new Razorpay(options);
                    
                    document.getElementById('rzp-button1').onclick = function(e){{
                        rzp1.open();
                        e.preventDefault();
                    }}
                    
                    // Auto-open for convenience
                    setTimeout(function() {{ rzp1.open(); }}, 1000);
                </script>
                """
                components.html(html_code, height=600, scrolling=False)
                
                # Back Button
                if st.button("← Cancel & Return to Plans", key="cancel_pay"):
                    st.session_state.show_payment = False
                    st.rerun()
                    
            else:
                st.error("Could not initiate payment session. Please check your internet connection.")
                if st.button("← Go Back"):
                    st.session_state.show_payment = False
                    st.rerun()

        return # STOP execution here so we don't render pricing cards

    # --- PRICING CARDS VIEW (Default) ---
    # Inject responsive CSS for pricing cards
    st.markdown("""
<style>
/* Pricing Cards Container */
.pricing-card {
    background: #ffffff;
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    padding: 2rem;
    height: 100%;
    text-align: center;
    display: flex;
    flex-direction: column;
    font-family: "Manrope", sans-serif !important;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.pricing-card:hover {
    transform: translateY(-8px);
    border-color: #0ea5e9;
    box-shadow: 0 15px 35px rgba(14, 165, 233, 0.1);
}

.pricing-card h3 {
    margin-top: 0;
}

.pricing-price {
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    font-weight: 700;
    margin: 1rem 0;
}

.pricing-features {
    margin: 1.5rem 0;
    text-align: left;
    font-size: 0.9rem;
    flex-grow: 1;
}

.pricing-features div {
    margin-bottom: 0.5rem;
}

/* Mobile Responsive */
@media only screen and (max-width: 768px) {
    .pricing-card {
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .pricing-features {
        font-size: 0.85rem;
        margin: 1rem 0;
    }
}
</style>
""", unsafe_allow_html=True)
    
    st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <h1 style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 0.75rem; font-weight: 800;">Facility Intelligence Solutions</h1>
    <p style="color: #475569; font-size: clamp(1rem, 2.5vw, 1.25rem); max-width: 700px; margin: 0 auto; line-height: 1.6;">
        Deploy world-class predictive diagnostics and clinical decision support to your facility. Trusted by modern medical centers globally.
    </p>
</div>
""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # --- CLINIC TIER (Basic) ---
    with col1:
        st.markdown("""
<div class="pricing-card">
<h3 style="margin-top: 0; color: #0F172A; font-weight: 800;">Clinic Hub</h3>
<div style="font-size: 3rem; font-weight: 800; margin: 1.5rem 0; color: #0f172a;">Free</div>
<p style="color: #64748B; font-size: 0.95rem; font-weight: 600;">For local practitioners</p>
<div style="margin: 2rem 0; text-align: left; font-size: 0.95rem; color: #475569; line-height: 1.8;">
<div style="display: flex; gap: 8px;">✅ <span>Single Provider Access</span></div>
<div style="display: flex; gap: 8px;">✅ <span>100 Secure Patient Profiles</span></div>
<div style="display: flex; gap: 8px;">✅ <span>Core Diagnostic Screens</span></div>
<div style="display: flex; gap: 8px;">✅ <span>Standard Digital Reports</span></div>
</div>
<button style="width: 100%; background: #f1f5f9; color: #94A3B8; border: none; padding: 1rem; border-radius: 12px; font-weight: 700; cursor: default;">Current Enrolled</button>
</div>
""", unsafe_allow_html=True)

    # --- DIAGNOSTIC CENTER TIER (Pro) ---
    with col2:
        st.markdown("""
<div class="pricing-card" style="border: 2.5px solid #0ea5e9; border-bottom: none; border-radius: 24px 24px 0 0; position: relative;">
<div style="position: absolute; top: -14px; left: 50%; transform: translateX(-50%); background: #0ea5e9; color: white; padding: 4px 16px; border-radius: 20px; font-size: 0.8rem; font-weight: 800; letter-spacing: 0.05em;">ELITE CHOICE</div>
<h3 style="margin-top: 0; color: #0F172A; font-weight: 800;">Diagnostic Pro</h3>
<div style="font-size: 3rem; font-weight: 800; margin: 1.5rem 0; color: #0ea5e9;">
₹2,499<span style="font-size: 1.1rem; color: #64748B; font-weight: 600;">/mo</span>
</div>
<p style="color: #64748B; font-size: 0.95rem; font-weight: 600;">For advanced medical centers</p>
<div style="margin: 2rem 0; text-align: left; font-size: 0.95rem; color: #475569; line-height: 1.8;">
<div style="display: flex; gap: 8px;">✅ <span><b>Unlimited</b> Diagnostic Logs</span></div>
<div style="display: flex; gap: 8px;">✅ <span><b>Full Team</b> Multi-Login</span></div>
<div style="display: flex; gap: 8px;">✅ <span>Custom Branded Reports</span></div>
<div style="display: flex; gap: 8px;">✅ <span>Advanced API Integration</span></div>
<div style="display: flex; gap: 8px;">✅ <span>24/7 Clinical Support</span></div>
</div>
</div>
""", unsafe_allow_html=True)
        
        # Action Area
        st.markdown("""
<div style="background: #ffffff; border: 2.5px solid #0ea5e9; border-top: none; border-radius: 0 0 24px 24px; padding: 0 2rem 2.5rem 2rem; text-align: center;">
""", unsafe_allow_html=True)
        
        if st.button("Activate Pro License", key="upgrade_pro", type="primary", use_container_width=True):
             st.session_state.show_payment = True
             st.rerun()
 
        st.markdown("</div>", unsafe_allow_html=True)
        
    # --- HOSPITAL TIER ---
    with col3:
        st.markdown("""
<div class="pricing-card">
<h3 style="margin-top: 0; color: #0F172A; font-weight: 800;">Enterprise Net</h3>
<div style="font-size: 3rem; font-weight: 800; margin: 1.5rem 0; color: #0f172a;">Inquiry</div>
<p style="color: #64748B; font-size: 0.95rem; font-weight: 600;">For hospital ecosystems</p>
<div style="margin: 2rem 0; text-align: left; font-size: 0.95rem; color: #475569; line-height: 1.8;">
<div style="display: flex; gap: 8px;">✅ <span>Full HIS / EMR Sync</span></div>
<div style="display: flex; gap: 8px;">✅ <span>Custom Neural Model Tuning</span></div>
<div style="display: flex; gap: 8px;">✅ <span>On-Premise Infrastructure</span></div>
<div style="display: flex; gap: 8px;">✅ <span>Dedicated Compliance Officer</span></div>
</div>
<a href="mailto:solutions@antigravityhealth.com" style="text-decoration: none;">
<div style="width: 100%; background: linear-gradient(135deg, #0ea5e9, #0284c7); color: #ffffff; border: none; padding: 1rem; border-radius: 12px; font-weight: 800; text-align: center; box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);">Contact Solution Architects</div>
</a>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
<div style="text-align: center; margin-top: 2rem;">
<p style="color: #64748B; font-weight: 500;">
<b>HIPAA & GDPR Compliant.</b> Secure Bank-Grade Professional Encryption. <br>
Preferred partner for 50+ Modern Diagnostic Centers.
</p>
<div style="font-size: 1.5rem; margin-top: 1rem; opacity: 0.4;">
🏥 🔬 🧬
</div>
</div>
""", unsafe_allow_html=True)
