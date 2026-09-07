import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime

st.set_page_config(
    page_title="Adventure Academy Kids",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 1. VECTOR SVG GRAPHICS ENGINE (NO EMOJIS)
# =========================================================

def get_avatar_svg(skin="#8d5524", hair_style="puffs", hair_color="#1a1110", glasses="gold_round", shirt="#3b82f6", accessory="none", size=180):
    """Renders a high-quality illustrated cartoon avatar using pure SVG."""
    
    # Hair paths
    hair_svg = ""
    if hair_style == "puffs":
        hair_svg = f"""
        <!-- Two Afro Puffs -->
        <circle cx="50" cy="55" r="28" fill="{hair_color}"/>
        <circle cx="150" cy="55" r="28" fill="{hair_color}"/>
        <path d="M 65 75 Q 100 45 135 75 Q 100 65 65 75 Z" fill="{hair_color}"/>
        """
    elif hair_style == "curly_bob":
        hair_svg = f"""
        <!-- Curly Bob -->
        <circle cx="65" cy="80" r="24" fill="{hair_color}"/>
        <circle cx="135" cy="80" r="24" fill="{hair_color}"/>
        <path d="M 60 70 Q 100 35 140 70 Q 100 55 60 70 Z" fill="{hair_color}"/>
        """
    elif hair_style == "short_fade":
        hair_svg = f"""
        <!-- Clean Fade -->
        <path d="M 65 80 Q 100 40 135 80 Q 100 60 65 80 Z" fill="{hair_color}"/>
        <rect x="68" y="70" width="64" height="15" rx="7" fill="{hair_color}"/>
        """
    elif hair_style == "ponytail":
        hair_svg = f"""
        <!-- High Ponytail with Bow -->
        <circle cx="100" cy="40" r="26" fill="{hair_color}"/>
        <path d="M 68 75 Q 100 45 132 75 Z" fill="{hair_color}"/>
        <ellipse cx="100" cy="55" rx="14" ry="6" fill="#ec4899"/>
        """

    # Glasses
    glasses_svg = ""
    if glasses == "gold_round":
        glasses_svg = """
        <!-- Fun Round Glasses -->
        <circle cx="82" cy="100" r="15" fill="none" stroke="#f59e0b" stroke-width="4"/>
        <circle cx="118" cy="100" r="15" fill="none" stroke="#f59e0b" stroke-width="4"/>
        <line x1="97" y1="100" x2="103" y2="100" stroke="#f59e0b" stroke-width="4"/>
        <line x1="67" y1="98" x2="60" y2="92" stroke="#f59e0b" stroke-width="3"/>
        <line x1="133" y1="98" x2="140" y2="92" stroke="#f59e0b" stroke-width="3"/>
        """
    elif glasses == "cool_shades":
        glasses_svg = """
        <!-- Star Sunglasses -->
        <polygon points="82,85 86,95 96,96 88,103 91,113 82,107 73,113 76,103 68,96 78,95" fill="#8b5cf6"/>
        <polygon points="118,85 122,95 132,96 124,103 127,113 118,107 109,113 112,103 104,96 114,95" fill="#8b5cf6"/>
        <line x1="94" y1="101" x2="106" y2="101" stroke="#6d28d9" stroke-width="4"/>
        """

    # Accessory
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

    svg_code = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="avatarGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="100%" stop-color="#dbeafe"/>
            </radialGradient>
        </defs>
        
        <!-- Background Bubble -->
        <circle cx="100" cy="100" r="95" fill="url(#avatarGlow)" stroke="#38bdf8" stroke-width="6"/>

        {acc_svg if accessory == "cape" else ""}

        <!-- Torso & Shirt -->
        <path d="M 60 185 C 60 145, 140 145, 140 185 Z" fill="{shirt}"/>
        <path d="M 85 145 Q 100 160 115 145 Z" fill="{skin}"/>

        <!-- Neck -->
        <rect x="91" y="132" width="18" height="18" rx="6" fill="{skin}"/>

        <!-- Head -->
        <ellipse cx="100" cy="100" rx="36" ry="42" fill="{skin}"/>

        <!-- Ears -->
        <circle cx="63" cy="102" r="9" fill="{skin}"/>
        <circle cx="137" cy="102" r="9" fill="{skin}"/>

        {hair_svg}

        <!-- Cartoon Eyes -->
        <ellipse cx="84" cy="98" rx="6" ry="8" fill="#ffffff"/>
        <circle cx="85" cy="98" r="4.5" fill="#0f172a"/>
        <circle cx="87" cy="95" r="1.5" fill="#ffffff"/>

        <ellipse cx="116" cy="98" rx="6" ry="8" fill="#ffffff"/>
        <circle cx="115" cy="98" r="4.5" fill="#0f172a"/>
        <circle cx="117" cy="95" r="1.5" fill="#ffffff"/>

        <!-- Cheerful Blush -->
        <ellipse cx="78" cy="109" rx="6" ry="3.5" fill="#f43f5e" opacity="0.35"/>
        <ellipse cx="122" cy="109" rx="6" ry="3.5" fill="#f43f5e" opacity="0.35"/>

        <!-- Happy Smile -->
        <path d="M 90 115 Q 100 128 110 115" fill="none" stroke="#78350f" stroke-width="3" stroke-linecap="round"/>

        {glasses_svg}
        {acc_svg if accessory != "cape" else ""}
    </svg>
    """
    return svg_code

# Vector Illustrations for Activities
def get_book_illustration(part="cover"):
    spine_highlight = 'stroke="#facc15" stroke-width="6"' if part == "spine" else 'stroke="#1e3a8a" stroke-width="2"'
    cover_highlight = 'stroke="#facc15" stroke-width="6"' if part == "cover" else 'stroke="#2563eb" stroke-width="2"'
    
    return f"""
    <svg width="260" height="200" viewBox="0 0 260 200" xmlns="http://www.w3.org/2000/svg">
        <rect x="25" y="25" width="210" height="150" rx="14" fill="#60a5fa" {cover_highlight}/>
        <!-- Book Spine -->
        <rect x="25" y="25" width="34" height="150" rx="6" fill="#1d4ed8" {spine_highlight}/>
        <line x1="36" y1="40" x2="36" y2="160" stroke="#93c5fd" stroke-width="3" stroke-dasharray="6,4"/>
        
        <!-- Book Cover Artwork -->
        <rect x="75" y="45" width="145" height="40" rx="8" fill="#ffffff"/>
        <text x="147" y="69" font-family="'Fredoka', sans-serif" font-size="14" font-weight="900" fill="#1e40af" text-anchor="middle">THE BRAVE PUPPY</text>
        
        <!-- Center Character on Book -->
        <circle cx="147" cy="115" r="22" fill="#fef08a"/>
        <ellipse cx="140" cy="112" rx="3" ry="4" fill="#0f172a"/>
        <ellipse cx="154" cy="112" rx="3" ry="4" fill="#0f172a"/>
        <ellipse cx="147" cy="120" rx="4" ry="2.5" fill="#78350f"/>
        
        <!-- Author Badge -->
        <rect x="85" y="146" width="125" height="18" rx="6" fill="#ffffffcc"/>
        <text x="147" y="159" font-family="'Fredoka', sans-serif" font-size="10" font-weight="800" fill="#334155" text-anchor="middle">By Raeven Brown</text>
    </svg>
    """

def get_candy_jar_svg(count=10, bean_color="#ef4444"):
    beans_svg = ""
    random.seed(42)
    for i in range(count):
        bx = 45 + (i % 4) * 20
        by = 135 - (i // 4) * 22
        beans_svg += f'<ellipse cx="{bx}" cy="{by}" rx="8" ry="6" fill="{bean_color}" stroke="#ffffff" stroke-width="1.5" transform="rotate({(i*25)%45}, {bx}, {by})"/>'
    
    return f"""
    <svg width="150" height="170" viewBox="0 0 150 170" xmlns="http://www.w3.org/2000/svg">
        <!-- Jar Lid -->
        <rect x="45" y="15" width="60" height="16" rx="5" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
        <rect x="52" y="5" width="46" height="12" rx="4" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
        <!-- Glass Jar -->
        <path d="M 40 32 Q 25 45 25 75 L 25 145 Q 25 160 40 160 L 110 160 Q 125 160 125 145 L 125 75 Q 125 45 110 32 Z" fill="#e0f2fe" opacity="0.85" stroke="#0284c7" stroke-width="4"/>
        <!-- Glass Shine -->
        <path d="M 35 60 L 35 140" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
        {beans_svg}
    </svg>
    """

# =========================================================
# 2. APPLICATION STYLING & WEBAUDIO (ZERO EMOJIS)
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700;800&family=Quicksand:wght@600;700;800&display=swap');

    .stApp {
        background: linear-gradient(180deg, #60a5fa 0%, #93c5fd 40%, #bbf7d0 100%) !important;
        font-family: 'Fredoka', 'Quicksand', cursive, sans-serif !important;
    }

    /* Chunky Tactile Arcade Buttons */
    .stButton > button {
        border-radius: 28px !important;
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        padding: 16px 28px !important;
        background: #ffffff !important;
        color: #0369a1 !important;
        border: 4px solid #38bdf8 !important;
        box-shadow: 0 9px 0 #0284c7, 0 14px 20px rgba(0,0,0,0.12) !important;
        transition: transform 0.08s ease !important;
    }
    .stButton > button:active {
        transform: translateY(7px) !important;
        box-shadow: 0 2px 0 #0284c7 !important;
    }

    /* Main Card Stage */
    .game-stage-card {
        background: #ffffff;
        border: 5px solid #38bdf8;
        border-radius: 36px;
        padding: 24px;
        box-shadow: 0 16px 36px rgba(0,0,0,0.12);
        margin-bottom: 20px;
        text-align: center;
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

    .badge-star {
        background: #fef08a;
        color: #854d0e;
        border-radius: 20px;
        padding: 8px 18px;
        font-weight: 800;
        font-size: 1.3rem;
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
            utter.pitch = 1.25;
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
# 3. GAME STATE MANAGEMENT
# =========================================================

if "screen" not in st.session_state:
    st.session_state.screen = "profile_select"

if "buddy_config" not in st.session_state:
    st.session_state.buddy_config = {
        "skin": "#8d5524",
        "hair_style": "puffs",
        "hair_color": "#1a1110",
        "glasses": "gold_round",
        "shirt": "#ec4899",
        "accessory": "crown"
    }

if "student_name" not in st.session_state:
    st.session_state.student_name = "Gracyn"

if "stars" not in st.session_state:
    st.session_state.stars = 14

if "streak" not in st.session_state:
    st.session_state.streak = 3

if "active_activity" not in st.session_state:
    st.session_state.active_activity = "sight_words"

if "show_hint" not in st.session_state:
    st.session_state.show_hint = False

# =========================================================
# SCREEN 1: PROFILE SELECTION (KHAN ACADEMY KIDS STYLE)
# =========================================================
if st.session_state.screen == "profile_select":
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px 0;">
        <h1 style="color:#0369a1; font-size:3.2rem; font-weight:900;">ADVENTURE LEARNING ACADEMY</h1>
        <p style="font-size:1.6rem; color:#1e293b; font-weight:800;">Who is playing today? Tap your character!</p>
    </div>
    """, unsafe_allow_html=True)
    speak("Who is playing today? Tap your character or create a new buddy!")

    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        st.markdown(f"""
        <div style="text-align:center;">
            {get_avatar_svg(
                skin=st.session_state.buddy_config['skin'],
                hair_style=st.session_state.buddy_config['hair_style'],
                hair_color=st.session_state.buddy_config['hair_color'],
                glasses=st.session_state.buddy_config['glasses'],
                shirt=st.session_state.buddy_config['shirt'],
                accessory=st.session_state.buddy_config['accessory'],
                size=200
            )}
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Play as {st.session_state.student_name}", use_container_width=True):
            st.session_state.screen = "adventure_map"
            st.rerun()

    with c2:
        st.markdown(f"""
        <div style="text-align:center;">
            {get_avatar_svg(skin="#e0ac69", hair_style="short_fade", hair_color="#271810", glasses="none", shirt="#3b82f6", accessory="cape", size=200)}
        </div>
        """, unsafe_allow_html=True)
        if st.button("Play as Jaxson", use_container_width=True):
            st.session_state.student_name = "Jaxson"
            st.session_state.screen = "adventure_map"
            st.rerun()

    with c3:
        st.markdown("""
        <div style="text-align:center;">
            <svg width="200" height="200" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="90" fill="#f8fafc" stroke="#94a3b8" stroke-width="6" stroke-dasharray="12,8"/>
                <line x1="100" y1="65" x2="100" y2="135" stroke="#0284c7" stroke-width="12" stroke-linecap="round"/>
                <line x1="65" y1="100" x2="135" y2="100" stroke="#0284c7" stroke-width="12" stroke-linecap="round"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        if st.button("New Buddy Studio", use_container_width=True):
            st.session_state.screen = "buddy_dressup"
            st.rerun()

# =========================================================
# SCREEN 2: TRUE INTERACTIVE BUDDY DRESS-UP STUDIO
# =========================================================
elif st.session_state.screen == "buddy_dressup":
    st.markdown("""
    <div class="game-stage-card" style="padding:16px;">
        <h2 style="color:#0369a1; font-size:2.4rem; margin:0;">BUDDY DRESS-UP STUDIO</h2>
        <p style="color:#475569; font-weight:700; font-size:1.2rem; margin:4px 0 0 0;">Customize your learning buddy! Change skin tones, hair styles, glasses, and clothes.</p>
    </div>
    """, unsafe_allow_html=True)
    speak("Welcome to the buddy studio! Tap the buttons to change hair, glasses, and clothes!")

    col_view, col_controls = st.columns([1.1, 1.4])

    with col_view:
        st.markdown(f"""
        <div style="background:#ffffff; border:5px solid #38bdf8; border-radius:36px; padding:24px; text-align:center; box-shadow:0 14px 28px rgba(0,0,0,0.1);">
            {get_avatar_svg(
                skin=st.session_state.buddy_config['skin'],
                hair_style=st.session_state.buddy_config['hair_style'],
                hair_color=st.session_state.buddy_config['hair_color'],
                glasses=st.session_state.buddy_config['glasses'],
                shirt=st.session_state.buddy_config['shirt'],
                accessory=st.session_state.buddy_config['accessory'],
                size=250
            )}
            <h3 style="color:#0f172a; margin-top:12px; font-size:1.8rem;">{st.session_state.student_name}</h3>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Ready to Play! Start Adventure", use_container_width=True):
            st.session_state.screen = "adventure_map"
            st.rerun()

    with col_controls:
        tab_hair, tab_skin, tab_clothes, tab_acc = st.tabs(["Hairstyle", "Skin Tone", "Outfit", "Accessories"])

        with tab_hair:
            st.markdown("#### Choose Haircut:")
            h1, h2 = st.columns(2)
            if h1.button("Afro Puffs"):
                st.session_state.buddy_config["hair_style"] = "puffs"
                st.rerun()
            if h2.button("Curly Bob"):
                st.session_state.buddy_config["hair_style"] = "curly_bob"
                st.rerun()
            if h1.button("Fresh Fade"):
                st.session_state.buddy_config["hair_style"] = "short_fade"
                st.rerun()
            if h2.button("High Ponytail"):
                st.session_state.buddy_config["hair_style"] = "ponytail"
                st.rerun()

        with tab_skin:
            st.markdown("#### Choose Complexion:")
            s1, s2, s3, s4 = st.columns(4)
            if s1.button("Deep Brown"):
                st.session_state.buddy_config["skin"] = "#5c3818"
                st.rerun()
            if s2.button("Warm Bronze"):
                st.session_state.buddy_config["skin"] = "#8d5524"
                st.rerun()
            if s3.button("Honey Tan"):
                st.session_state.buddy_config["skin"] = "#c68642"
                st.rerun()
            if s4.button("Peaches"):
                st.session_state.buddy_config["skin"] = "#f1c27d"
                st.rerun()

        with tab_clothes:
            st.markdown("#### Choose Shirt Color:")
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("Pink"):
                st.session_state.buddy_config["shirt"] = "#ec4899"
                st.rerun()
            if c2.button("Sky Blue"):
                st.session_state.buddy_config["shirt"] = "#0284c7"
                st.rerun()
            if c3.button("Sunshine"):
                st.session_state.buddy_config["shirt"] = "#eab308"
                st.rerun()
            if c4.button("Emerald"):
                st.session_state.buddy_config["shirt"] = "#16a34a"
                st.rerun()

        with tab_acc:
            st.markdown("#### Accessories & Eyewear:")
            a1, a2 = st.columns(2)
            if a1.button("Gold Glasses"):
                st.session_state.buddy_config["glasses"] = "gold_round"
                st.rerun()
            if a2.button("Star Shades"):
                st.session_state.buddy_config["glasses"] = "cool_shades"
                st.rerun()
            if a1.button("Royal Crown"):
                st.session_state.buddy_config["accessory"] = "crown"
                st.rerun()
            if a2.button("Hero Cape"):
                st.session_state.buddy_config["accessory"] = "cape"
                st.rerun()

# =========================================================
# SCREEN 3: ADVENTURE MAP (KHAN KIDS CURRICULUM ISLANDS)
# =========================================================
elif st.session_state.screen == "adventure_map":
    # Top HUD
    st.markdown(f"""
    <div class="hud-bar">
        <div style="display:flex; align-items:center; gap:12px;">
            {get_avatar_svg(
                skin=st.session_state.buddy_config['skin'],
                hair_style=st.session_state.buddy_config['hair_style'],
                hair_color=st.session_state.buddy_config['hair_color'],
                glasses=st.session_state.buddy_config['glasses'],
                shirt=st.session_state.buddy_config['shirt'],
                accessory=st.session_state.buddy_config['accessory'],
                size=54
            )}
            <div>
                <b style="font-size:1.4rem; color:#0f172a;">{st.session_state.student_name}'s Quest</b><br>
                <span style="color:#0284c7; font-weight:800; font-size:1.05rem;">Kindergarten Scholar</span>
            </div>
        </div>
        <div style="display:flex; gap:14px;">
            <div class="badge-star">Stars: {st.session_state.stars}</div>
            <div class="badge-star" style="background:#dcfce7; color:#166534; border-color:#86efac;">Streak: {st.session_state.streak}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Activity Stations
    st.markdown("""
    <div style="text-align:center; margin-bottom:14px;">
        <h2 style="color:#0369a1; font-size:2.3rem;">CHOOSE YOUR LEARNING STATION</h2>
    </div>
    """, unsafe_allow_html=True)

    nav1, nav2, nav3, nav4 = st.columns(4)
    with nav1:
        if st.button("Reading & Sight Words", use_container_width=True):
            st.session_state.active_activity = "sight_words"
            st.session_state.show_hint = False
            st.rerun()
    with nav2:
        if st.button("Parts of a Book", use_container_width=True):
            st.session_state.active_activity = "book_parts"
            st.session_state.show_hint = False
            st.rerun()
    with nav3:
        if st.button("Number Detective (Counting)", use_container_width=True):
            st.session_state.active_activity = "numbers"
            st.session_state.show_hint = False
            st.rerun()
    with nav4:
        if st.button("Word Family Spelling", use_container_width=True):
            st.session_state.active_activity = "spelling"
            st.session_state.show_hint = False
            st.rerun()

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # ACTIVITY 1: SIGHT WORDS WITH TRACING PAD
    # -------------------------------------------------------------
    if st.session_state.active_activity == "sight_words":
        words_pool = ["THE", "AND", "WAS", "YOU", "FOR", "SEE"]
        if "sw_word" not in st.session_state:
            st.session_state.sw_word = "THE"

        speak(f"Read this word out loud, then trace it with your finger: {st.session_state.sw_word}")

        st.markdown(f"""
        <div class="game-stage-card">
            <h3 style="color:#ef4444; font-size:1.6rem; margin:0 0 6px 0;">SIGHT WORD EXPLORER</h3>
            <div style="font-size:5.5rem; font-weight:900; color:#dc2626; letter-spacing:8px; margin: 10px 0;">
                {st.session_state.sw_word}
            </div>
            <p style="font-size:1.25rem; font-weight:800; color:#64748b;">Read it, trace it below with your finger, and check your work!</p>
        </div>
        """, unsafe_allow_html=True)

        col_pad, col_check = st.columns([2, 1])
        with col_pad:
            # Interactive Canvas Tracing Pad
            html_trace = """
            <div style="background:#f8fafc; border:4px dashed #0284c7; border-radius:26px; padding:12px; text-align:center;">
                <canvas id="cPad" width="480" height="180" style="background:#ffffff; border-radius:20px; touch-action:none; cursor:crosshair; border:3px solid #cbd5e1;"></canvas>
                <div style="margin-top:10px;">
                    <button onclick="clearPad()" style="background:#ef4444; color:#fff; font-size:1.2rem; font-weight:800; border:none; border-radius:16px; padding:10px 22px; cursor:pointer;">Clear</button>
                    <button onclick="savePad()" style="background:#22c55e; color:#fff; font-size:1.2rem; font-weight:800; border:none; border-radius:16px; padding:10px 22px; cursor:pointer;">Star Writing</button>
                </div>
            </div>
            <script>
                const cvs = document.getElementById('cPad');
                const ctx = cvs.getContext('2d');
                let drawing = false;

                function getPos(e) {
                    const r = cvs.getBoundingClientRect();
                    const cx = e.touches ? e.touches[0].clientX : e.clientX;
                    const cy = e.touches ? e.touches[0].clientY : e.clientY;
                    return { x: cx - r.left, y: cy - r.top };
                }
                function start(e) { e.preventDefault(); drawing = true; const p = getPos(e); ctx.beginPath(); ctx.moveTo(p.x, p.y); }
                function draw(e) {
                    if (!drawing) return;
                    e.preventDefault();
                    const p = getPos(e);
                    ctx.lineWidth = 10;
                    ctx.lineCap = 'round';
                    ctx.strokeStyle = '#ec4899';
                    ctx.lineTo(p.x, p.y);
                    ctx.stroke();
                }
                function end(e) { drawing = false; ctx.beginPath(); }
                cvs.addEventListener('mousedown', start);
                cvs.addEventListener('mousemove', draw);
                window.addEventListener('mouseup', end);
                cvs.addEventListener('touchstart', start, {passive:false});
                cvs.addEventListener('touchmove', draw, {passive:false});
                window.addEventListener('touchend', end);
                function clearPad() { ctx.clearRect(0, 0, cvs.width, cvs.height); }
                function savePad() { alert('Great tracing job!'); }
            </script>
            """
            components.html(html_trace, height=270)

        with col_check:
            st.markdown("#### Finished reading?")
            if st.button("I Mastered It! (+1 Star)", use_container_width=True):
                st.session_state.stars += 1
                st.session_state.streak += 1
                st.session_state.sw_word = random.choice([w for w in words_pool if w != st.session_state.sw_word])
                st.balloons()
                st.rerun()

            if st.button("Try Another Word", use_container_width=True):
                st.session_state.sw_word = random.choice([w for w in words_pool if w != st.session_state.sw_word])
                st.rerun()

    # -------------------------------------------------------------
    # ACTIVITY 2: INTERACTIVE PARTS OF A BOOK
    # -------------------------------------------------------------
    elif st.session_state.active_activity == "book_parts":
        st.markdown("""
        <div class="game-stage-card">
            <h3 style="color:#1d4ed8; font-size:1.8rem; margin:0;">INTERACTIVE BOOK DETECTIVE</h3>
            <p style="color:#475569; font-size:1.25rem; font-weight:700;">Look at the book graphic and tap the part you think it is!</p>
        </div>
        """, unsafe_allow_html=True)

        col_img, col_quiz = st.columns([1.2, 1.4])

        with col_img:
            st.markdown(f"""
            <div style="background:#f8fafc; border:4px solid #93c5fd; border-radius:28px; padding:20px; text-align:center;">
                {get_book_illustration(part="spine")}
            </div>
            """, unsafe_allow_html=True)

        with col_quiz:
            speak("Look at the golden yellow border on the side edge! What holds the pages together like a backbone?")
            st.markdown("#### What is the side edge called that holds all the pages together?")
            
            b1, b2 = st.columns(2)
            if b1.button("The Spine", use_container_width=True):
                st.session_state.stars += 1
                st.session_state.show_hint = False
                st.balloons()
                speak("Awesome job! The spine holds the pages together tightly!")
                st.success("Correct! The spine is the book's backbone.")

            if b2.button("Front Cover", use_container_width=True):
                st.session_state.show_hint = True
                speak("Almost! The front cover is on the front. Look at the side edge!")

            if st.session_state.show_hint:
                st.info("Hint: The spine is the backbone on the side of the book!")

    # -------------------------------------------------------------
    # ACTIVITY 3: NUMBER DETECTIVE (REAL JELLYBEAN JARS)
    # -------------------------------------------------------------
    elif st.session_state.active_activity == "numbers":
        st.markdown("""
        <div class="game-stage-card">
            <h3 style="color:#b45309; font-size:1.8rem; margin:0;">CANDY SHOP NUMBER DETECTIVE</h3>
            <p style="color:#475569; font-size:1.25rem; font-weight:700;">Count the jellybeans in each jar! Which card shows exactly 18?</p>
        </div>
        """, unsafe_allow_html=True)

        col_j1, col_j2 = st.columns(2)

        with col_j1:
            st.markdown(f"""
            <div style="background:#ffffff; border:4px solid #38bdf8; border-radius:28px; padding:16px; text-align:center;">
                <div style="display:flex; justify-content:center; gap:12px;">
                    {get_candy_jar_svg(count=10, bean_color="#ef4444")}
                    {get_candy_jar_svg(count=8, bean_color="#22c55e")}
                </div>
                <h4 style="color:#0369a1; font-size:1.4rem; margin-top:8px;">Jar 1 (10) + Jar 2 (8)</h4>
            </div>
            """, unsafe_allow_html=True)
            if st.button("This shows 18!", key="jar_corr", use_container_width=True):
                st.session_state.stars += 1
                st.balloons()
                speak("Yes! Ten red beans plus eight green beans makes 18!")
                st.success("Correct! 10 + 8 = 18!")

        with col_j2:
            st.markdown(f"""
            <div style="background:#ffffff; border:4px solid #f87171; border-radius:28px; padding:16px; text-align:center;">
                <div style="display:flex; justify-content:center; gap:12px;">
                    {get_candy_jar_svg(count=10, bean_color="#3b82f6")}
                    {get_candy_jar_svg(count=4, bean_color="#f59e0b")}
                </div>
                <h4 style="color:#dc2626; font-size:1.4rem; margin-top:8px;">Jar 1 (10) + Jar 2 (4)</h4>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Is this 18?", key="jar_wrong", use_container_width=True):
                speak("Count carefully! Ten plus four is 14, not 18! Try the other jar!")
                st.warning("10 + 4 = 14. Look for 18!")

    # -------------------------------------------------------------
    # ACTIVITY 4: WORD FAMILY SPELLING
    # -------------------------------------------------------------
    elif st.session_state.active_activity == "spelling":
        st.markdown("""
        <div class="game-stage-card">
            <h3 style="color:#7e22ce; font-size:1.8rem; margin:0;">WORD FAMILY BUILDER: -AT FAMILY</h3>
            <p style="color:#475569; font-size:1.25rem; font-weight:700;">Tap a starting letter to spell and rhyme!</p>
        </div>
        """, unsafe_allow_html=True)
        speak("Tap a letter tile to spell a new rhyming word!")

        s1, s2, s3, s4 = st.columns(4)
        if s1.button("C + AT"):
            speak("C plus A T spells CAT!")
            st.success("CAT! Great job!")
            st.session_state.stars += 1

        if s2.button("B + AT"):
            speak("B plus A T spells BAT!")
            st.success("BAT! Wonderful spelling!")
            st.session_state.stars += 1

        if s3.button("H + AT"):
            speak("H plus A T spells HAT!")
            st.success("HAT! You made a word!")
            st.session_state.stars += 1

        if s4.button("R + AT"):
            speak("R plus A T spells RAT!")
            st.success("RAT! Super rhyming!")
            st.session_state.stars += 1

    st.markdown("---")
    if st.button("Switch Character / Go Back to Profile"):
        st.session_state.screen = "profile_select"
        st.rerun()
