import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime

st.set_page_config(
    page_title="Adventure Learning Academy",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 1. VECTOR GRAPHICS & REFERENCE MAP ENGINE
# =========================================================

def render_avatar(skin="#8d5524", hair_style="puffs", hair_color="#1a1110", glasses="gold_round", shirt="#ec4899", accessory="crown", size=60):
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
            <circle cx="100" cy="100" r="95" fill="url(#glow_{size})" stroke="#38bdf8" stroke-width="5"/>
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
            "unlocked_level": 3,
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
            "daily_log": []
        }
    }

if "active_user" not in st.session_state:
    st.session_state.active_user = "Gracyn"

if "screen" not in st.session_state:
    st.session_state.screen = "profile_select"

if "active_activity" not in st.session_state:
    st.session_state.active_activity = "sight_words"

def record_event(activity, is_correct, detail, level_num):
    user = st.session_state.active_user
    prof = st.session_state.profiles[user]
    if is_correct:
        prof["stars"] += 1
        prof["streak"] += 1
        if level_num >= prof["unlocked_level"] and prof["unlocked_level"] < 8:
            prof["unlocked_level"] = level_num + 1
    prof["daily_log"].append({
        "time": datetime.now().strftime("%I:%M:%S %p"),
        "activity": activity,
        "detail": detail,
        "result": "Passed (+1 Star)" if is_correct else "Gentle Hint Used"
    })

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
                speak(f"Welcome back {name}! Follow your winding learning path to play!")
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
# SCREEN 3: KHAN ACADEMY KIDS REFERENCE MAP & PATHWAY
# =========================================================
elif st.session_state.screen == "adventure_trail":
    user = st.session_state.active_user
    pdata = st.session_state.profiles[user]
    b = pdata["buddy"]
    unlocked_lvl = pdata.get("unlocked_level", 1)

    # Top Header matching reference image
    col_lib, col_title, col_prof = st.columns([1, 3, 1])
    with col_lib:
        if st.button("📚 Library"):
            st.session_state.screen = "hub"
            st.rerun()
    with col_title:
        st.markdown("<h2 style='text-align:center; color:#0f172a; margin:0;'>💚 Khan Academy Kids</h2>", unsafe_allow_html=True)
    with col_prof:
        avatar_html = render_avatar(skin=b['skin'], hair_style=b['hair_style'], hair_color=b['hair_color'], glasses=b['glasses'], shirt=b['shirt'], accessory=b['accessory'], size=50)
        components.html(avatar_html, height=60)
        if st.button("Switch Profile", key="switch_p"):
            st.session_state.screen = "profile_select"
            st.rerun()

    speak(f"Welcome to your adventure trail {user}! Follow the winding path and tap the house play button or any unlocked station to begin!")

    # STATION DEFINITIONS (ALL 8 LEVELS)
    trail_stations = [
        {"level": 1, "id": "sight_words", "title": "Sight Words", "icon": "📖"},
        {"level": 2, "id": "book_parts", "title": "Book Parts", "icon": "📚"},
        {"level": 3, "id": "numbers", "title": "Numbers", "icon": "🕵️"},
        {"level": 4, "id": "spelling", "title": "Word Family", "icon": "🔤"},
        {"level": 5, "id": "ispy", "title": "Letter I-Spy", "icon": "🔍"},
        {"level": 6, "id": "seasons", "title": "Seasons", "icon": "🍁"},
        {"level": 7, "id": "math", "title": "Cool Math", "icon": "➕"},
        {"level": 8, "id": "parent_portal", "title": "Parent Portal", "icon": "📊"}
    ]

    # KHAN ACADEMY KIDS REFERENCE MAP CONTAINER (WINDING PATH, PREVIEW CARDS, LEARNING HOUSE, ANIMALS)
    map_container_html = f"""
    <div style="background:linear-gradient(180deg, #f0fdf4 0%, #e0f2fe 100%); border:5px solid #0284c7; border-radius:36px; padding:20px; box-shadow:0 16px 32px rgba(0,0,0,0.12); position:relative; overflow:hidden;">
        <!-- SVG Winding Path and Previews matching reference -->
        <svg width="100%" height="240" viewBox="0 0 900 240" xmlns="http://www.w3.org/2000/svg">
            <!-- Winding Path Road -->
            <path d="M 40 160 Q 180 60 320 150 Q 480 240 620 110" fill="none" stroke="#64748b" stroke-width="16" stroke-linecap="round" opacity="0.6"/>
            
            <!-- Milestone Preview Card 1 -->
            <g transform="translate(60, 110)">
                <rect x="0" y="0" width="110" height="70" rx="12" fill="#ffffff" stroke="#0284c7" stroke-width="4"/>
                <text x="55" y="42" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#0369a1" text-anchor="middle">📖 Level 1</text>
            </g>

            <!-- Milestone Preview Card 2 -->
            <g transform="translate(230, 85)">
                <rect x="0" y="0" width="110" height="70" rx="12" fill="#ffffff" stroke="#10b981" stroke-width="4"/>
                <text x="55" y="42" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#047857" text-anchor="middle">📚 Level 2</text>
            </g>

            <!-- Milestone Preview Card 3 -->
            <g transform="translate(410, 140)">
                <rect x="0" y="0" width="110" height="70" rx="12" fill="#ffffff" stroke="#f59e0b" stroke-width="4"/>
                <text x="55" y="42" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#b45309" text-anchor="middle">🕵️ Level 3</text>
            </g>

            <!-- Learning House on the Right with Giant Play Button -->
            <g transform="translate(640, 15)">
                <!-- Roof -->
                <polygon points="100,10 20,80 180,80" fill="#991b1b"/>
                <!-- House Body -->
                <rect x="35" y="80" width="130" height="110" fill="#f8fafc" stroke="#475569" stroke-width="4"/>
                <rect x="80" y="125" width="40" height="65" rx="6" fill="#78350f"/>
                <!-- Giant Play Button -->
                <circle cx="100" cy="115" r="32" fill="#14b8a6" stroke="#ffffff" stroke-width="4"/>
                <polygon points="90,100 90,130 118,115" fill="#ffffff"/>
            </g>
        </svg>

        <!-- Companion Animals along the bottom -->
        <div style="display:flex; justify-content:center; gap:35px; align-items:flex-end; margin-top:5px;">
            <div style="font-size:3rem;">🐘</div>
            <div style="font-size:3rem;">🦊</div>
            <div style="font-size:2.6rem;">🦜</div>
            <div style="font-size:3rem;">🦭</div>
        </div>
    </div>
    """
    components.html(map_container_html, height=330)

    st.markdown("### 🎮 Tap an Unlocked Level to Play:")
    cols_trail = st.columns(4)

    for idx, node in enumerate(trail_stations):
        lvl = node["level"]
        is_unlocked = lvl <= unlocked_lvl
        with cols_trail[idx % 4]:
            if is_unlocked:
                if st.button(f"{node['icon']} Level {lvl}: {node['title']}", key=f"trail_btn_{node['id']}", use_container_width=True):
                    st.session_state.active_activity = node['id']
                    st.session_state.current_level_num = lvl
                    st.session_state.screen = "station_play"
                    st.rerun()
            else:
                if st.button(f"🔒 Level {lvl} (Locked)", key=f"trail_lock_{node['id']}", use_container_width=True):
                    speak(f"Level {lvl} is locked! Complete previous levels first!")
                    st.warning(f"🔒 **Level {lvl} Locked**")

