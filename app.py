import json
import os
import time
import urllib.request
import urllib.error
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="The Brown Girls Creative Studio | AI Growth Assistant",
    page_icon="🤎",
    layout="wide"
)

# 2. Studio Brand Styling
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stAppDeployButton {display: none;}
    a.anchorjs-link, [data-testid="stHeaderActionElements"] {display: none !important;}
    
    .stApp {
        background-color: #1A120B !important;
        background-image: 
            linear-gradient(to right, rgba(197, 155, 88, 0.08) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(197, 155, 88, 0.08) 1px, transparent 1px) !important;
        background-size: 44px 44px !important;
        color: #EADBC8 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .studio-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0px 24px 0px;
        border-bottom: 1px solid rgba(197, 155, 88, 0.18);
        margin-bottom: 30px;
    }

    .brand-logo {
        font-family: 'Fraunces', serif !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #FAF5E9 !important;
        text-decoration: none !important;
        letter-spacing: -0.3px !important;
        display: inline-flex !important;
        align-items: baseline !important;
        gap: 6px !important;
    }
    .brand-logo:hover, .brand-logo:visited, .brand-logo:active {
        color: #FAF5E9 !important;
        text-decoration: none !important;
    }
    .brand-logo .accent-gold {
        color: #C59B58 !important;
    }

    .nav-links {
        display: flex;
        gap: 24px;
        align-items: center;
        font-size: 13.5px;
        font-weight: 500;
        color: #D4C3B3;
    }
    
    .nav-audit-btn {
        background: #C59B58 !important;
        color: #1A120B !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        padding: 9px 18px !important;
        border-radius: 6px !important;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(197, 155, 88, 0.25) !important;
    }

    .section-eyebrow {
        color: #C59B58;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .hero-title {
        font-family: 'Fraunces', serif;
        font-size: 46px;
        font-weight: 700;
        line-height: 1.15;
        color: #FAF5E9;
        letter-spacing: -0.8px;
        margin-bottom: 16px;
    }
    .hero-title em {
        font-family: 'Fraunces', serif;
        font-style: italic;
        color: #C59B58;
        font-weight: 400;
    }

    .hero-sub {
        font-size: 15px;
        line-height: 1.65;
        color: #C4B5A5;
        max-width: 680px;
        margin-bottom: 32px;
    }

    label {
        color: #FAF5E9 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }
    
    div[data-baseweb="select"] {
        background-color: #140D07 !important;
        border: 1px solid rgba(197, 155, 88, 0.3) !important;
        border-radius: 6px !important;
        color: #FAF5E9 !important;
    }

    .stTextInput input {
        background-color: #140D07 !important;
        color: #FAF5E9 !important;
        border: 1px solid rgba(197, 155, 88, 0.3) !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
    }
    .stTextInput input:focus {
        border-color: #C59B58 !important;
        box-shadow: 0 0 0 1px #C59B58 !important;
    }

    .stButton button {
        background-color: #C59B58 !important;
        color: #1A120B !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(197, 155, 88, 0.25) !important;
    }
    .stButton button:hover {
        background-color: #D6AA66 !important;
        transform: translateY(-1px);
    }
    
    .status-badge {
        display: inline-block;
        font-size: 11px;
        padding: 4px 10px;
        border-radius: 12px;
        margin-bottom: 14px;
        font-weight: 600;
    }
    .status-live {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .status-demo {
        background: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 3. Top Studio Navigation Bar
st.markdown("""
<div class="studio-nav">
    <a href="https://raevenbrown.github.io/thebrowngirlsstudio/index.html#education" class="brand-logo" target="_blank">
        <span>the brown girls</span><span class="accent-gold">creative studio</span>
    </a>
    <div class="nav-links">
        <span>Studio Services</span>
        <span>Creative Metrix</span>
        <span>School Labs</span>
        <span>Apprenticeships</span>
        <a href="https://raevenbrown.github.io/thebrowngirlsstudio/index.html#education" target="_blank" class="nav-audit-btn">Run Free Audit</a>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Hero Section
st.markdown("""
<div class="section-eyebrow">— DATA ARCHITECTURE · AI INNOVATION · WORKFORCE IMPACT</div>
<div class="hero-title">Building the front end, back end, <em>and future</em> of local business.</div>
<div class="hero-sub">
    We turn disconnected operations into streamlined, data-driven growth machines with Creative Metrix — 
    while training the next generation of AI and tech talent right here in our community.
</div>
""", unsafe_allow_html=True)

# 5. Handle Authentication
raw_api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
api_key = str(raw_api_key).strip() if raw_api_key else ""

if api_key:
    st.markdown('<span class="status-badge status-live">🟢 LIVE ENGINE ACTIVE</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="status-badge status-demo">🟡 SIMULATOR MODE (Add GEMINI_API_KEY in Secrets)</span>', unsafe_allow_html=True)

STUDIO_SYSTEM_INSTRUCTION = (
    "You are the Principal Growth Architect for 'The Brown Girls Creative Studio'. "
    "Provide actionable, numbered steps with real revenue math, concrete timelines, and specific tools. "
    "Structure responses into: 1) Revenue Math, 2) Phase 1 (Days 1-30), 3) Phase 2 (Days 31-60), "
    "4) Phase 3 (Days 61-90), and 5) Executive Standard."
)

def query_gemini_api(key: str, user_prompt: str, persona: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}" if key.startswith("AIzaSy") else "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    payload = {
        "system_instruction": {"parts": [{"text": STUDIO_SYSTEM_INSTRUCTION}]},
        "contents": [{"parts": [{"text": f"Advisory Lens: {persona}\nGoal: {user_prompt}"}]}],
        "generationConfig": {"temperature": 0.7}
    }
    
    headers = {"Content-Type": "application/json"}
    if key.startswith("AQ."):
        headers["Authorization"] = f"Bearer {key}"
        
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result["candidates"][0]["content"]["parts"][0]["text"]

# 6. Interactive Studio AI Assistant Panel
st.markdown('<div class="section-eyebrow">— INTERACTIVE AI STRATEGY ENGINE</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    persona_options = [
        "Creative Entrepreneur",
        "Content & Brand Strategy",
        "Operations & Automation",
        "Brand Identity & Design",
        "Client Acquisition"
    ]
    selected_persona = st.selectbox("Select Advisory Lens:", persona_options)
    placeholder_map = {
        "Creative Entrepreneur": "How to get $7k in 3 months?",
        "Content & Brand Strategy": "How do I create short-form hooks that convert viewers into paying clients?",
        "Operations & Automation": "How do I automate client onboarding without writing complex code?",
        "Brand Identity & Design": "How do I position my business as an executive, high-ticket brand?",
        "Client Acquisition": "How do I pitch corporate clients and close bigger ongoing retainers?"
    }

with col2:
    user_input = st.text_input("Ask a Growth or Systems Question:", placeholder=placeholder_map[selected_persona])
    generate_btn = st.button("Generate Strategic Blueprint ✨")

# 7. Response Generation
if generate_btn:
    if not user_input.strip():
        st.warning("⚠️ Please enter a strategic question or goal above.")
    else:
        st.markdown(f"### Strategic Output: *{selected_persona}*")
        message_placeholder = st.empty()

        if api_key:
            try:
                with st.spinner("Generating Strategic Blueprint..."):
                    answer = query_gemini_api(api_key, user_input.strip(), selected_persona)
                
                full_text = ""
                for line in answer.split("\n"):
                    full_text += line + "\n"
                    message_placeholder.markdown(full_text + "▌")
                    time.sleep(0.015)
                message_placeholder.markdown(answer)

            except urllib.error.HTTPError as err:
                st.error(f"API Error ({err.code}): {err.read().decode('utf-8')}")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please verify your `GEMINI_API_KEY` is added under Streamlit Settings > Secrets.")
