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
# 3. CURRICULUM DEFINITION (15 COMPLETE LEVELS)
# =========================================================

CURRICULUM_LEVELS = [
    {"id": "lvl_1", "name": "Level 1: List 1 Sight Words"},
    {"id": "lvl_2", "name": "Level 2: List 2 Sight Words"},
    {"id": "lvl_3", "name": "Level 3: Write & Type ABCs"},
    {"id": "lvl_4", "name": "Level 4: Count to 100 & What Comes Next"},
    {"id": "lvl_5", "name": "Level 5: Rhyming Words"},
    {"id": "lvl_6", "name": "Level 6: Syllables"},
    {"id": "lvl_7", "name": "Level 7: Addition Up to 10"},
    {"id": "lvl_8", "name": "Level 8: Subtraction Up to 10"},
    {"id": "lvl_9", "name": "Level 9: Upper & Lowercase Match"},
    {"id": "lvl_10", "name": "Level 10: Find Letters in ABCs"},
    {"id": "lvl_11", "name": "Level 11: Reading Picture Word Book"},
    {"id": "lvl_12", "name": "Level 12: Write a Sentence"},
    {"id": "lvl_13", "name": "Level 13: Count by 2s, 5s & 10s"},
    {"id": "lvl_14", "name": "Level 14: Personal Location (USA, GA, Covington, Belmont Circle)"},
    {"id": "lvl_15", "name": "Level 15: Spell Full Name (First, Middle, Last)"}
]

# =========================================================
# 4. PERSISTENT PROFILES & STATE MANAGEMENT
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
            "level_progress": {},
            "daily_log": []
        }
    }

if "active_user" not in st.session_state:
    st.session_state.active_user = "Gracyn"

if "screen" not in st.session_state:
    st.session_state.screen = "profile_select"

if "active_level_id" not in st.session_state:
    st.session_state.active_level_id = "lvl_1"

def record_progress(level_id, is_correct):
    user = st.session_state.active_user
    if user not in st.session_state.profiles:
        return
    prof = st.session_state.profiles[user]
    if "level_progress" not in prof:
        prof["level_progress"] = {}
    
    current_step = prof["level_progress"].get(level_id, 0)
    if is_correct:
        prof["stars"] += 1
        prof["streak"] += 1
        prof["level_progress"][level_id] = current_step + 1
        
        if prof["level_progress"][level_id] >= 3:
            for idx, lvl in enumerate(CURRICULUM_LEVELS):
                if lvl["id"] == level_id and prof["unlocked_level"] <= idx + 1:
                    if idx + 1 < len(CURRICULUM_LEVELS):
                        prof["unlocked_level"] = idx + 2