# =========================================================
# SCREEN 4: INDIVIDUAL STATION PLAY ARENA
# =========================================================
elif st.session_state.screen == "station_play":
    user = st.session_state.active_user
    pdata = st.session_state.profiles[user]
    act = st.session_state.active_activity
    lvl_num = st.session_state.get("current_level_num", 1)

    # Top Navigation Bar
    b1, b2, b3 = st.columns([1, 1, 1])
    with b1:
        if st.button("🗺️ Back to Trail Map"):
            st.session_state.screen = "adventure_trail"
            st.rerun()
    with b2:
        if st.button("🏠 Switch Profile"):
            st.session_state.screen = "profile_select"
            st.rerun()
    with b3:
        st.markdown(f"<div class='stat-chip' style='text-align:center;'>⭐ {pdata['stars']} Stars</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # 1. SIGHT WORDS
    if act == "sight_words":
        words_pool = ["THE", "AND", "YOU", "SEE", "CAN", "WAS"]
        if "sw_current" not in st.session_state: st.session_state.sw_current = "THE"
        speak(f"Read this word out loud, then trace it: {st.session_state.sw_current}")

        st.markdown(f"""
        <div class="game-card">
            <h3 style="color:#ef4444; font-size:1.6rem; margin:0;">SIGHT WORD EXPLORER (Level 1)</h3>
            <div style="font-size:5.5rem; font-weight:900; color:#dc2626; letter-spacing:8px; margin: 10px 0;">
                {st.session_state.sw_current}
            </div>
            <p style="font-size:1.2rem; font-weight:800; color:#64748b;">Read the word, then trace it below with your finger!</p>
        </div>
        """, unsafe_allow_html=True)

        col_pad, col_check = st.columns([2, 1])
        with col_pad:
            trace_html = """
            <div style="background:#f8fafc; border:4px dashed #0284c7; border-radius:24px; padding:10px; text-align:center;">
                <canvas id="c" width="460" height="170" style="background:#ffffff; border-radius:18px; touch-action:none; cursor:crosshair; border:2px solid #cbd5e1;"></canvas>
                <div style="margin-top:8px;">
                    <button onclick="c.getContext('2d').clearRect(0,0,c.width,c.height)" style="background:#ef4444; color:#fff; font-size:1.1rem; font-weight:800; border:none; border-radius:14px; padding:8px 20px; cursor:pointer;">Clear Writing</button>
                </div>
            </div>
            <script>
                const c = document.getElementById('c');
                const ctx = c.getContext('2d');
                let d = false;
                function gp(e){ const r=c.getBoundingClientRect(); return {x:(e.touches?e.touches[0].clientX:e.clientX)-r.left, y:(e.touches?e.touches[0].clientY:e.clientY)-r.top}; }
                c.addEventListener('mousedown', (e)=>{ d=true; const p=gp(e); ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineWidth=9; ctx.lineCap='round'; ctx.strokeStyle='#ec4899'; });
                c.addEventListener('mousemove', (e)=>{ if(!d)return; const p=gp(e); ctx.lineTo(p.x,p.y); ctx.stroke(); });
                window.addEventListener('mouseup', ()=>d=false);
                c.addEventListener('touchstart', (e)=>{ e.preventDefault(); d=true; const p=gp(e); ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineWidth=9; ctx.lineCap='round'; ctx.strokeStyle='#ec4899'; }, {passive:false});
                c.addEventListener('touchmove', (e)=>{ e.preventDefault(); if(!d)return; const p=gp(e); ctx.lineTo(p.x,p.y); ctx.stroke(); }, {passive:false});
                window.addEventListener('touchend', ()=>d=false);
            </script>
            """
            components.html(trace_html, height=250)

        with col_check:
            if st.button("I Read It! (+1 Star & Unlock Level 2)", use_container_width=True):
                st.balloons()
                speak(f"Awesome reading! Level 2 is now unlocked!")
                record_event("Sight Words", True, f"Mastered {st.session_state.sw_current}", level_num=1)
                st.session_state.sw_current = random.choice([w for w in words_pool if w != st.session_state.sw_current])
                st.rerun()
            if st.button("Next Word", use_container_width=True):
                st.session_state.sw_current = random.choice([w for w in words_pool if w != st.session_state.sw_current])
                st.rerun()

    # 2. BOOK PARTS
    elif act == "book_parts":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#1d4ed8; font-size:1.8rem; margin:0;">INTERACTIVE BOOK DETECTIVE (Level 2)</h3>
            <p style="color:#475569; font-size:1.2rem; font-weight:700;">Look at the book graphic and identify the highlighted part!</p>
        </div>
        """, unsafe_allow_html=True)
        b_img, b_quiz = st.columns([1.2, 1.4])
        with b_img:
            render_book_diagram(part="spine")
        with b_quiz:
            speak("What is the side edge called that holds all the pages together like your backbone?")
            st.markdown("#### What is the side edge called that holds all the pages together?")
            p1, p2 = st.columns(2)
            if p1.button("The Spine", use_container_width=True):
                st.balloons()
                speak("Yes! The spine holds the pages together and unlocks Level 3!")
                record_event("Parts of a Book", True, "Identified Spine", level_num=2)
                st.success("Correct! Level 3 Unlocked!")
            if p2.button("Front Cover", use_container_width=True):
                speak("Almost! The front cover is on the front. Look at the side edge!")
                record_event("Parts of a Book", False, "Guessed Cover", level_num=2)
                st.info("Hint: The spine is the backbone on the side edge!")

    # 3. NUMBERS
    elif act == "numbers":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#b45309; font-size:1.8rem; margin:0;">CANDY SHOP NUMBER DETECTIVE (Level 3)</h3>
            <p style="color:#475569; font-size:1.2rem; font-weight:700;">Count the jellybeans in each jar! Which card shows exactly 18?</p>
        </div>
        """, unsafe_allow_html=True)
        j1, j2 = st.columns(2)
        with j1:
            st.markdown("""
            <div style="background:#ffffff; border:4px solid #38bdf8; border-radius:26px; padding:12px; text-align:center;">
                <h4 style="color:#0369a1; font-size:1.3rem; margin:0 0 6px 0;">Jar 1 (10) + Jar 2 (8)</h4>
            </div>
            """, unsafe_allow_html=True)
            render_candy_jars(10, 8)
            if st.button("This shows 18 Beans!", key="j_c", use_container_width=True):
                st.balloons()
                speak("Yes! Ten plus eight makes 18! Level 4 unlocked!")
                record_event("Number Detective", True, "10+8=18", level_num=3)
                st.success("Correct! Level 4 Unlocked!")
        with j2:
            st.markdown("""
            <div style="background:#ffffff; border:4px solid #f87171; border-radius:26px; padding:12px; text-align:center;">
                <h4 style="color:#dc2626; font-size:1.3rem; margin:0 0 6px 0;">Jar 1 (10) + Jar 2 (4)</h4>
            </div>
            """, unsafe_allow_html=True)
            render_candy_jars(10, 4)
            if st.button("Is this 18?", key="j_w", use_container_width=True):
                speak("Count carefully! Ten plus four is 14, not 18!")
                record_event("Number Detective", False, "Guessed 14", level_num=3)
                st.info("Hint: 10 plus 4 is 14. Look for 18!")

    # 4. SPELLING
    elif act == "spelling":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#7e22ce; font-size:1.8rem; margin:0;">WORD FAMILY BUILDER: -AT FAMILY (Level 4)</h3>
            <p style="color:#475569; font-size:1.2rem; font-weight:700;">Tap a letter to blend and spell rhyming words!</p>
        </div>
        """, unsafe_allow_html=True)
        speak("Tap a letter to spell a new rhyming word!")
        s1, s2, s3, s4 = st.columns(4)
        if s1.button("C + AT"):
            st.balloons(); speak("C plus A T spells CAT! Level 5 unlocked!"); record_event("Word Family", True, "CAT", level_num=4); st.success("CAT! Level 5 Unlocked!")
        if s2.button("B + AT"):
            st.balloons(); speak("B plus A T spells BAT! Level 5 unlocked!"); record_event("Word Family", True, "BAT", level_num=4); st.success("BAT! Level 5 Unlocked!")
        if s3.button("H + AT"):
            st.balloons(); speak("H plus A T spells HAT! Level 5 unlocked!"); record_event("Word Family", True, "HAT", level_num=4); st.success("HAT! Level 5 Unlocked!")
        if s4.button("R + AT"):
            st.balloons(); speak("R plus A T spells RAT! Level 5 unlocked!"); record_event("Word Family", True, "RAT", level_num=4); st.success("RAT! Level 5 Unlocked!")

    # 5. I-SPY
    elif act == "ispy":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#db2777; font-size:1.8rem; margin:0;">LETTER I-SPY SAFARI (Level 5)</h3>
            <p style="color:#475569; font-size:1.2rem; font-weight:700;">Pop all the bubbles matching the letter: <strong>A</strong>!</p>
        </div>
        """, unsafe_allow_html=True)
        speak("I spy the letter A! Pop all the bubbles that show the letter A!")
        b_grid = ["A", "B", "A", "C", "D", "A", "E", "A"]
        cols = st.columns(4)
        for idx, letter in enumerate(b_grid):
            with cols[idx % 4]:
                if st.button(f"Bubble {letter}", key=f"ispy_{idx}"):
                    if letter == "A":
                        st.balloons(); speak("Pop! You found letter A! Level 6 unlocked!"); record_event("Letter I-Spy", True, "Found A", level_num=5); st.success("Popped A! Level 6 Unlocked!")
                    else:
                        speak(f"Oops! That is the letter {letter}. Look for letter A!")
                        record_event("Letter I-Spy", False, f"Tapped {letter}", level_num=5)

    # 6. SEASONS
    elif act == "seasons":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#15803d; font-size:1.8rem; margin:0;">WEATHER-CASTER QUEST (Level 6)</h3>
            <p style="color:#475569; font-size:1.2rem; font-weight:700;">Leaves turn orange and red, pumpkins grow, and we wear cozy sweaters! What season is it?</p>
        </div>
        """, unsafe_allow_html=True)
        speak("Leaves turn orange and red, pumpkins grow, and we wear cozy sweaters! What season is it?")
        sc1, sc2 = st.columns(2)
        if sc1.button("Fall / Autumn", use_container_width=True):
            st.balloons(); speak("Correct! That happens during Fall and Autumn! Level 7 unlocked!"); record_event("Seasons", True, "Fall", level_num=6); st.success("Correct! Level 7 Unlocked!")
        if sc2.button("Summer", use_container_width=True):
            speak("Think about the leaves changing color! Summer is hot and sunny!")
            record_event("Seasons", False, "Guessed Summer", level_num=6)
            st.info("Hint: Leaves fall from trees during Fall / Autumn!")

    # 7. MATH
    elif act == "math":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#7e22ce; font-size:1.8rem; margin:0;">COOL MATH APPLES (Level 7)</h3>
            <div style="font-size:3.5rem; font-weight:900; color:#7e22ce; margin:8px 0;">3 + 2 = ?</div>
            <p style="color:#475569; font-size:1.2rem; font-weight:700;">Count the apples to solve the problem!</p>
        </div>
        """, unsafe_allow_html=True)
        speak("What is 3 plus 2? Count the apples to find the answer!")
        m1, m2, m3 = st.columns(3)
        if m1.button("4", use_container_width=True):
            speak("Count carefully! 3 apples and 2 more!"); record_event("Cool Math", False, "Guessed 4", level_num=7)
        if m2.button("5", use_container_width=True):
            st.balloons(); speak("Yes! 3 plus 2 equals 5! Level 8 unlocked!"); record_event("Cool Math", True, "3+2=5", level_num=7); st.success("Correct! Level 8 Unlocked!")
        if m3.button("6", use_container_width=True):
            speak("Count the apples one by one!"); record_event("Cool Math", False, "Guessed 6", level_num=7)

    # 8. PARENT PORTAL
    elif act == "parent_portal":
        st.markdown(f"""
        <div class="game-card">
            <h3 style="color:#0f172a; font-size:1.8rem; margin:0;">PRACTICE & TELEMETRY LOG: {user}</h3>
            <p style="color:#475569; font-size:1.15rem; font-weight:700;">Track real-time responses and progress across all learning domains.</p>
        </div>
        """, unsafe_allow_html=True)
        tot = len(pdata["daily_log"])
        corr = sum(1 for e in pdata["daily_log"] if "Passed" in e["result"])
        acc = int((corr / tot) * 100) if tot > 0 else 100
        
        m_a, m_b, m_c = st.columns(3)
        m_a.metric("Total Questions", tot)
        m_b.metric("Total Stars", pdata["stars"])
        m_c.metric("First-Try Accuracy", f"%{acc}")

        st.markdown("#### Detailed Activity Stream:")
        if pdata["daily_log"]:
            for item in reversed(pdata["daily_log"]):
                st.write(f"• **{item['time']}** — [{item['activity']}] {item['detail']}: **{item['result']}**")
        else:
            st.info("No activities logged yet for this profile.")
