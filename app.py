import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime

st.set_page_config(
    page_title="Kindergarten Road Map",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 1. VECTOR GRAPHICS ENGINE (AVATARS & BOOKS)
# =========================================================

def render_avatar(skin="#8d5524", hair_style="puffs", hair_color="#1a1110", glasses="gold_round", shirt="#ec4899", accessory="crown", size=180):
    hair_svg = ""
    if hair_style == "puffs":
        hair_svg = f"""
        <circle cx="50" cy="55" r="28" fill="{hair_color}"/>
        <circle cx="150" cy="55" r="28" fill="{hair_color}"/>
        <path d="M 65 75 Q 100 45 135 75 Q 100 65 65 75 Z" fill="{hair_color}"/>
        """
    elif hair_style == "curly_bob":
        hair_svg = f"""
        <circle cx="65" cy="80" r="24" fill="{hair_color}"/>
        <circle cx="135" cy="80" r="24" fill="{hair_color}"/>
        <path d="M 60 70 Q 100 35 140 70 Q 100 55 60 70 Z" fill="{hair_color}"/>
        """
    elif hair_style == "short_fade":
        hair_svg = f"""
        <path d="M 65 80 Q 100 40 135 80 Q 100 60 65 80 Z" fill="{hair_color}"/>
        <rect x="68" y="70" width="64" height="15" rx="7" fill="{hair_color}"/>
        """
    elif hair_style == "ponytail":
        hair_svg = f"""
        <circle cx="100" cy="40" r="26" fill="{hair_color}"/>
        <path d="M 68 75 Q 100 45 132 75 Z" fill="{hair_color}"/>
        <ellipse cx="100" cy="55" rx="14" ry="6" fill="#ec4899"/>
        """

    glasses_svg = ""
    if glasses == "gold_round":
        glasses_svg = """
        <circle cx="82" cy="100" r="15" fill="none" stroke="#f59e0b" stroke-width="4"/>
        <circle cx="118" cy="100" r="15" fill="none" stroke="#f59e0b" stroke-width="4"/>
        <line x1="97" y1="100" x2="103" y2="100" stroke="#f59e0b" stroke-width="4"/>
        <line x1="67" y1="98" x2="60" y2="92" stroke="#f59e0b" stroke-width="3"/>
        <line x1="133" y1="98" x2="140" y2="92" stroke="#f59e0b" stroke-width="3"/>
        """
    elif glasses == "cool_shades":
        glasses_svg = """
        <polygon points="82,85 86,95 96,96 88,103 91,113 82,107 73,113 76,103 68,96 78,95" fill="#8b5cf6"/>
        <polygon points="118,85 122,95 132,96 124,103 127,113 118,107 109,113 112,103 104,96 114,95" fill="#8b5cf6"/>
        <line x1="94" y1="101" x2="106" y2="101" stroke="#6d28d9" stroke-width="4"/>
        """

    acc_svg = ""
    if accessory == "crown":
        acc_svg = """
        <polygon points="75,55 85,35 100,50 115,35 125,55" fill="#facc15" stroke="#eab308" stroke-width="2"/>
        <circle cx="100" cy="48" r="3" fill="#ef4444"/>
        """
    elif accessory == "cape":
        acc_svg = """
        <path d="M 55 140 Q 30 180 40 200 Q 100 190 160 200 Q 170 180 145 140 Z" fill="#ef4444"/>
        """

    raw_html = f"""
    <div style="display:flex; justify-content:center; align-items:center; width:100%; margin:0; padding:0;">
        <svg width="{size}" height="{size}" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="glow_{size}" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#ffffff"/>
                    <stop offset="100%" stop-color="#e0f2fe"/>
                </radialGradient>
            </defs>
            <circle cx="100" cy="100" r="95" fill="url(#glow_{size})" stroke="#38bdf8" stroke-width="6"/>
            {acc_svg if accessory == "cape" else ""}
            <path d="M 60 185 C 60 145, 140 145, 140 185 Z" fill="{shirt}"/>
            <path d="M 85 145 Q 100 160 115 145 Z" fill="{skin}"/>
            <rect x="91" y="132" width="18" height="18" rx="6" fill="{skin}"/>
            <ellipse cx="100" cy="100" rx="36" ry="42" fill="{skin}"/>
            <circle cx="63" cy="102" r="9" fill="{skin}"/>
            <circle cx="137" cy="102" r="9" fill="{skin}"/>
            {hair_svg}
            <ellipse cx="84" cy="98" rx="6" ry="8" fill="#ffffff"/>
            <circle cx="85" cy="98" r="4.5" fill="#0f172a"/>
            <circle cx="87" cy="95" r="1.5" fill="#ffffff"/>
            <ellipse cx="116" cy="98" rx="6" ry="8" fill="#ffffff"/>
            <circle cx="115" cy="98" r="4.5" fill="#0f172a"/>
            <circle cx="117" cy="95" r="1.5" fill="#ffffff"/>
            <ellipse cx="78" cy="109" rx="6" ry="3.5" fill="#f43f5e" opacity="0.35"/>
            <ellipse cx="122" cy="109" rx="6" ry="3.5" fill="#f43f5e" opacity="0.35"/>
            <path d="M 90 115 Q 100 128 110 115" fill="none" stroke="#78350f" stroke-width="3" stroke-linecap="round"/>
            {glasses_svg}
            {acc_svg if accessory != "cape" else ""}
        </svg>
    </div>
    """
    return raw_html

def render_book_diagram(part="spine"):
    spine_border = 'stroke="#facc15" stroke-width="6"' if part == "spine" else 'stroke="#1e3a8a" stroke-width="2"'
    cover_border = 'stroke="#facc15" stroke-width="6"' if part == "cover" else 'stroke="#2563eb" stroke-width="2"'
    raw_html = f"""
    <div style="display:flex; justify-content:center; align-items:center; width:100%;">
        <svg width="280" height="210" viewBox="0 0 280 210" xmlns="http://www.w3.org/2000/svg">
            <rect x="25" y="25" width="230" height="160" rx="14" fill="#60a5fa" {cover_border}/>
            <rect x="25" y="25" width="40" height="160" rx="6" fill="#1d4ed8" {spine_border}/>
            <line x1="38" y1="40" x2="38" y2="170" stroke="#93c5fd" stroke-width="3" stroke-dasharray="6,4"/>
            <rect x="80" y="45" width="160" height="42" rx="8" fill="#ffffff"/>
            <text x="160" y="71" font-family="'Fredoka', sans-serif" font-size="15" font-weight="900" fill="#1e40af" text-anchor="middle">THE BRAVE PUPPY</text>
            <circle cx="160" cy="120" r="24" fill="#fef08a"/>
            <ellipse cx="152" cy="116" rx="3.5" ry="4.5" fill="#0f172a"/>
            <ellipse cx="168" cy="116" rx="3.5" ry="4.5" fill="#0f172a"/>
            <ellipse cx="160" cy="124" rx="4.5" ry="3" fill="#78350f"/>
            <rect x="90" y="152" width="140" height="22" rx="6" fill="#ffffffcc"/>
            <text x="160" y="167" font-family="'Fredoka', sans-serif" font-size="11" font-weight="800" fill="#334155" text-anchor="middle">By Raeven Brown</text>
        </svg>
    </div>
    """
    components.html(raw_html, height=220)

def render_candy_jars(count1=10, count2=8):
    def build_beans(count, col):
        out = ""
        for i in range(count):
            bx = 35 + (i % 3) * 18
            by = 115 - (i // 3) * 18
            out += f'<ellipse cx="{bx}" cy="{by}" rx="7" ry="5" fill="{col}" stroke="#fff" stroke-width="1.5"/>'
        return out

    raw_html = f"""
    <div style="display:flex; justify-content:center; gap:20px; align-items:center;">
        <svg width="110" height="140" viewBox="0 0 110 140">
            <rect x="30" y="10" width="50" height="12" rx="4" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
            <path d="M 25 25 Q 15 35 15 60 L 15 120 Q 15 135 25 135 L 85 135 Q 95 135 95 120 L 95 60 Q 95 35 85 25 Z" fill="#e0f2fe" opacity="0.85" stroke="#0284c7" stroke-width="3"/>
            {build_beans(count1, "#ef4444")}
        </svg>
        <svg width="110" height="140" viewBox="0 0 110 140">
            <rect x="30" y="10" width="50" height="12" rx="4" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
            <path d="M 25 25 Q 15 35 15 60 L 15 120 Q 15 135 25 135 L 85 135 Q 95 135 95 120 L 95 60 Q 95 35 85 25 Z" fill="#e0f2fe" opacity="0.85" stroke="#0284c7" stroke-width="3"/>
            {build_beans(count2, "#22c55e")}
        </svg>
    </div>
    """
    components.html(raw_html, height=150)

# =========================================================
# 2. STYLING & AUDIO SYNTHESIZER
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700;800&family=Quicksand:wght@600;700;800&display=swap');

    .stApp {
        background: linear-gradient(180deg, #60a5fa 0%, #93c5fd 45%, #bbf7d0 100%) !important;
        font-family: 'Fredoka', 'Quicksand', cursive, sans-serif !important;
    }

    .stButton > button {
        border-radius: 28px !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        padding: 12px 20px !important;
        background: #ffffff !important;
        color: #0369a1 !important;
        border: 4px solid #38bdf8 !important;
        box-shadow: 0 8px 0 #0284c7, 0 12px 20px rgba(0,0,0,0.12) !important;
        transition: transform 0.08s ease !important;
        width: 100%;
    }
    .stButton > button:active {
        transform: translateY(6px) !important;
        box-shadow: 0 2px 0 #0284c7 !important;
    }

    .game-card {
        background: #ffffff;
        border: 5px solid #38bdf8;
        border-radius: 32px;
        padding: 22px;
        box-shadow: 0 14px 30px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 18px;
    }

    .stat-chip {
        background: #fef08a;
        color: #854d0e;
        border-radius: 20px;
        padding: 6px 16px;
        font-weight: 800;
        font-size: 1.2rem;
        border: 2px solid #facc15;
    }
</style>
""", unsafe_allow_html=True)

def speak(text):
    clean = text.replace('"', '\\"').replace("'", "\\'")
    js = f"""
    <script>
        (function() {{
            const synth = (window.parent && window.parent.speechSynthesis) ? window.parent.speechSynthesis : window.speechSynthesis;
            if (!synth) return;
            try {{
                synth.cancel();
                if (synth.paused) synth.resume();
            }} catch(e) {{}}
            const utter = new SpeechSynthesisUtterance("{clean}");
            utter.rate = 0.85;
            utter.pitch = 1.22;
            utter.lang = 'en-US';
            const voices = synth.getVoices();
            if (voices.length > 0) {{
                const pref = voices.find(v => (v.name.includes("Samantha") || v.name.includes("Victoria") || v.lang === "en-US") && !v.name.includes("Bad"));
                if (pref) utter.voice = pref;
            }}
            synth.speak(utter);
        }})();
    </script>
    """
    components.html(js, height=0)

# =========================================================
# 3. PERSISTENT PROFILES & STATE MANAGEMENT
# =========================================================

if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "Gracyn": {
            "buddy": {
                "skin": "#8d5524",
                "hair_style": "puffs",
                "hair_color": "#1a1110",
                "glasses": "gold_round",
                "shirt": "#ec4899",
                "accessory": "crown"
            },
            "stars": 14,
            "streak": 3,
            "unlocked_level": 1,
            "level_progress": {"level_1_step": 0, "level_2_step": 0, "level_3_step": 0},
            "daily_log": []
        },
        "Jaxson": {
            "buddy": {
                "skin": "#e0ac69",
                "hair_style": "short_fade",
                "hair_color": "#271810",
                "glasses": "none",
                "shirt": "#3b82f6",
                "accessory": "cape"
            },
            "stars": 8,
            "streak": 2,
            "unlocked_level": 1,
            "level_progress": {"level_1_step": 0, "level_2_step": 0, "level_3_step": 0},
            "daily_log": []
        }
    }

if "active_user" not in st.session_state:
    st.session_state.active_user = "Gracyn"

if "screen" not in st.session_state:
    st.session_state.screen = "profile_select"

if "active_activity" not in st.session_state:
    st.session_state.active_activity = "sight_words"

# =========================================================
# SCREEN 1: PROFILE HUB
# =========================================================
if st.session_state.screen == "profile_select":
    st.markdown("""
    <div style="text-align:center; padding: 18px 0 10px 0;">
        <h1 style="color:#0369a1; font-size:3.2rem; font-weight:900; margin-bottom:4px;">ADVENTURE LEARNING ACADEMY</h1>
        <p style="font-size:1.5rem; color:#1e293b; font-weight:800;">Who is playing today? Tap your character!</p>
    </div>
    """, unsafe_allow_html=True)
    speak("Who is playing today? Tap your character or design a new buddy!")

    prof_names = list(st.session_state.profiles.keys())
    cols = st.columns(len(prof_names) + 1)

    for i, name in enumerate(prof_names):
        p_data = st.session_state.profiles[name]
        b = p_data["buddy"]
        with cols[i]:
            avatar_html = render_avatar(skin=b["skin"], hair_style=b["hair_style"], hair_color=b["hair_color"], glasses=b["glasses"], shirt=b["shirt"], accessory=b["accessory"], size=180)
            components.html(avatar_html, height=190)
            if st.button(f"Play as {name}", key=f"prof_{name}", use_container_width=True):
                st.session_state.active_user = name
                st.session_state.screen = "adventure_trail"
                speak(f"Welcome back {name}! Complete all questions in each level to advance!")
                st.rerun()

    with cols[-1]:
        raw_plus = """
        <div style="display:flex; justify-content:center; align-items:center; width:100%;">
            <svg width="180" height="180" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="90" fill="#f8fafc" stroke="#94a3b8" stroke-width="6" stroke-dasharray="12,8"/>
                <line x1="100" y1="65" x2="100" y2="135" stroke="#0284c7" stroke-width="12" stroke-linecap="round"/>
                <line x1="65" y1="100" x2="135" y2="100" stroke="#0284c7" stroke-width="12" stroke-linecap="round"/>
            </svg>
        </div>
        """
        components.html(raw_plus, height=190)
        if st.button("New Buddy Studio", use_container_width=True):
            st.session_state.screen = "buddy_dressup"
            st.rerun()

# =========================================================
# SCREEN 2: BUDDY DRESS-UP STUDIO
# =========================================================
elif st.session_state.screen == "buddy_dressup":
    st.markdown("""
    <div class="game-card" style="padding:14px; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h2 style="color:#0369a1; font-size:2.2rem; margin:0;">BUDDY DRESS-UP STUDIO</h2>
            <p style="color:#475569; font-weight:700; font-size:1.15rem; margin:4px 0 0 0;">Create a custom avatar for your new learning profile!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    speak("Design your buddy! Pick hairstyles, skin tones, and outfits!")

    if "temp_buddy" not in st.session_state:
        st.session_state.temp_buddy = {"skin": "#c68642", "hair_style": "puffs", "hair_color": "#1a1110", "glasses": "gold_round", "shirt": "#0284c7", "accessory": "crown"}

    tb = st.session_state.temp_buddy
    col_preview, col_options = st.columns([1.1, 1.4])

    with col_preview:
        avatar_html = render_avatar(skin=tb['skin'], hair_style=tb['hair_style'], hair_color=tb['hair_color'], glasses=tb['glasses'], shirt=tb['shirt'], accessory=tb['accessory'], size=230)
        components.html(avatar_html, height=240)
        new_profile_name = st.text_input("Enter Profile Name:", value="Superstar")
        if st.button("Save & Start Learning!", use_container_width=True):
            clean_name = new_profile_name.strip() if new_profile_name.strip() else "Learner"
            st.session_state.profiles[clean_name] = {
                "buddy": tb,
                "stars": 10,
                "streak": 1,
                "unlocked_level": 1,
                "level_progress": {"level_1_step": 0, "level_2_step": 0, "level_3_step": 0},
                "daily_log": []
            }
            st.session_state.active_user = clean_name
            st.session_state.screen = "adventure_trail"
            speak(f"Awesome! Welcome to Adventure Academy, {clean_name}!")
            st.rerun()

        if st.button("⬅️ Back to Profiles", use_container_width=True):
            st.session_state.screen = "profile_select"
            st.rerun()

    with col_options:
        tab_h, tab_s, tab_c, tab_a = st.tabs(["Hairstyle", "Skin Tone", "Outfit", "Accessories"])
        with tab_h:
            h1, h2 = st.columns(2)
            if h1.button("Afro Puffs"): tb["hair_style"] = "puffs"; st.rerun()
            if h2.button("Curly Bob"): tb["hair_style"] = "curly_bob"; st.rerun()
            if h1.button("Fresh Fade"): tb["hair_style"] = "short_fade"; st.rerun()
            if h2.button("Ponytail"): tb["hair_style"] = "ponytail"; st.rerun()
        with tab_s:
            s1, s2, s3, s4 = st.columns(4)
            if s1.button("Deep"): tb["skin"] = "#5c3818"; st.rerun()
            if s2.button("Bronze"): tb["skin"] = "#8d5524"; st.rerun()
            if s3.button("Tan"): tb["skin"] = "#c68642"; st.rerun()
            if s4.button("Peach"): tb["skin"] = "#f1c27d"; st.rerun()
        with tab_c:
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("Pink"): tb["shirt"] = "#ec4899"; st.rerun()
            if c2.button("Sky"): tb["shirt"] = "#0284c7"; st.rerun()
            if c3.button("Gold"): tb["shirt"] = "#eab308"; st.rerun()
            if c4.button("Green"): tb["shirt"] = "#16a34a"; st.rerun()
        with tab_a:
            a1, a2 = st.columns(2)
            if a1.button("Gold Glasses"): tb["glasses"] = "gold_round"; st.rerun()
            if a2.button("Star Shades"): tb["glasses"] = "cool_shades"; st.rerun()
            if a1.button("Royal Crown"): tb["accessory"] = "crown"; st.rerun()
            if a2.button("Hero Cape"): tb["accessory"] = "cape"; st.rerun()

# =========================================================
# SCREEN 3: KINDERGARTEN ROAD MAP (UNCLIPPED FULL CONTAINER)
# =========================================================
elif st.session_state.screen == "adventure_trail":
    user = st.session_state.active_user
    pdata = st.session_state.profiles[user]
    b = pdata["buddy"]
    unlocked_lvl = pdata.get("unlocked_level", 1)

    col_lib, col_title, col_prof = st.columns([1, 3, 1])
    with col_lib:
        if st.button("📚 Library"):
            st.session_state.active_activity = "parent_portal"
            st.session_state.current_level_num = 8
            st.session_state.screen = "station_play"
            st.rerun()
    with col_title:
        st.markdown("<h1 style='text-align:center; color:#0f172a; margin:0; font-size:2.8rem;'>🌱 Kindergarten Road Map</h1>", unsafe_allow_html=True)
    with col_prof:
        if st.button("Switch Profile", key="switch_p", use_container_width=True):
            st.session_state.screen = "profile_select"
            st.rerun()

    speak(f"Welcome to your Kindergarten Road Map {user}! Complete all mastery tasks in each level to advance down the road!")

    # UNCLIPPED FULL MAP CONTAINER WITH 520px HEIGHT
    map_container_html = f"""
    <div style="background:linear-gradient(135deg, #e0f2fe, #bae6fd); border:5px solid #0284c7; border-radius:36px; padding:35px 30px; box-shadow:0 16px 32px rgba(0,0,0,0.12); position:relative; margin:20px auto; width:100%; box-sizing:border-box;">
        <svg width="100%" height="320" viewBox="0 0 900 320" xmlns="http://www.w3.org/2000/svg" style="overflow:visible;">
            <!-- Winding Path Road -->
            <path d="M 50 200 Q 220 50 450 180 Q 680 310 820 160" fill="none" stroke="#64748b" stroke-width="22" stroke-linecap="round" opacity="0.6"/>
            
            <!-- LEVEL 1 CARD -->
            <g transform="translate(80, 110)">
                <rect x="0" y="0" width="130" height="85" rx="16" fill="#ffffff" stroke="#0284c7" stroke-width="5"/>
                <text x="65" y="35" font-family="'Fredoka', sans-serif" font-size="15" font-weight="900" fill="#0369a1" text-anchor="middle">📖 Sight Words</text>
                <text x="65" y="60" font-family="'Fredoka', sans-serif" font-size="14" font-weight="800" fill="#1e293b" text-anchor="middle">Level 1 (Active)</text>
            </g>

            <!-- LEVEL 2 CARD -->
            <g transform="translate(280, 45)">
                <rect x="0" y="0" width="130" height="85" rx="16" fill="#ffffff" stroke="{'#10b981' if unlocked_lvl >= 2 else '#94a3b8'}" stroke-width="5"/>
                <text x="65" y="35" font-family="'Fredoka', sans-serif" font-size="15" font-weight="900" fill="{'#047857' if unlocked_lvl >= 2 else '#94a3b8'}" text-anchor="middle">📚 Book Parts</text>
                <text x="65" y="60" font-family="'Fredoka', sans-serif" font-size="14" font-weight="800" fill="{('#047857' if unlocked_lvl >= 2 else '#94a3b8')}">{'Level 2' if unlocked_lvl >= 2 else '🔒 Locked'}</text>
            </g>

            <!-- LEVEL 3 CARD -->
            <g transform="translate(480, 165)">
                <rect x="0" y="0" width="130" height="85" rx="16" fill="#ffffff" stroke="{'#f59e0b' if unlocked_lvl >= 3 else '#94a3b8'}" stroke-width="5"/>
                <text x="65" y="35" font-family="'Fredoka', sans-serif" font-size="15" font-weight="900" fill="{'#b45309' if unlocked_lvl >= 3 else '#94a3b8'}" text-anchor="middle">🕵️ Numbers</text>
                <text x="65" y="60" font-family="'Fredoka', sans-serif" font-size="14" font-weight="800" fill="{('#b45309' if unlocked_lvl >= 3 else '#94a3b8')}">{'Level 3' if unlocked_lvl >= 3 else '🔒 Locked'}</text>
            </g>

            <!-- Learning House on the Right with Giant Play Button -->
            <g transform="translate(680, 20)">
                <polygon points="100,10 15,85 185,85" fill="#991b1b"/>
                <rect x="30" y="85" width="140" height="110" fill="#f8fafc" stroke="#475569" stroke-width="4"/>
                <rect x="75" y="125" width="50" height="70" rx="6" fill="#78350f"/>
                <circle cx="100" cy="115" r="32" fill="#14b8a6" stroke="#ffffff" stroke-width="4"/>
                <polygon points="90,102 90,128 116,115" fill="#ffffff"/>
            </g>
        </svg>

        <!-- Companion Animals along the bottom -->
        <div style="display:flex; justify-content:center; gap:45px; align-items:flex-end; margin-top:20px;">
            <div style="font-size:3.5rem;">🐘</div>
            <div style="font-size:3.5rem;">🦊</div>
            <div style="font-size:3rem;">🦜</div>
            <div style="font-size:3.5rem;">🦭</div>
        </div>
    </div>
    """
    components.html(map_container_html, height=520)

    # NATIVE, 100% RELIABLE CLICKABLE LEVEL BUTTONS RIGHT BELOW THE FULL BOX
    st.markdown("### 🚀 Click a Level to Complete Mastery:", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("📖 Play Level 1: Sight Words", use_container_width=True):
            st.session_state.active_activity = "sight_words"
            st.session_state.current_level_num = 1
            st.session_state.screen = "station_play"
            st.rerun()
            
    with c2:
        if unlocked_lvl >= 2:
            if st.button("📚 Play Level 2: Book Parts", use_container_width=True):
                st.session_state.active_activity = "book_parts"
                st.session_state.current_level_num = 2
                st.session_state.screen = "station_play"
                st.rerun()
        else:
            if st.button("🔒 Level 2 (Locked)", use_container_width=True):
                speak("Level 2 is locked! Complete all 3 questions in Level 1 first!")
                st.warning("🔒 Level 2 is locked! Complete Level 1 mastery first.")

    with c3:
        if unlocked_lvl >= 3:
            if st.button("🕵️ Play Level 3: Numbers", use_container_width=True):
                st.session_state.active_activity = "numbers"
                st.session_state.current_level_num = 3
                st.session_state.screen = "station_play"
                st.rerun()
        else:
            if st.button("🔒 Level 3 (Locked)", use_container_width=True):
                speak("Level 3 is locked! Complete Level 2 first!")
                st.warning("🔒 Level 3 is locked! Complete Level 2 mastery first.")

# =========================================================
# SCREEN 4: INDIVIDUAL STATION PLAY ARENA (MULTI-QUESTION MASTERY LOOP)
# =========================================================
elif st.session_state.screen == "station_play":
    user = st.session_state.active_user
    pdata = st.session_state.profiles[user]
    act = st.session_state.active_activity
    lvl_num = st.session_state.get("current_level_num", 1)

    if "level_progress" not in pdata:
        pdata["level_progress"] = {"level_1_step": 0, "level_2_step": 0, "level_3_step": 0}

    step_key = f"level_{lvl_num}_step"
    current_step = pdata["level_progress"].get(step_key, 0)

    # Top Navigation Bar
    b1, b2, b3 = st.columns([1, 1, 1])
    with b1:
        if st.button("🗺️ Back to Road Map"):
            st.session_state.screen = "adventure_trail"
            st.rerun()
    with b2:
        if st.button("🏠 Switch Profile"):
            st.session_state.screen = "profile_select"
            st.rerun()
    with b3:
        st.markdown(f"<div class='stat-chip' style='text-align:center;'>⭐ {pdata['stars']} Stars</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # LEVEL 1: SIGHT WORDS (3 Mastery Questions)
    # ---------------------------------------------------------
    if act == "sight_words":
        q_list = [
            {"word": "THE", "correct": "the", "opts": ["the", "and", "was"], "hint": "Starts with T!"},
            {"word": "AND", "correct": "and", "opts": ["you", "and", "see"], "hint": "Starts with A!"},
            {"word": "YOU", "correct": "you", "opts": ["can", "was", "you"], "hint": "Starts with Y!"}
        ]

        if current_step < len(q_list):
            q = q_list[current_step]
            speak(f"Mastery Question {current_step + 1} of 3: Which word says {q['word']}?")

            st.markdown(f"""
            <div class="game-card">
                <h3 style="color:#ef4444; font-size:1.6rem; margin:0;">SIGHT WORD MASTERY (Level 1 — Question {current_step + 1} / 3)</h3>
                <div style="font-size:5rem; font-weight:900; color:#dc2626; letter-spacing:6px; margin: 10px 0;">
                    {q['word']}
                </div>
                <p style="font-size:1.2rem; font-weight:800; color:#64748b;">Complete all 3 questions correctly to master Level 1 and unlock Level 2!</p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l1_opt_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            pdata["level_progress"][step_key] += 1
                            pdata["stars"] += 1
                            st.balloons()
                            speak("Correct mastery answer!")
                            if pdata["level_progress"][step_key] >= len(q_list):
                                if pdata["unlocked_level"] < 2:
                                    pdata["unlocked_level"] = 2
                                speak("Fantastic! Level 1 fully mastered! Level 2 is now unlocked!")
                                st.success("🎉 **Level 1 Fully Mastered!** Level 2 is now Unlocked!")
                            st.rerun()
                        else:
                            speak(f"Not quite! Remember: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.markdown("""
            <div class="game-card" style="background:#dcfce7; border-color:#22c55e;">
                <h2 style="color:#166534;">🎉 Level 1 Fully Mastered!</h2>
                <p style="font-size:1.3rem; font-weight:800; color:#14532d;">You have successfully completed all mastery questions for Level 1. Level 2 is unlocked!</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🗺️ Return to Road Map & Play Level 2", use_container_width=True):
                st.session_state.screen = "adventure_trail"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 2: BOOK PARTS (3 Mastery Questions)
    # ---------------------------------------------------------
    elif act == "book_parts":
        b_list = [
            {"q": "What is the side edge called that holds all the pages together?", "correct": "spine", "opts": ["spine", "cover", "title"], "hint": "It's like your backbone!"},
            {"q": "Where is the title and author displayed first?", "correct": "front cover", "opts": ["back cover", "front cover", "page 5"], "hint": "The very front of the book!"},
            {"q": "What do we turn gently to read the next page?", "correct": "page", "opts": ["spine", "page", "table"], "hint": "Thin paper sheet inside!"}
        ]

        if current_step < len(b_list):
            q = b_list[current_step]
            speak(f"Mastery Question {current_step + 1} of 3: {q['q']}")

            st.markdown(f"""
            <div class="game-card">
                <h3 style="color:#1d4ed8; font-size:1.6rem; margin:0;">BOOK DETECTIVE MASTERY (Level 2 — Question {current_step + 1} / 3)</h3>
                <p style="font-size:1.4rem; font-weight:800; color:#1e293b; margin:15px 0;">{q['q']}</p>
                <p style="font-size:1.1rem; font-weight:700; color:#64748b;">Complete all 3 questions correctly to master Level 2 and unlock Level 3!</p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt.title()}", key=f"l2_opt_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            pdata["level_progress"][step_key] += 1
                            pdata["stars"] += 1
                            st.balloons()
                            speak("Correct mastery answer!")
                            if pdata["level_progress"][step_key] >= len(b_list):
                                if pdata["unlocked_level"] < 3:
                                    pdata["unlocked_level"] = 3
                                speak("Fantastic! Level 2 fully mastered! Level 3 is now unlocked!")
                                st.success("🎉 **Level 2 Fully Mastered!** Level 3 is now Unlocked!")
                            st.rerun()
                        else:
                            speak(f"Not quite! Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.markdown("""
            <div class="game-card" style="background:#dcfce7; border-color:#22c55e;">
                <h2 style="color:#166534;">🎉 Level 2 Fully Mastered!</h2>
                <p style="font-size:1.3rem; font-weight:800; color:#14532d;">You have successfully completed all mastery questions for Level 2. Level 3 is unlocked!</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🗺️ Return to Road Map & Play Level 3", use_container_width=True):
                st.session_state.screen = "adventure_trail"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 3: NUMBERS (3 Mastery Questions)
    # ---------------------------------------------------------
    elif act == "numbers":
        n_list = [
            {"q": "Count the beans: 10 red + 8 green. How many total?", "correct": "18", "opts": ["14", "18", "20"], "hint": "10 plus 8 equals 18!"},
            {"q": "What number comes right after 15?", "correct": "16", "opts": ["14", "16", "17"], "hint": "15... 16!"},
            {"q": "Which number is greater: 12 or 19?", "correct": "19", "opts": ["12", "19", "Both equal"], "hint": "19 is bigger than 12!"}
        ]

        if current_step < len(n_list):
            q = n_list[current_step]
            speak(f"Mastery Question {current_step + 1} of 3: {q['q']}")

            st.markdown(f"""
            <div class="game-card">
                <h3 style="color:#b45309; font-size:1.6rem; margin:0;">NUMBER DETECTIVE MASTERY (Level 3 — Question {current_step + 1} / 3)</h3>
                <p style="font-size:1.4rem; font-weight:800; color:#1e293b; margin:15px 0;">{q['q']}</p>
                <p style="font-size:1.1rem; font-weight:700; color:#64748b;">Complete all 3 questions correctly to master Level 3!</p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l3_opt_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            pdata["level_progress"][step_key] += 1
                            pdata["stars"] += 1
                            st.balloons()
                            speak("Correct mastery answer!")
                            if pdata["level_progress"][step_key] >= len(n_list):
                                speak("Fantastic! Level 3 fully mastered!")
                                st.success("🎉 **Level 3 Fully Mastered!** Amazing job completing all levels!")
                            st.rerun()
                        else:
                            speak(f"Not quite! Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.markdown("""
            <div class="game-card" style="background:#dcfce7; border-color:#22c55e;">
                <h2 style="color:#166534;">🎉 Level 3 Fully Mastered!</h2>
                <p style="font-size:1.3rem; font-weight:800; color:#14532d;">You have successfully completed all mastery questions for Level 3. You are a Kindergarten Math Star!</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🗺️ Return to Road Map", use_container_width=True):
                st.session_state.screen = "adventure_trail"
                st.rerun()
