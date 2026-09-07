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
# 1. VECTOR SVG GRAPHICS ENGINE
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
    components.html(raw_html, height=size + 10)

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
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        padding: 14px 26px !important;
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

    .hud-bar {
        background: #ffffff;
        border-radius: 26px;
        padding: 12px 24px;
        border: 4px solid #facc15;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .stat-chip {
        background: #fef08a;
        color: #854d0e;
        border-radius: 20px;
        padding: 6px 16px;
        font-weight: 800;
        font-size: 1.25rem;
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
# 3. PERSISTENT STUDENT PROFILES & STATE MANAGEMENT
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
            "unlocked_node": 1,
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
            "unlocked_node": 1,
            "daily_log": []
        }
    }

if "active_user" not in st.session_state:
    st.session_state.active_user = "Gracyn"

if "screen" not in st.session_state:
    st.session_state.screen = "profile_select"

if "active_activity" not in st.session_state:
    st.session_state.active_activity = "sight_words"

# Helper to record progress into the active profile
def record_event(activity, is_correct, detail):
    user = st.session_state.active_user
    prof = st.session_state.profiles[user]
    if is_correct:
        prof["stars"] += 1
        prof["streak"] += 1
        # Advance trail milestone node if they complete enough
        if prof["unlocked_node"] < 7:
            prof["unlocked_node"] += 1
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
            render_avatar(skin=b["skin"], hair_style=b["hair_style"], hair_color=b["hair_color"], glasses=b["glasses"], shirt=b["shirt"], accessory=b["accessory"], size=180)
            if st.button(f"Play as {name}", key=f"prof_{name}", use_container_width=True):
                st.session_state.active_user = name
                st.session_state.screen = "adventure_map"
                speak(f"Welcome back {name}! Let's continue your adventure!")
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
        render_avatar(skin=tb['skin'], hair_style=tb['hair_style'], hair_color=tb['hair_color'], glasses=tb['glasses'], shirt=tb['shirt'], accessory=tb['accessory'], size=230)
        new_profile_name = st.text_input("Enter Profile Name:", value="Superstar")
        if st.button("Save & Start Learning!", use_container_width=True):
            clean_name = new_profile_name.strip() if new_profile_name.strip() else "Learner"
            st.session_state.profiles[clean_name] = {
                "buddy": tb,
                "stars": 10,
                "streak": 1,
                "unlocked_node": 1,
                "daily_log": []
            }
            st.session_state.active_user = clean_name
            st.session_state.screen = "adventure_map"
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
# SCREEN 3: KHAN-KIDS STYLE ADVENTURE TRAIL MAP & PLAY STATIONS
# =========================================================
elif st.session_state.screen == "adventure_map":
    user = st.session_state.active_user
    pdata = st.session_state.profiles[user]
    b = pdata["buddy"]

    # Top HUD Bar with Home/Switch Profile button
    hud_l, hud_r = st.columns([3, 1])
    with hud_l:
        st.markdown(f"""
        <div class="hud-bar" style="margin-bottom:0;">
            <div style="display:flex; align-items:center; gap:10px;">
                <b style="font-size:1.35rem; color:#0f172a;">{user}'s Adventure Trail</b>
            </div>
            <div style="display:flex; gap:10px;">
                <div class="stat-chip">⭐ {pdata['stars']} Stars</div>
                <div class="stat-chip" style="background:#dcfce7; color:#166534; border-color:#86efac;">🔥 {pdata['streak']} Streak</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with hud_r:
        if st.button("🏠 Switch Profile", use_container_width=True):
            st.session_state.screen = "profile_select"
            st.rerun()

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # Adventure Trail Nodes (Khan Academy Kids style progression map)
    st.markdown("""
    <div style="background:rgba(255,255,255,0.7); border:3px solid #38bdf8; border-radius:24px; padding:12px; text-align:center; margin-bottom:14px;">
        <h3 style="color:#0369a1; margin:0; font-size:1.4rem;">🗺️ Tap any station along your learning path!</h3>
    </div>
    """, unsafe_allow_html=True)

    trail_nodes = [
        {"id": "sight_words", "title": "1. Sight Words Explorer", "icon": "📖", "desc": "Read & Trace"},
        {"id": "book_parts", "title": "2. Book Detective", "icon": "📚", "desc": "Parts of a Book"},
        {"id": "numbers", "title": "3. Number Detective", "icon": "🕵️", "desc": "Counting & Quantities"},
        {"id": "spelling", "title": "4. Word Family Lab", "icon": "🔤", "desc": "Onset-Rime Rhymes"},
        {"id": "ispy", "title": "5. Letter I-Spy Safari", "icon": "🔍", "desc": "Bubble Pop Phonics"},
        {"id": "seasons", "title": "6. Seasons Quest", "icon": "🍁", "desc": "Nature & Weather"},
        {"id": "math", "title": "7. Cool Math Apples", "icon": "➕", "desc": "Addition Sums"},
        {"id": "parent_portal", "title": "8. Parent Progress", "icon": "📊", "desc": "Telemetry & Logs"}
    ]

    cols_map = st.columns(4)
    for idx, node in enumerate(trail_nodes):
        with cols_map[idx % 4]:
            is_unlocked = (idx + 1) <= pdata["unlocked_node"]
            btn_label = f"{node['icon']} {node['title']}"
            if st.button(btn_label, key=f"node_{node['id']}", use_container_width=True):
                st.session_state.active_activity = node['id']
                st.rerun()

    st.markdown("---")

    # -------------------------------------------------------------
    # ACTIVE LEARNING STATION ROUTER
    # -------------------------------------------------------------
    act = st.session_state.active_activity

    if act == "sight_words":
        words_pool = ["THE", "AND", "YOU", "SEE", "CAN", "WAS"]
        if "sw_current" not in st.session_state: st.session_state.sw_current = "THE"
        speak(f"Read this word out loud, then trace it: {st.session_state.sw_current}")

        st.markdown(f"""
        <div class="game-card">
            <h3 style="color:#ef4444; font-size:1.6rem; margin:0;">SIGHT WORD EXPLORER</h3>
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
            if st.button("I Read It! (+1 Star)", use_container_width=True):
                st.balloons()
                speak(f"Awesome reading! You mastered {st.session_state.sw_current}!")
                record_event("Sight Words", True, f"Mastered {st.session_state.sw_current}")
                st.session_state.sw_current = random.choice([w for w in words_pool if w != st.session_state.sw_current])
                st.rerun()
            if st.button("Next Word", use_container_width=True):
                st.session_state.sw_current = random.choice([w for w in words_pool if w != st.session_state.sw_current])
                st.rerun()

    elif act == "book_parts":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#1d4ed8; font-size:1.8rem; margin:0;">INTERACTIVE BOOK DETECTIVE</h3>
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
                speak("Yes! The spine holds the pages together like your backbone!")
                record_event("Parts of a Book", True, "Identified Spine")
                st.success("Correct! The spine is the book's backbone.")
            if p2.button("Front Cover", use_container_width=True):
                speak("Almost! The front cover is on the front. Look at the side edge!")
                record_event("Parts of a Book", False, "Guessed Cover")
                st.info("Hint: The spine is the backbone on the side edge!")

    elif act == "numbers":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#b45309; font-size:1.8rem; margin:0;">CANDY SHOP NUMBER DETECTIVE</h3>
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
                speak("Yes! Ten red beans plus eight green beans makes 18!")
                record_event("Number Detective", True, "10+8=18")
                st.success("Correct! 10 + 8 = 18!")
        with j2:
            st.markdown("""
            <div style="background:#ffffff; border:4px solid #f87171; border-radius:26px; padding:12px; text-align:center;">
                <h4 style="color:#dc2626; font-size:1.3rem; margin:0 0 6px 0;">Jar 1 (10) + Jar 2 (4)</h4>
            </div>
            """, unsafe_allow_html=True)
            render_candy_jars(10, 4)
            if st.button("Is this 18?", key="j_w", use_container_width=True):
                speak("Count carefully! Ten plus four is 14, not 18!")
                record_event("Number Detective", False, "Guessed 14")
                st.info("Hint: 10 plus 4 is 14. Look for 18!")

    elif act == "spelling":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#7e22ce; font-size:1.8rem; margin:0;">WORD FAMILY BUILDER: -AT FAMILY</h3>
            <p style="color:#475569; font-size:1.2rem; font-weight:700;">Tap a letter to blend and spell rhyming words!</p>
        </div>
        """, unsafe_allow_html=True)
        speak("Tap a letter to spell a new rhyming word!")
        s1, s2, s3, s4 = st.columns(4)
        if s1.button("C + AT"):
            st.balloons(); speak("C plus A T spells CAT!"); record_event("Word Family", True, "CAT"); st.success("CAT! Great job!")
        if s2.button("B + AT"):
            st.balloons(); speak("B plus A T spells BAT!"); record_event("Word Family", True, "BAT"); st.success("BAT! Wonderful spelling!")
        if s3.button("H + AT"):
            st.balloons(); speak("H plus A T spells HAT!"); record_event("Word Family", True, "HAT"); st.success("HAT! You made a word!")
        if s4.button("R + AT"):
            st.balloons(); speak("R plus A T spells RAT!"); record_event("Word Family", True, "RAT"); st.success("RAT! Super rhyming!")

    elif act == "ispy":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#db2777; font-size:1.8rem; margin:0;">LETTER I-SPY SAFARI</h3>
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
                        st.balloons(); speak("Pop! You found letter A!"); record_event("Letter I-Spy", True, "Found A"); st.success("Popped A!")
                    else:
                        speak(f"Oops! That is the letter {letter}. Look for letter A!")
                        record_event("Letter I-Spy", False, f"Tapped {letter}")

    elif act == "seasons":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#15803d; font-size:1.8rem; margin:0;">WEATHER-CASTER QUEST</h3>
            <p style="color:#475569; font-size:1.2rem; font-weight:700;">Leaves turn orange and red, pumpkins grow, and we wear cozy sweaters! What season is it?</p>
        </div>
        """, unsafe_allow_html=True)
        speak("Leaves turn orange and red, pumpkins grow, and we wear cozy sweaters! What season is it?")
        sc1, sc2 = st.columns(2)
        if sc1.button("Fall / Autumn", use_container_width=True):
            st.balloons(); speak("Correct! That happens during Fall and Autumn!"); record_event("Seasons", True, "Fall"); st.success("Correct! Pumpkins and orange leaves happen in Fall!")
        if sc2.button("Summer", use_container_width=True):
            speak("Think about the leaves changing color! Summer is hot and sunny!")
            record_event("Seasons", False, "Guessed Summer")
            st.info("Hint: Leaves fall from trees during Fall / Autumn!")

    elif act == "math":
        st.markdown("""
        <div class="game-card">
            <h3 style="color:#7e22ce; font-size:1.8rem; margin:0;">COOL MATH APPLES</h3>
            <div style="font-size:3.5rem; font-weight:900; color:#7e22ce; margin:8px 0;">3 + 2 = ?</div>
            <p style="color:#475569; font-size:1.2rem; font-weight:700;">Count the apples to solve the problem!</p>
        </div>
        """, unsafe_allow_html=True)
        speak("What is 3 plus 2? Count the apples to find the answer!")
        m1, m2, m3 = st.columns(3)
        if m1.button("4", use_container_width=True):
            speak("Count carefully! 3 apples and 2 more!"); record_event("Cool Math", False, "Guessed 4")
        if m2.button("5", use_container_width=True):
            st.balloons(); speak("Yes! 3 plus 2 equals 5!"); record_event("Cool Math", True, "3+2=5"); st.success("Correct! 3 + 2 = 5!")
        if m3.button("6", use_container_width=True):
            speak("Count the apples one by one!"); record_event("Cool Math", False, "Guessed 6")

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
        m_c.metric("First-Try Accuracy", f"{acc}%")

        st.markdown("#### Detailed Activity Stream:")
        if pdata["daily_log"]:
            for item in reversed(pdata["daily_log"]):
                st.write(f"• **{item['time']}** — [{item['activity']}] {item['detail']}: **{item['result']}**")
        else:
            st.info("No activities logged yet for this profile.")