# =========================================================
# SCREEN 1: PROFILE HUB (WITH EXPLICIT DELETE PLAYER OPTION)
# =========================================================
if st.session_state.screen == "profile_select":
    st.markdown("""
    <div style="text-align:center; padding: 18px 0 10px 0;">
        <h1 style="color:#0369a1; font-size:3.2rem; font-weight:900; margin-bottom:4px;">ADVENTURE LEARNING ACADEMY</h1>
        <p style="font-size:1.5rem; color:#1e293b; font-weight:800;">Who is playing today? Tap your character or delete profiles below!</p>
    </div>
    """, unsafe_allow_html=True)
    speak("Who is playing today? Tap your character or design a new buddy!")

    prof_names = list(st.session_state.profiles.keys())
    cols = st.columns(len(prof_names) + 1)

    for i, name in enumerate(prof_names):
        p_data = st.session_state.profiles[name]
        b = p_data["buddy"]
        with cols[i]:
            avatar_html = render_avatar(skin=b["skin"], hair_style=b["hair_style"], hair_color=b["hair_color"], glasses=b["glasses"], shirt=b["shirt"], accessory=b["accessory"], size=160)
            components.html(avatar_html, height=170)
            
            if st.button(f"Play as {name}", key=f"prof_{name}", use_container_width=True):
                st.session_state.active_user = name
                st.session_state.screen = "adventure_trail"
                speak(f"Welcome back {name}! Follow your Kindergarten Road Map to learn and grow!")
                st.rerun()

            if st.button(f"🗑️ Delete {name}", key=f"del_{name}", use_container_width=True):
                if len(st.session_state.profiles) > 1:
                    del st.session_state.profiles[name]
                    remaining = list(st.session_state.profiles.keys())
                    st.session_state.active_user = remaining[0] if remaining else ""
                    speak(f"Player {name} deleted.")
                    st.success(f"🗑️ Player '{name}' deleted successfully!")
                    st.rerun()
                else:
                    st.warning("⚠️ You must keep at least one profile in the academy!")

    with cols[-1]:
        raw_plus = """
        <div style="display:flex; justify-content:center; align-items:center; width:100%;">
            <svg width="160" height="160" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="90" fill="#f8fafc" stroke="#94a3b8" stroke-width="6" stroke-dasharray="12,8"/>
                <line x1="100" y1="65" x2="100" y2="135" stroke="#0284c7" stroke-width="12" stroke-linecap="round"/>
                <line x1="65" y1="100" x2="135" y2="100" stroke="#0284c7" stroke-width="12" stroke-linecap="round"/>
            </svg>
        </div>
        """
        components.html(raw_plus, height=170)
        if st.button("New Buddy Studio", use_container_width=True):
            st.session_state.screen = "buddy_dressup"
            st.rerun()

# =========================================================
# SCREEN 2: BUDDY DRESS-UP STUDIO
# =========================================================
elif st.session_state.screen == "buddy_dressup":
    st.markdown("""
    <div class="game-card" style="padding:14px;">
        <h2 style="color:#0369a1; font-size:2.2rem; margin:0;">BUDDY DRESS-UP STUDIO</h2>
        <p style="color:#475569; font-weight:700; font-size:1.15rem; margin:4px 0 0 0;">Create your custom avatar for the Kindergarten Road Map!</p>
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
                "level_progress": {},
                "daily_log": []
            }
            st.session_state.active_user = clean_name
            st.session_state.screen = "adventure_trail"
            speak(f"Awesome! Welcome to Kindergarten Road Map, {clean_name}!")
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
# SCREEN 3: CANDY LAND ROAD MAP (COMPLETELY CLOSED GAP & PERFECTLY OUTLINED)
# =========================================================
elif st.session_state.screen == "adventure_trail":
    user = st.session_state.active_user
    if user not in st.session_state.profiles:
        st.session_state.screen = "profile_select"
        st.rerun()
        
    pdata = st.session_state.profiles[user]
    b = pdata["buddy"]
    unlocked_lvl = pdata.get("unlocked_level", 1)

    col_lib, col_title, col_prof = st.columns([1, 3, 1])
    with col_lib:
        if st.button("📚 Library"):
            st.session_state.active_level_id = "lvl_15"
            st.session_state.screen = "station_play"
            st.rerun()
    with col_title:
        st.markdown("<h1 style='text-align:center; color:#0f172a; margin:0; font-size:2.8rem;'>🌱 Kindergarten Road Map</h1>", unsafe_allow_html=True)
    with col_prof:
        if st.button("Switch Profile", key="switch_p", use_container_width=True):
            st.session_state.screen = "profile_select"
            st.rerun()

    speak(f"Welcome to your Kindergarten Road Map {user}! Follow the Candy Land trail from 1 to 15 and tap any unlocked level to play!")

    # REMOVED EXTRA BOTTOM PADDING & TIGHTENED MARGINS TO ELIMINATE THE BIG SPACE SHOWN BY THE RED LINE
    road_map_html = f"""
    <div style="background:linear-gradient(135deg, #e0f2fe, #bae6fd); border:5px solid #0284c7; border-radius:36px; padding:25px 20px 20px 20px; box-shadow:0 16px 32px rgba(0,0,0,0.12); position:relative; margin:10px auto; width:100%; box-sizing:border-box;">
        <div style="text-align:center; margin-bottom:10px;">
            <h2 style="color:#0369a1; margin:0; font-size:1.8rem;">🍭 Candy Land Winding Road Map (Level {unlocked_lvl} of 15 Unlocked)</h2>
            <p style="color:#334155; font-weight:700; font-size:1rem; margin-top:3px;">Follow the path from Level 1 to Level 15 to reach the house!</p>
        </div>

        <!-- SVG VIEWBOX & HEIGHT TIGHTLY OPTIMIZED SO EVERYTHING FITS FLUSH AND NO GIANT GAP REMAINS -->
        <svg width="100%" height="340" viewBox="0 0 1300 400" xmlns="http://www.w3.org/2000/svg" style="overflow:visible;">
            <!-- Winding Path Road -->
            <path d="M 60 280 Q 140 180 220 240 Q 300 300 380 160 Q 460 20 540 110 Q 620 200 700 60 Q 780 -80 860 20 Q 940 120 1020 -40 Q 1100 20 1180 -100" fill="none" stroke="#f43f5e" stroke-width="22" stroke-linecap="round" stroke-dasharray="16,12" opacity="0.85"/>

            <!-- LEVEL 1 -->
            <g transform="translate(40, 240)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=1'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 1 else '#38bdf8' if unlocked_lvl == 1 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#fff" text-anchor="middle">1</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Sight Words 1</text>
            </g>

            <!-- LEVEL 2 -->
            <g transform="translate(130, 160)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=2'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 2 else '#38bdf8' if unlocked_lvl == 2 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#fff" text-anchor="middle">2</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Sight Words 2</text>
            </g>

            <!-- LEVEL 3 -->
            <g transform="translate(220, 210)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=3'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 3 else '#38bdf8' if unlocked_lvl == 3 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#fff" text-anchor="middle">3</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">ABCs</text>
            </g>

            <!-- LEVEL 4 -->
            <g transform="translate(310, 260)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=4'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 4 else '#38bdf8' if unlocked_lvl == 4 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#fff" text-anchor="middle">4</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Count to 100</text>
            </g>

            <!-- LEVEL 5 -->
            <g transform="translate(400, 120)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=5'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 5 else '#38bdf8' if unlocked_lvl == 5 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#fff" text-anchor="middle">5</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Rhymes</text>
            </g>

            <!-- LEVEL 6 -->
            <g transform="translate(480, -20)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=6'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 6 else '#38bdf8' if unlocked_lvl == 6 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#fff" text-anchor="middle">6</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Syllables</text>
            </g>

            <!-- LEVEL 7 -->
            <g transform="translate(560, 30)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=7'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 7 else '#38bdf8' if unlocked_lvl == 7 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#fff" text-anchor="middle">7</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Addition</text>
            </g>

            <!-- LEVEL 8 -->
            <g transform="translate(640, 100)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=8'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 8 else '#38bdf8' if unlocked_lvl == 8 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#fff" text-anchor="middle">8</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Subtraction</text>
            </g>

            <!-- LEVEL 9 -->
            <g transform="translate(710, 20)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=9'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 9 else '#38bdf8' if unlocked_lvl == 9 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#fff" text-anchor="middle">9</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Upper/Lower</text>
            </g>

            <!-- LEVEL 10 -->
            <g transform="translate(770, -80)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=10'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 10 else '#38bdf8' if unlocked_lvl == 10 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="13" font-weight="900" fill="#fff" text-anchor="middle">10</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Find Letters</text>
            </g>

            <!-- LEVEL 11 -->
            <g transform="translate(840, -40)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=11'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 11 else '#38bdf8' if unlocked_lvl == 11 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="13" font-weight="900" fill="#fff" text-anchor="middle">11</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Picture Book</text>
            </g>

            <!-- LEVEL 12 -->
            <g transform="translate(910, 30)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=12'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 12 else '#38bdf8' if unlocked_lvl == 12 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="13" font-weight="900" fill="#fff" text-anchor="middle">12</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Sentences</text>
            </g>

            <!-- LEVEL 13 -->
            <g transform="translate(980, -20)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=13'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 13 else '#38bdf8' if unlocked_lvl == 13 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="13" font-weight="900" fill="#fff" text-anchor="middle">13</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Count 2,5,10</text>
            </g>

            <!-- LEVEL 14 -->
            <g transform="translate(1040, -80)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=14'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 14 else '#38bdf8' if unlocked_lvl == 14 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="13" font-weight="900" fill="#fff" text-anchor="middle">14</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">My Address</text>
            </g>

            <!-- LEVEL 15 -->
            <g transform="translate(1100, -140)" style="cursor:pointer;" onclick="window.parent.location.href='?lvl=15'">
                <circle cx="28" cy="28" r="28" fill="{('#10b981' if unlocked_lvl > 15 else '#38bdf8' if unlocked_lvl == 15 else '#94a3b8')}" stroke="#fff" stroke-width="4"/>
                <text x="28" y="34" font-family="'Fredoka', sans-serif" font-size="13" font-weight="900" fill="#fff" text-anchor="middle">15</text>
                <text x="28" y="68" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#0f172a" text-anchor="middle">Spell Name</text>
            </g>

            <g transform="translate(1160, -180)">
                <polygon points="60,10 5,60 115,60" fill="#991b1b"/>
                <rect x="15" y="60" width="90" height="80" fill="#f8fafc" stroke="#475569" stroke-width="3"/>
                <rect x="45" y="95" width="30" height="45" rx="4" fill="#78350f"/>
                <circle cx="60" cy="82" r="20" fill="#14b8a6" stroke="#ffffff" stroke-width="3"/>
                <polygon points="53,72 53,92 70,82" fill="#ffffff"/>
            </g>
        </svg>

        <!-- Companion Animals tucked neatly at the bottom inside the blue border -->
        <div style="display:flex; justify-content:center; gap:40px; align-items:flex-end; margin-top:5px;">
            <div style="font-size:2.2rem;">🐘</div>
            <div style="font-size:2.2rem;">🦊</div>
            <div style="font-size:2rem;">🦜</div>
            <div style="font-size:2.2rem;">🦭</div>
        </div>
    </div>
    """
    components.html(road_map_html, height=480)

    # Check if a map node was clicked via URL parameters
    params = st.query_params
    if "lvl" in params:
        clicked_lvl = int(params["lvl"][0])
        if clicked_lvl <= unlocked_lvl:
            target_id = CURRICULUM_LEVELS[clicked_lvl - 1]["id"]
            st.session_state.active_level_id = target_id
            st.query_params.clear()
            st.session_state.screen = "station_play"
            st.rerun()
        else:
            speak(f"Level {clicked_lvl} is locked! Complete previous levels first!")
            st.query_params.clear()
            st.warning(f"🔒 Level {clicked_lvl} is locked!")

    # DISPLAY ALL 15 LEVELS IN A BEAUTIFUL 3-COLUMN GRID BELOW THE MAP
    st.markdown("### 🚀 Or Select Your Level Below:", unsafe_allow_html=True)
    
    cols_grid = st.columns(3)
    for idx, lvl_info in enumerate(CURRICULUM_LEVELS):
        lvl_num = idx + 1
        is_unlocked = lvl_num <= unlocked_lvl
        col_target = cols_grid[idx % 3]
        
        with col_target:
            if is_unlocked:
                if st.button(f"🌟 Play {lvl_info['name']}", key=f"road_{lvl_info['id']}", use_container_width=True):
                    st.session_state.active_level_id = lvl_info["id"]
                    st.session_state.screen = "station_play"
                    st.rerun()
            else:
                if st.button(f"🔒 {lvl_info['name']} (Locked)", key=f"lock_{lvl_info['id']}", use_container_width=True):
                    speak("This level is locked! Complete previous levels first.")
                    st.warning(f"🔒 **{lvl_info['name']} is Locked:** Complete previous levels to unlock!")

# =========================================================
# SCREEN 4: INDIVIDUAL LEVEL PLAY ARENA (MASTERY ENGINE)
# =========================================================
elif st.session_state.screen == "station_play":
    user = st.session_state.active_user
    if user not in st.session_state.profiles:
        st.session_state.screen = "profile_select"
        st.rerun()
        
    pdata = st.session_state.profiles[user]
    lvl_id = st.session_state.active_level_id
    
    current_lvl_info = next((l for l in CURRICULUM_LEVELS if l["id"] == lvl_id), CURRICULUM_LEVELS[0])
    
    if "level_progress" not in pdata:
        pdata["level_progress"] = {}
    current_step = pdata["level_progress"].get(lvl_id, 0)

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

    st.markdown(f"<h2 style='color:#0369a1; text-align:center;'>{current_lvl_info['name']} (Question {min(current_step + 1, 3)} of 3)</h2>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # LEVEL 1: LIST 1 SIGHT WORDS
    # ---------------------------------------------------------
    if lvl_id == "lvl_1":
        questions = [
            {"q": "Which word says 'the'?", "correct": "the", "opts": ["the", "at", "it"], "hint": "Starts with T!"},
            {"q": "Which word says 'and'?", "correct": "and", "opts": ["dog", "and", "run"], "hint": "Starts with A!"},
            {"q": "Which word says 'you'?", "correct": "you", "opts": ["see", "cat", "you"], "hint": "Starts with Y!"}
        ]
        
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l1_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 1 Completed! Level 2 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_2"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 2: LIST 2 SIGHT WORDS
    # ---------------------------------------------------------
    elif lvl_id == "lvl_2":
        questions = [
            {"q": "Which word says 'look'?", "correct": "look", "opts": ["look", "dog", "big"], "hint": "Starts with L!"},
            {"q": "Which word says 'play'?", "correct": "play", "opts": ["run", "play", "red"], "hint": "Starts with P!"},
            {"q": "Which word says 'said'?", "correct": "said", "opts": ["said", "cat", "sun"], "hint": "Starts with S!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l2_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 2 Completed! Level 3 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_3"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 3: WRITE & TYPE ABCs (Sound & Order)
    # ---------------------------------------------------------
    elif lvl_id == "lvl_3":
        questions = [
            {"q": "What letter comes right after A?", "correct": "B", "opts": ["B", "C", "D"], "hint": "A, B, C!"},
            {"q": "What sound does the letter 'S' make?", "correct": "/s/ snake sound", "opts": ["/s/ snake sound", "/m/ monkey sound", "/b/ bear sound"], "hint": "S says ssss!"},
            {"q": "What letter comes right before Z?", "correct": "Y", "opts": ["X", "Y", "W"], "hint": "X, Y, Z!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l3_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 3 Completed! Level 4 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_4"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 4: COUNT TO 100 & WHAT COMES NEXT
    # ---------------------------------------------------------
    elif lvl_id == "lvl_4":
        questions = [
            {"q": "What number comes after 9?", "correct": "10", "opts": ["8", "10", "11"], "hint": "9, 10!"},
            {"q": "What number comes after 19?", "correct": "20", "opts": ["18", "20", "21"], "hint": "19, 20!"},
            {"q": "What number comes after 49?", "correct": "50", "opts": ["48", "50", "60"], "hint": "49, 50!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l4_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 4 Completed! Level 5 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_5"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 5: RHYMING WORDS
    # ---------------------------------------------------------
    elif lvl_id == "lvl_5":
        questions = [
            {"q": "What word rhymes with 'cat'?", "correct": "hat", "opts": ["dog", "hat", "sun"], "hint": "Listen to the ending: -at!"},
            {"q": "What word rhymes with 'pig'?", "correct": "wig", "opts": ["car", "wig", "hop"], "hint": "Listen to the ending: -ig!"},
            {"q": "What word rhymes with 'sun'?", "correct": "run", "opts": ["run", "cup", "pen"], "hint": "Listen to the ending: -un!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l5_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 5 Completed! Level 6 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_6"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 6: SYLLABLES
    # ---------------------------------------------------------
    elif lvl_id == "lvl_6":
        questions = [
            {"q": "How many syllables in 'cat'? (Clap it out: cat)", "correct": "1", "opts": ["1", "2", "3"], "hint": "Cat is 1 clap!"},
            {"q": "How many syllables in 'apple'? (Clap it out: ap-ple)", "correct": "2", "opts": ["1", "2", "3"], "hint": "Ap-ple is 2 claps!"},
            {"q": "How many syllables in 'elephant'? (Clap it out: el-e-phant)", "correct": "3", "opts": ["1", "2", "3"], "hint": "El-e-phant is 3 claps!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l6_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 6 Completed! Level 7 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_7"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 7: ADDITION UP TO 10
    # ---------------------------------------------------------
    elif lvl_id == "lvl_7":
        questions = [
            {"q": "What is 3 + 2?", "correct": "5", "opts": ["4", "5", "6"], "hint": "Count 3, then add 2 more!"},
            {"q": "What is 4 + 4?", "correct": "8", "opts": ["7", "8", "9"], "hint": "Count all together!"},
            {"q": "What is 5 + 5?", "correct": "10", "opts": ["9", "10", "11"], "hint": "Two hands of fingers!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l7_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 7 Completed! Level 8 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_8"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 8: SUBTRACTION UP TO 10
    # ---------------------------------------------------------
    elif lvl_id == "lvl_8":
        questions = [
            {"q": "What is 5 - 2?", "correct": "3", "opts": ["2", "3", "4"], "hint": "Take away 2 from 5!"},
            {"q": "What is 7 - 3?", "correct": "4", "opts": ["3", "4", "5"], "hint": "Count backward 3 from 7!"},
            {"q": "What is 10 - 5?", "correct": "5", "opts": ["4", "5", "6"], "hint": "Half of 10!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l8_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 8 Completed! Level 9 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_9"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 9: UPPER & LOWERCASE MATCH
    # ---------------------------------------------------------
    elif lvl_id == "lvl_9":
        questions = [
            {"q": "What is the lowercase partner for uppercase 'A'?", "correct": "a", "opts": ["a", "b", "c"], "hint": "Round circle with a tail!"},
            {"q": "What is the lowercase partner for uppercase 'B'?", "correct": "b", "opts": ["d", "b", "p"], "hint": "Straight line with a belly!"},
            {"q": "What is the lowercase partner for uppercase 'M'?", "correct": "m", "opts": ["n", "m", "w"], "hint": "Two humps!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l9_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 9 Completed! Level 10 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_10"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 10: FIND LETTERS IN ABCs
    # ---------------------------------------------------------
    elif lvl_id == "lvl_10":
        questions = [
            {"q": "Which letter comes first in the alphabet?", "correct": "A", "opts": ["A", "Z", "M"], "hint": "Starts with the very beginning!"},
            {"q": "Find the letter 'K' in the alphabet.", "correct": "K", "opts": ["J", "K", "L"], "hint": "Between J and L!"},
            {"q": "Which letter comes last in the alphabet?", "correct": "Z", "opts": ["A", "T", "Z"], "hint": "The very end!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l10_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 10 Completed! Level 11 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_11"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 11: READING PICTURE WORD BOOK
    # ---------------------------------------------------------
    elif lvl_id == "lvl_11":
        questions = [
            {"q": "Read: 'I see the cat.' Which word is a sight word?", "correct": "the", "opts": ["cat", "the", "see"], "hint": "T-H-E!"},
            {"q": "Read: 'Look at the big dog.' Which word is a sight word?", "correct": "look", "opts": ["dog", "big", "look"], "hint": "L-O-O-K!"},
            {"q": "Read: 'Play with me.' Which word is a sight word?", "correct": "play", "opts": ["play", "me", "with"], "hint": "P-L-A-Y!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l11_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 11 Completed! Level 12 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_12"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 12: WRITE A SENTENCE
    # ---------------------------------------------------------
    elif lvl_id == "lvl_12":
        questions = [
            {"q": "What goes at the very end of a sentence?", "correct": "Period (.)", "opts": ["Comma", "Period (.)", "Question mark"], "hint": "A dot!"},
            {"q": "What should the first letter of a sentence be?", "correct": "Capital letter", "opts": ["Small letter", "Capital letter", "Any letter"], "hint": "Uppercase!"},
            {"q": "What needs to be between words in a sentence?", "correct": "Finger spaces", "opts": ["Spaces", "Glue", "Nothing"], "hint": "Keep them apart!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l12_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 12 Completed! Level 13 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_13"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 13: COUNT BY 2s, 5s & 10s
    # ---------------------------------------------------------
    elif lvl_id == "lvl_13":
        questions = [
            {"q": "Count by 2s: 2, 4, 6, ... What's next?", "correct": "8", "opts": ["7", "8", "9"], "hint": "Add 2!"},
            {"q": "Count by 5s: 5, 10, 15, ... What's next?", "correct": "20", "opts": ["18", "20", "25"], "hint": "Add 5!"},
            {"q": "Count by 10s: 10, 20, 30, ... What's next?", "correct": "40", "opts": ["35", "40", "50"], "hint": "Add 10!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l13_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 13 Completed! Level 14 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_14"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 14: PERSONAL LOCATION
    # ---------------------------------------------------------
    elif lvl_id == "lvl_14":
        questions = [
            {"q": "What city do you live in?", "correct": "Covington", "opts": ["Atlanta", "Covington", "Savannah"], "hint": "Covington, GA!"},
            {"q": "What street do you live on?", "correct": "210 Belmont Circle", "opts": ["123 Main St", "210 Belmont Circle", "500 Peachtree Rd"], "hint": "210 Belmont Circle!"},
            {"q": "What state do you live in?", "correct": "Georgia (GA)", "opts": ["Florida", "Georgia (GA)", "Texas"], "hint": "The Peach State!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l14_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Level 14 Completed! Level 15 Unlocked!")
            if st.button("Next Level"):
                st.session_state.active_level_id = "lvl_15"
                st.rerun()

    # ---------------------------------------------------------
    # LEVEL 15: SPELL FULL NAME
    # ---------------------------------------------------------
    elif lvl_id == "lvl_15":
        questions = [
            {"q": "What is your first name?", "correct": "Gracyn", "opts": ["Gracyn", "Alex", "Taylor"], "hint": "Gracyn!"},
            {"q": "What is your middle name / last name initial?", "correct": "Brown", "opts": ["Smith", "Brown", "Johnson"], "hint": "Brown!"},
            {"q": "Are you a Kindergarten Star?", "correct": "Yes!", "opts": ["No", "Yes!", "Maybe"], "hint": "Always yes!"}
        ]
        if current_step < len(questions):
            q = questions[current_step]
            speak(q["q"])
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for i, opt in enumerate(q["opts"]):
                with [c1, c2, c3][i]:
                    if st.button(f"👉 {opt}", key=f"l15_{current_step}_{opt}", use_container_width=True):
                        if opt == q["correct"]:
                            record_progress(lvl_id, True)
                            st.balloons()
                            speak("Correct!")
                            st.rerun()
                        else:
                            speak(f"Hint: {q['hint']}")
                            st.warning(f"💡 Hint: {q['hint']}")
        else:
            st.success("🎉 Congratulations! You have fully completed all 15 Levels of the Kindergarten Road Map!")
            if st.button("🗺️ Return to Road Map"):
                st.session_state.screen = "adventure_trail"
                st.rerun()
