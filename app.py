import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime
from supabase import create_client, Client

st.set_page_config(
    page_title="Gracyn's Learning Adventure Studio",
    page_icon="🐣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- KHAN ACADEMY KIDS ARCADE STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700;800&family=Quicksand:wght@600;700;800&display=swap');

    .stApp {
        background: linear-gradient(180deg, #e0f2fe 0%, #bae6fd 40%, #7dd3fc 100%) !important;
        font-family: 'Fredoka', 'Quicksand', cursive, sans-serif !important;
    }

    /* Tactile Profile Bubbles */
    .profile-bubble {
        width: 170px;
        height: 170px;
        border-radius: 50%;
        background: #ffffff;
        border: 7px solid #38bdf8;
        box-shadow: 0 14px 30px rgba(0,0,0,0.15);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px auto;
        transition: transform 0.15s ease;
    }

    /* Big Tactile Buttons for iPad */
    .stButton > button {
        border-radius: 28px !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        padding: 14px 26px !important;
        box-shadow: 0 8px 0 rgba(0,0,0,0.18) !important;
        transition: transform 0.08s ease !important;
        border: 3.5px solid #ffffff !important;
    }
    .stButton > button:active {
        transform: translateY(6px) !important;
        box-shadow: 0 2px 0 rgba(0,0,0,0.18) !important;
    }

    /* High-contrast Selectors */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 3.5px solid #0284c7 !important;
        border-radius: 22px !important;
        color: #0f172a !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        box-shadow: 0 6px 0 rgba(0,0,0,0.12) !important;
    }

    /* Mascot Speech Banner */
    .mascot-banner {
        display: flex;
        align-items: center;
        gap: 16px;
        background: #ffffff;
        border: 4px solid #38bdf8;
        border-radius: 30px;
        padding: 16px 22px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.1);
        margin-bottom: 18px;
    }

    .mascot-face {
        font-size: 4.2rem;
        background: #f0fdf4;
        border: 3.5px solid #22c55e;
        border-radius: 50%;
        width: 90px;
        height: 90px;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: floatMascot 2.5s ease-in-out infinite alternate;
        flex-shrink: 0;
    }

    @keyframes floatMascot {
        0% { transform: translateY(0px) rotate(-3deg); }
        100% { transform: translateY(-7px) rotate(3deg); }
    }

    .mascot-speech {
        background: #f8fafc;
        border: 3px solid #60a5fa;
        border-radius: 24px;
        padding: 12px 18px;
        flex: 1;
        font-size: 1.2rem;
        font-weight: 700;
        color: #0f172a;
    }

    .instruction-card {
        background: #ffffff;
        border-radius: 26px;
        padding: 16px 22px;
        border: 3.5px solid #60a5fa;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        margin-bottom: 16px;
        text-align: center;
    }

    .jar-container {
        background: #ffffff;
        border: 4px solid #0284c7;
        border-radius: 26px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 8px 22px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- DIRECT UNIVERSAL WEBAUDIO & SPEECH SYNTHESIS ENGINE ---
def speak(text, sfx="pop"):
    sound_url = {
        "pop": "https://cdn.freesound.org/previews/536/536108_11565331-lq.mp3",
        "cheer": "https://cdn.freesound.org/previews/270/270304_5123851-lq.mp3",
        "tada": "https://cdn.freesound.org/previews/397/397355_4284968-lq.mp3",
        "tryagain": "https://cdn.freesound.org/previews/415/415079_5121236-lq.mp3"
    }.get(sfx, "")

    clean_text = text.replace('"', '\\"').replace("'", "\\'")
    js = f"""
    <script>
        (function() {{
            try {{
                let snd = new Audio("{sound_url}");
                snd.volume = 0.55;
                snd.play().catch(() => {{}});
            }} catch(e) {{}}

            function triggerSpeech() {{
                const synth = (window.parent && window.parent.speechSynthesis) 
                    ? window.parent.speechSynthesis 
                    : window.speechSynthesis;
                if (!synth) return;

                try {{
                    synth.cancel();
                    if (synth.paused) synth.resume();
                }} catch(e) {{}}

                const utter = new SpeechSynthesisUtterance("{clean_text}");
                utter.rate = 0.84;
                utter.pitch = 1.22;
                utter.lang = 'en-US';

                const voices = synth.getVoices();
                if (voices && voices.length > 0) {{
                    const preferred = voices.find(v => (v.name.includes("Samantha") || v.name.includes("Victoria") || v.name.includes("Karen") || v.lang === "en-US") && !v.name.includes("Bad"));
                    if (preferred) utter.voice = preferred;
                }}

                synth.speak(utter);
            }}

            triggerSpeech();
            setTimeout(triggerSpeech, 250);
        }})();
    </script>
    """
    components.html(js, height=0)

def render_mascot_guide(text, name="Chickie", emoji="🐥"):
    st.markdown(f"""
    <div class="mascot-banner">
        <div class="mascot-face">{emoji}</div>
        <div class="mascot-speech">
            <b style="color:#0284c7;">{name} says:</b><br>
            "{text}"
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- PERSISTENT PROFILES DATABASE (SUPABASE READY) ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        pass

# Default stored profiles
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "Gracyn": {
            "avatar": "🦄",
            "buddy": {"skin": "🏽", "hair": "👧🏾", "glasses": "👓", "shirt": "🚀"},
            "coins": 50,
            "stars": 12,
            "streak": 3,
            "sw_score_count": 0,
            "daily_log": {}
        }
    }

if "active_user" not in st.session_state:
    st.session_state.active_user = None

if "screen" not in st.session_state:
    st.session_state.screen = "profile_picker"

if "current_game" not in st.session_state:
    st.session_state.current_game = "📖 Sight Words"

if "selected_sw_list" not in st.session_state:
    st.session_state.selected_sw_list = "⭐ List 1 (12 Words)"

if "trigger_treasure" not in st.session_state:
    st.session_state.trigger_treasure = False

# SIGHT WORD BANK
SIGHT_WORD_LISTS = {
    "⭐ List 1 (12 Words)": ["a", "at", "do", "was", "the", "as", "I", "you", "am", "to", "is", "an"],
    "🌟 List 2 (12 Words)": ["man", "did", "of", "your", "in", "sit", "for", "said", "it", "can", "from", "all"]
}

# Progress Logging
def track_score(activity, detail, points=10, stars=1):
    user = st.session_state.active_user
    data = st.session_state.profiles[user]
    data["coins"] += points
    data["stars"] += stars
    data["streak"] += 1
    
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    if today_str not in data["daily_log"]:
        data["daily_log"][today_str] = {"attempts": 0, "correct": 0, "activities": []}
    data["daily_log"][today_str]["attempts"] += 1
    data["daily_log"][today_str]["correct"] += 1
    data["daily_log"][today_str]["activities"].append({
        "time": datetime.now().strftime("%I:%M %p"),
        "activity": activity,
        "detail": detail,
        "result": "Passed"
    })

    if supabase:
        try:
            supabase.table("student_milestones").insert({
                "student_name": user,
                "date_stamp": today_str,
                "activity_type": activity,
                "action_result": "Passed",
                "detail": detail,
                "coins": data["coins"],
                "stars": data["stars"]
            }).execute()
        except Exception:
            pass

# Tracing Pad
def tracing_box(word):
    html = f"""
    <div style="background:#f8fafc; border:4px dashed #0284c7; border-radius:26px; padding:14px; text-align:center;">
        <canvas id="cPad" width="340" height="155" style="background:#ffffff; border-radius:20px; touch-action:none; cursor:crosshair; border:3px solid #cbd5e1;"></canvas>
        <div style="margin-top:12px; display:flex; justify-content:center; gap:12px;">
            <button onclick="clearPad()" style="background:#ef4444; color:#fff; font-size:1.15rem; font-weight:800; border:none; border-radius:18px; padding:10px 22px; box-shadow:0 4px 0 #b91c1c; cursor:pointer;">🧹 Erase</button>
            <button onclick="checkTrace()" style="background:#22c55e; color:#fff; font-size:1.15rem; font-weight:800; border:none; border-radius:18px; padding:10px 22px; box-shadow:0 4px 0 #15803d; cursor:pointer;">⭐ Check Writing!</button>
        </div>
        <div id="cMsg" style="font-size:1.35rem; font-weight:800; color:#16a34a; margin-top:10px; min-height:35px;"></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
        const cvs = document.getElementById('cPad');
        const ctx = cvs.getContext('2d');
        let isPressing = false;

        function getCoordinates(e) {{
            const rect = cvs.getBoundingClientRect();
            if (e.touches && e.touches.length > 0) {{
                return {{ x: e.touches[0].clientX - rect.left, y: e.touches[0].clientY - rect.top }};
            }}
            return {{ x: e.clientX - rect.left, y: e.clientY - rect.top }};
        }}

        function handleDown(e) {{
            if (e.type === 'mousedown' && e.button !== 0) return;
            e.preventDefault();
            isPressing = true;
            const pt = getCoordinates(e);
            ctx.beginPath();
            ctx.moveTo(pt.x, pt.y);
            ctx.lineWidth = 10;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.strokeStyle = '#ec4899';
        }}

        function handleMove(e) {{
            if (!isPressing) return;
            e.preventDefault();
            if (e.type === 'mousemove' && e.buttons === 0) {{
                isPressing = false;
                ctx.beginPath();
                return;
            }}
            const pt = getCoordinates(e);
            ctx.lineTo(pt.x, pt.y);
            ctx.stroke();
        }}

        function handleUp(e) {{
            if (isPressing) {{ isPressing = false; ctx.beginPath(); }}
        }}

        cvs.addEventListener('mousedown', handleDown);
        cvs.addEventListener('mousemove', handleMove);
        window.addEventListener('mouseup', handleUp);

        cvs.addEventListener('touchstart', handleDown, {{ passive: false }});
        cvs.addEventListener('touchmove', handleMove, {{ passive: false }});
        window.addEventListener('touchend', handleUp, {{ passive: false }});
        window.addEventListener('touchcancel', handleUp, {{ passive: false }});

        function clearPad() {{
            ctx.clearRect(0, 0, cvs.width, cvs.height);
            document.getElementById('cMsg').innerText = '';
        }}

        function checkTrace() {{
            confetti({{ particleCount: 90, spread: 75, origin: {{ y: 0.75 }} }});
            document.getElementById('cMsg').innerText = "🌟 WOW! Great handwriting!";
            let a = new Audio('https://cdn.freesound.org/previews/270/270304_5123851-lq.mp3');
            a.play().catch(() => {{}});
        }}
    </script>
    """
    components.html(html, height=330)

# Instant Speech Input
def speech_box(target_word):
    clean_target = target_word.strip().lower()
    html = f"""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <div style="text-align:center; margin-top:8px;">
        <button id="micB" style="background:#f97316; color:#ffffff; font-size:1.35rem; font-weight:800; border:none; border-radius:26px; padding:14px 28px; box-shadow:0 6px 0 #c2410c; cursor:pointer;" onclick="listenNow()">
            🎙️ Tap to Say Your Word
        </button>
        <div id="mRes" style="font-size:1.35rem; font-weight:800; margin-top:10px; min-height:30px;"></div>
    </div>
    <script>
        let rec = null;
        let answered = false;

        function listenNow() {{
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            const res = document.getElementById('mRes');
            const btn = document.getElementById('micB');
            if (!SpeechRec) {{ res.innerHTML = "<span style='color:red;'>Please use Safari or Chrome!</span>"; return; }}

            answered = false;
            rec = new SpeechRec();
            rec.lang = 'en-US';
            rec.interimResults = true;

            btn.innerText = "👂 Listening...";
            btn.style.background = "#22c55e";
            res.innerHTML = "";

            rec.onresult = (e) => {{
                if (answered) return;
                let heard = "";
                for (let i = 0; i < e.results.length; ++i) {{
                    heard += e.results[i][0].transcript.toLowerCase();
                }}
                heard = heard.trim();
                let target = "{clean_target}";
                let match = (heard.includes(target) || target.includes(heard));

                if (target === "to" && (heard.includes("two") || heard.includes("too") || heard.includes("2"))) match = true;
                if (target === "for" && (heard.includes("four") || heard.includes("4"))) match = true;
                if (target === "i" && (heard.includes("eye") || heard === "ay")) match = true;

                if (match) {{
                    answered = true;
                    try {{ rec.stop(); }} catch(err) {{}}
                    confetti({{ particleCount: 120, spread: 80, origin: {{ y: 0.7 }} }});
                    let a = new Audio('https://cdn.freesound.org/previews/270/270304_5123851-lq.mp3');
                    a.play().catch(() => {{}});
                    res.innerHTML = "<span style='color:#15803d;'>🎉 YES! You read it correctly! 🌟</span>";
                    btn.innerText = '🎙️ Tap to Say Again';
                    btn.style.background = "#f97316";
                }}
            }};

            rec.onspeechend = () => {{
                setTimeout(() => {{
                    if (!answered) {{
                        btn.innerText = '🎙️ Tap to Say Your Word';
                        btn.style.background = "#f97316";
                    }}
                }}, 400);
            }};

            rec.start();
        }}
    </script>
    """
    components.html(html, height=125)

# =========================================================
# SCREEN 1: KHAN ACADEMY KIDS PROFILE SELECTOR HUB
# =========================================================
if st.session_state.screen == "profile_picker":
    st.markdown("""
    <div style="text-align:center; padding:25px 0 10px 0;">
        <div style="font-size:3.5rem; font-weight:900; color:#0284c7; display:flex; justify-content:center; align-items:center; gap:12px;">
            <span>🛡️</span> Adventure Academy
        </div>
        <div style="font-size:1.6rem; color:#475569; font-weight:800;">Who is ready to learn today? Tap your name!</div>
    </div>
    """, unsafe_allow_html=True)
    speak("Who is ready to learn today? Tap your name, or tap new to create a profile!")

    # Render Profiles in Khan-Kids Circular Bubbles
    prof_names = list(st.session_state.profiles.keys())
    cols = st.columns(len(prof_names) + 1)

    for i, name in enumerate(prof_names):
        prof = st.session_state.profiles[name]
        with cols[i]:
            st.markdown(f"""
            <div class="profile-bubble">
                <div style="font-size:5rem;">{prof['avatar']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"⭐ {name}", key=f"sel_prof_{name}", use_container_width=True):
                st.session_state.active_user = name
                st.session_state.screen = "adventure_hub"
                speak(f"Welcome back {name}! Let's start learning!")
                st.rerun()

    # The "+ NEW" Profile Bubble
    with cols[-1]:
        st.markdown("""
        <div class="profile-bubble" style="border:7px dashed #94a3b8; background:#f8fafc;">
            <div style="font-size:4.5rem; color:#0284c7;">➕</div>
            <div style="font-weight:900; color:#0369a1; font-size:1.2rem;">NEW</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("➕ Add Person", key="btn_add_person", use_container_width=True):
            st.session_state.screen = "buddy_creator"
            st.rerun()

# =========================================================
# SCREEN 2: BUDDY CREATION STUDIO
# =========================================================
elif st.session_state.screen == "buddy_creator":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:2rem; font-weight:900; color:#b45309;">🎨 Buddy Creation Studio</div>
        <div style="font-size:1.2rem; font-weight:700; color:#475569;">Design your learning buddy to guide you through your adventure!</div>
    </div>
    """, unsafe_allow_html=True)
    speak("Welcome to the buddy creation studio! Type your name and pick your favorite hair, skin tone, and outfit!")

    new_name = st.text_input("What is your name?", value="", placeholder="Type your name here...")

    b_col1, b_col2 = st.columns([1, 1.2])

    if "temp_buddy" not in st.session_state:
        st.session_state.temp_buddy = {"skin": "🏽", "hair": "👧🏾", "glasses": "👓", "shirt": "🚀", "avatar": "🦄"}

    b = st.session_state.temp_buddy

    with b_col1:
        st.markdown(f"""
        <div style="background:#ffffff; border:5px solid #38bdf8; border-radius:32px; padding:30px; text-align:center; box-shadow:0 12px 28px rgba(0,0,0,0.1);">
            <div style="font-size:7.5rem; line-height:1.1;">{b['hair']}</div>
            <div style="font-size:4rem; margin-top:-20px;">{b['glasses']}</div>
            <div style="font-size:4.5rem; margin-top:-10px;">{b['shirt']}</div>
            <div style="font-size:1.6rem; font-weight:900; color:#0284c7; margin-top:10px;">Buddy Preview</div>
        </div>
        """, unsafe_allow_html=True)

    with b_col2:
        st.markdown("#### 1. Pick Hair & Style:")
        h_cols = st.columns(5)
        for idx, h in enumerate(["👧🏾", "👧🏽", "👧🏼", "👦🏾", "👦🏽"]):
            if h_cols[idx].button(h, key=f"bh_{idx}"):
                b["hair"] = h
                st.rerun()

        st.markdown("#### 2. Pick Glasses / Accessories:")
        g_cols = st.columns(4)
        for idx, g in enumerate(["👓", "🕶️", "👑", "🎀"]):
            if g_cols[idx].button(g, key=f"bg_{idx}"):
                b["glasses"] = g
                st.rerun()

        st.markdown("#### 3. Pick Outfit Theme:")
        s_cols = st.columns(4)
        for idx, s in enumerate(["🚀", "⭐", "🎨", "⚽"]):
            if s_cols[idx].button(s, key=f"bs_{idx}"):
                b["shirt"] = s
                st.rerun()

        st.markdown("#### 4. Pick Your Mascot Avatar Icon:")
        a_cols = st.columns(4)
        for idx, a in enumerate(["🦄", "🐯", "🐼", "🐬"]):
            if a_cols[idx].button(a, key=f"ba_{idx}"):
                b["avatar"] = a
                st.rerun()

    if st.button("🎉 Save My Buddy & Start Learning!", use_container_width=True):
        final_name = new_name.strip() if new_name.strip() else "Superstar"
        st.session_state.profiles[final_name] = {
            "avatar": b["avatar"],
            "buddy": b,
            "coins": 50,
            "stars": 10,
            "streak": 1,
            "sw_score_count": 0,
            "daily_log": {}
        }
        st.session_state.active_user = final_name
        st.session_state.screen = "adventure_hub"
        speak(f"Awesome! Welcome to Adventure Academy {final_name}!")
        st.rerun()

# =========================================================
# SCREEN 3: MAIN ADVENTURE HUB & ACTIVITIES
# =========================================================
elif st.session_state.screen == "adventure_hub":
    curr_user = st.session_state.active_user
    u_data = st.session_state.profiles[curr_user]
    buddy = u_data.get("buddy", {"hair": "👧🏾", "shirt": "🚀"})

    # TOP HUD
    hud_c1, hud_c2, hud_c3 = st.columns([1.8, 2, 1.4])
    with hud_c1:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="font-size:3.2rem; background:#ffffff; border-radius:50%; border:3.5px solid #38bdf8; width:72px; height:72px; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
                {u_data['avatar']}
            </div>
            <div>
                <b style="font-size:1.4rem; color:#0f172a;">{curr_user}'s Quest</b><br>
                <span style="color:#0284c7; font-weight:800; font-size:1.05rem;">Buddy: {buddy['hair']}{buddy['shirt']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with hud_c2:
        progress_val = min(1.0, (u_data['sw_score_count'] % 12) / 6.0) if u_data['sw_score_count'] <= 6 else min(1.0, (u_data['sw_score_count'] % 12) / 12.0)
        st.progress(progress_val)
        st.markdown(f"<div style='text-align:center; font-weight:800; color:#0369a1;'>🎁 {u_data['sw_score_count'] % 6}/6 Words to Treasure Box! (Streak: 🔥 {u_data['streak']})</div>", unsafe_allow_html=True)

    with hud_c3:
        ch1, ch2 = st.columns(2)
        ch1.markdown(f"<div class='hud-chip'>🪙 {u_data['coins']}</div>", unsafe_allow_html=True)
        ch2.markdown(f"<div class='hud-chip'>⭐ {u_data['stars']}</div>", unsafe_allow_html=True)

    # Station Chooser
    st.markdown("""
    <div class="instruction-card">
        <span style="font-size:1.3rem; font-weight:800; color:#0369a1;">🎮 Choose Your Learning Adventure Station:</span>
    </div>
    """, unsafe_allow_html=True)

    game_modes = [
        "📖 Sight Words",
        "📚 Parts of a Book & Story Time",
        "🕵️ Number Detective (20 & Under)",
        "🔤 Word Family Spelling Lab",
        "🔍 Letter I-Spy Safari",
        "🍁 Seasons & Nature Quest",
        "➕ Cool Math (10 and Under)",
        "📊 Parent Progress Portal"
    ]
    active_game = st.selectbox("", game_modes, index=game_modes.index(st.session_state.current_game), label_visibility="collapsed")
    if active_game != st.session_state.current_game:
        st.session_state.current_game = active_game
        st.rerun()

    # 1. SIGHT WORDS
    if active_game == "📖 Sight Words":
        mascot_msg = f"Hey {curr_user}! Read the big word card, tap the orange button to say it, and trace it with your finger!"
        render_mascot_guide(mascot_msg, "Buddy", buddy['hair'])
        speak(mascot_msg)

        sel_col1, sel_col2 = st.columns([1.2, 1])
        with sel_col1:
            st.markdown("<b style='font-size:1.15rem; color:#0c4a6e;'>📚 Choose Word List:</b>", unsafe_allow_html=True)
            chosen_list = st.selectbox(
                "Word List",
                list(SIGHT_WORD_LISTS.keys()),
                index=list(SIGHT_WORD_LISTS.keys()).index(st.session_state.selected_sw_list),
                label_visibility="collapsed"
            )
            if chosen_list != st.session_state.selected_sw_list:
                st.session_state.selected_sw_list = chosen_list
                st.session_state.current_sw = SIGHT_WORD_LISTS[chosen_list][0]
                st.rerun()

        active_bank = SIGHT_WORD_LISTS[st.session_state.selected_sw_list]
        if "current_sw" not in st.session_state or st.session_state.current_sw not in active_bank:
            st.session_state.current_sw = active_bank[0]

        with sel_col2:
            st.markdown("<b style='font-size:1.15rem; color:#0c4a6e;'>🎯 Target Word:</b>", unsafe_allow_html=True)
            picked = st.selectbox("Target Word", active_bank, index=active_bank.index(st.session_state.current_sw), label_visibility="collapsed")
            if picked != st.session_state.current_sw:
                st.session_state.current_sw = picked
                st.rerun()

        word = st.session_state.current_sw

        w_col1, w_col2 = st.columns([1, 1.25])
        with w_col1:
            st.markdown(f"""
            <div style="background:#ffffff; border:5px solid #f87171; border-radius:32px; padding:22px; text-align:center; box-shadow:0 12px 28px rgba(0,0,0,0.08);">
                <div style="font-size:1.4rem; color:#ef4444; font-weight:800;">❤️ {st.session_state.selected_sw_list.split('(')[0].strip()}</div>
                <div style="font-size:5.5rem; font-weight:900; color:#dc2626; letter-spacing:6px; margin:8px 0;">{word.upper()}</div>
                <div style="font-size:1.1rem; color:#64748b; font-weight:700;">Word {active_bank.index(word) + 1} of {len(active_bank)}</div>
            </div>
            """, unsafe_allow_html=True)
            speech_box(word)

        with w_col2:
            st.markdown("""
            <div style="background:#ffffff; border-radius:24px; padding:10px 18px; border:3px solid #0284c7; margin-bottom:8px; text-align:center;">
                <b style="font-size:1.25rem; color:#0369a1;">✏️ Trace & Write with Your Finger:</b>
            </div>
            """, unsafe_allow_html=True)
            tracing_box(word.upper())

            b1, b2 = st.columns(2)
            with b1:
                if st.button("🌟 I Mastered It! (+10 🪙)", use_container_width=True):
                    u_data["sw_score_count"] += 1
                    track_score("Sight Words", f"Mastered {word}")
                    curr_i = active_bank.index(word)
                    st.session_state.current_sw = active_bank[(curr_i + 1) % len(active_bank)]
                    st.rerun()
            with b2:
                if st.button("➡️ Next Word 🎲", use_container_width=True):
                    rem = [w for w in active_bank if w != word]
                    st.session_state.current_sw = random.choice(rem) if rem else word
                    st.rerun()

    # 2. PARTS OF A BOOK
    elif active_game == "📚 Parts of a Book & Story Time":
        b_tab1, b_tab2, b_tab3 = st.tabs(["🎓 Step 1: Touch & Learn", "📖 Step 2: Read Story & Recall", "🕵️ Step 3: Detective Quiz"])

        with b_tab1:
            msg_p1 = "Tap each glowing part of the book below so I can show you what it does!"
            render_mascot_guide(msg_p1, "Bella", "🐶")
            speak(msg_p1)

            p1, p2, p3 = st.columns(3)
            p4, p5, p6 = st.columns(3)
            with p1:
                if st.button("📕 Front Cover", use_container_width=True):
                    speak("The front cover is the strong front door that protects the pages inside!")
                    st.info("📕 **Front Cover:** Heavy cardboard that protects the book.")
            with p2:
                if st.button("🏷️ The Title", use_container_width=True):
                    speak("The title is the big name of the book that tells you what the story is about!")
                    st.info("🏷️ **Title:** The name of the story.")
            with p3:
                if st.button("🧑‍🏫 The Author", use_container_width=True):
                    speak("The author is the writer who writes all the words in the story!")
                    st.info("🧑‍🏫 **Author:** The person who writes words.")
            with p4:
                if st.button("🎨 The Illustrator", use_container_width=True):
                    speak("The illustrator is the artist who paints all the colorful pictures!")
                    st.info("🎨 **Illustrator:** The artist drawing pictures.")
            with p5:
                if st.button("📏 The Spine", use_container_width=True):
                    speak("The spine is the side edge that holds all the pages tightly together like your backbone!")
                    st.info("📏 **Spine:** The backbone binding all pages.")
            with p6:
                if st.button("📘 The Back Cover", use_container_width=True):
                    speak("The back cover has the barcode and a quick summary of the story!")
                    st.info("📘 **Back Cover:** Has the barcode.")

        with b_tab2:
            msg_story = "Listen to our mini story about Bella the Pup! Pay close attention to what happens!"
            render_mascot_guide(msg_story, "Oliver Owl", "🦉")
            speak(msg_story)

            st.markdown("""
            <div style="background:#ffffff; border:4px solid #38bdf8; border-radius:28px; padding:22px; text-align:center; box-shadow:0 8px 22px rgba(0,0,0,0.08); margin-bottom:18px;">
                <div style="font-size:4rem; margin-bottom:8px;">🐶🌈🎈</div>
                <h3 style="color:#0369a1; margin-bottom:6px;">Title: Bella's Big Sunny Day</h3>
                <p style="font-size:1.35rem; color:#1e293b; font-weight:700; line-height:1.6;">
                    Once upon a time, a fluffy golden pup named Bella found a bright red balloon stuck in a tree. 
                    Bella wagged her tail, jumped with all her puppy might, and tapped the balloon with her nose. 
                    Pop! The balloon floated up into the clouds, and Bella made a new friend named Oliver the Owl!
                </p>
                <div style="background:#f0fdf4; border-radius:18px; padding:10px; font-weight:800; color:#166534; font-size:1.15rem;">
                    Written by: Raeven Brown (Author)  •  Illustrated by: Gracyn (Artist)
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔊 Read Story Aloud", use_container_width=True):
                speak("Bella's Big Sunny Day! Once upon a time, a fluffy golden pup named Bella found a bright red balloon stuck in a tree. Bella wagged her tail, jumped with all her puppy might, and tapped the balloon with her nose! Pop! The balloon floated into the clouds and Bella made a new friend named Oliver the Owl! Written by Raeven Brown, Illustrated by Gracyn!")

            st.markdown("#### 🧠 Story Recall Check:")
            rc1, rc2 = st.columns(2)
            with rc1:
                if st.button("🐶 Who was the hero? (A) Bella the Pup", use_container_width=True):
                    st.balloons()
                    speak("Yes! Bella the fluffy pup was the main character!", "cheer")
                    track_score("Story Recall", "Bella the pup")
            with rc2:
                if st.button("🐱 Was the hero a Kitty named Cleo?", use_container_width=True):
                    speak("Think back to our story! It was about Bella the brave pup!", "tryagain")

        with b_tab3:
            book_questions = [
                {
                    "target": "Front Cover", "highlight": "cover",
                    "q": "Look at the front. What part protects the book and welcomes you in?",
                    "correct": "Front Cover",
                    "opts": [
                        {"name": "Front Cover", "icon": "📕", "desc": "Front Cover with Picture"},
                        {"name": "The Spine", "icon": "📏", "desc": "Side Edge Backbone"},
                        {"name": "Back Cover", "icon": "📘", "desc": "Back of Book"},
                        {"name": "Page Numbers", "icon": "📄", "desc": "Bottom Corner Numbers"}
                    ]
                },
                {
                    "target": "The Title", "highlight": "title",
                    "q": "Look at THE BRAVE PUPPY at the top. What is the name of a book called?",
                    "correct": "The Title",
                    "opts": [
                        {"name": "The Title", "icon": "🏷️", "desc": "Name of the Book"},
                        {"name": "The Author", "icon": "🧑‍🏫", "desc": "Writes words"},
                        {"name": "The Spine", "icon": "📏", "desc": "Side Backbone"},
                        {"name": "The Illustrator", "icon": "🎨", "desc": "Draws pictures"}
                    ]
                }
            ]
            if "bq_idx" not in st.session_state: st.session_state.bq_idx = 0
            curr_q = book_questions[st.session_state.bq_idx % len(book_questions)]

            render_mascot_guide(f"{curr_user}! {curr_q['q']}", "Chickie", "🐥")
            speak(f"{curr_user}! {curr_q['q']}")

            t_key = curr_q["highlight"]
            html_book = f"""
            <div style="display:flex; justify-content:center; align-items:center; margin:10px 0 20px 0;">
                <div style="display:flex; width:380px; height:280px; box-shadow:0 16px 32px rgba(0,0,0,0.2); border-radius:14px 26px 26px 14px; background:#fff;">
                    <div style="width:50px; background:linear-gradient(90deg, #1e3a8a, #3b82f6); border-radius:14px 0 0 14px; color:#fff; writing-mode:vertical-rl; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.15rem; letter-spacing:4px; border:{'5px solid #facc15' if t_key == 'spine' else 'none'};">
                        SPINE
                    </div>
                    <div style="flex:1; background:linear-gradient(135deg, #60a5fa, #93c5fd); border-radius:0 22px 22px 0; padding:16px; display:flex; flex-direction:column; justify-content:space-between; align-items:center; border:{'5px solid #facc15' if t_key == 'cover' else 'none'};">
                        <div style="background:#fff; border:{'4px solid #facc15' if t_key == 'title' else '2px solid #2563eb'}; border-radius:16px; padding:6px 16px; font-size:1.35rem; font-weight:900; color:#1e3a8a;">
                            📖 THE BRAVE PUPPY
                        </div>
                        <div style="font-size:3.8rem;">🐶🐾</div>
                        <div style="font-size:1.05rem; font-weight:800; color:#0f172a; background:#ffffffcc; border-radius:12px; padding:4px 14px;">
                            ✍️ By Raeven Brown (Author)
                        </div>
                    </div>
                </div>
            </div>
            """
            components.html(html_book, height=300)

            cols_top = st.columns(2)
            cols_bot = st.columns(2)
            grid_cols = [cols_top[0], cols_top[1], cols_bot[0], cols_bot[1]]

            for i, opt in enumerate(curr_q["opts"]):
                with grid_cols[i]:
                    st.markdown(f"""
                    <div style="background:#ffffff; border:3.5px solid #93c5fd; border-radius:22px; padding:14px; text-align:center; margin-bottom:8px; box-shadow:0 6px 14px rgba(0,0,0,0.06);">
                        <div style="font-size:3.5rem; margin-bottom:4px;">{opt['icon']}</div>
                        <div style="font-size:1.35rem; font-weight:900; color:#0f172a;">{opt['name']}</div>
                        <div style="font-size:1.05rem; font-weight:700; color:#64748b;">{opt['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"👉 Select {opt['name']}", key=f"btn_bk_opt_{opt['name']}_{st.session_state.bq_idx}", use_container_width=True):
                        if opt["name"] == curr_q["correct"]:
                            st.balloons()
                            speak(f"Yes! That is {opt['name']}!", "cheer")
                            track_score("Parts of a Book", opt["name"])
                            st.session_state.bq_idx += 1
                            st.rerun()
                        else:
                            speak("Not quite. Look at the card again!", "tryagain")

    # 3. NUMBER DETECTIVE (20 & UNDER)
    elif active_game == "🕵️ Number Detective (20 & Under)":
        mascot_num = f"{curr_user}! We are looking for the number 18! Count the jelly beans in the glass jars and tallies!"
        render_mascot_guide(mascot_num, "Buddy", buddy['hair'])
        speak(mascot_num)

        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)

        with c1:
            st.markdown("""
            <div class="jar-container">
                <b style="font-size:1.4rem; color:#0369a1;">🫙 Candy Shop Glass Jars:</b><br>
                <div style="background:#e0f2fe; border:2.5px solid #0284c7; border-radius:18px; padding:14px; margin:10px 0;">
                    <div style="font-size:2rem; margin-bottom:4px;">🍬🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴</div>
                    <b style="font-size:1.25rem; color:#0f172a;">Jar 1: Exactly 10 Red Beans</b>
                    <div style="font-size:2rem; margin:8px 0 4px 0;">🍬🟢🟢🟢🟢🟢🟢🟢🟢</div>
                    <b style="font-size:1.25rem; color:#0f172a;">Jar 2: Exactly 8 Green Beans</b>
                </div>
                <div style="background:#fef08a; border-radius:14px; padding:6px; font-size:1.35rem; font-weight:900; color:#854d0e;">
                    10 Beans + 8 Beans
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✅ Yes! This makes 18 Beans!", key="btn_jar_18", use_container_width=True):
                st.balloons()
                speak("Yes! Ten beans plus eight beans equals 18!", "cheer")
                track_score("Number Detective", "10+8 Beans = 18")

        with c2:
            st.markdown("""
            <div class="jar-container">
                <b style="font-size:1.4rem; color:#0369a1;">🟧 Base-Ten Rods & Ones:</b><br>
                <div style="background:#e0f2fe; border:2.5px solid #0284c7; border-radius:18px; padding:14px; margin:10px 0;">
                    <div style="font-size:2rem; margin-bottom:4px;">🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦</div>
                    <b style="font-size:1.25rem; color:#0f172a;">1 Ten-Rod (10)</b>
                    <div style="font-size:2rem; margin:8px 0 4px 0;">🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟩</div>
                    <b style="font-size:1.25rem; color:#0f172a;">8 Unit Cubes (8)</b>
                </div>
                <div style="background:#fef08a; border-radius:14px; padding:6px; font-size:1.35rem; font-weight:900; color:#854d0e;">
                    1 Ten + 8 Ones
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✅ Yes! This is 18!", key="btn_base10_18", use_container_width=True):
                st.balloons()
                speak("Bingo! 1 ten rod and 8 single cubes makes 18!", "cheer")
                track_score("Number Detective", "Base Ten 18")

        with c3:
            st.markdown("""
            <div class="jar-container" style="border-color:#f87171;">
                <b style="font-size:1.4rem; color:#dc2626;">🍪 Cookie Bakery Jar:</b><br>
                <div style="background:#fee2e2; border:2.5px solid #ef4444; border-radius:18px; padding:14px; margin:10px 0;">
                    <div style="font-size:2rem; margin-bottom:4px;">🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪</div>
                    <b style="font-size:1.25rem; color:#0f172a;">Jar 1: 10 Cookies</b>
                    <div style="font-size:2rem; margin:8px 0 4px 0;">🍪🍪🍪🍪</div>
                    <b style="font-size:1.25rem; color:#0f172a;">Jar 2: 4 Cookies</b>
                </div>
                <div style="background:#fee2e2; border-radius:14px; padding:6px; font-size:1.35rem; font-weight:900; color:#b91c1c;">
                    10 Cookies + 4 Cookies
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Is this 18 Cookies? 🤔", key="btn_cookies_14", use_container_width=True):
                speak("Count carefully! Ten plus four is 14, not 18!", "tryagain")

        with c4:
            st.markdown("""
            <div class="jar-container">
                <b style="font-size:1.4rem; color:#0369a1;">🥢 Wooden Campfire Tallies:</b><br>
                <div style="background:#e0f2fe; border:2.5px solid #0284c7; border-radius:18px; padding:14px; margin:10px 0;">
                    <div style="font-size:2.2rem; letter-spacing:6px; margin-bottom:4px;">卌 卌 卌</div>
                    <b style="font-size:1.25rem; color:#0f172a;">3 Bundles of 5 = 15</b>
                    <div style="font-size:2.2rem; letter-spacing:6px; margin:8px 0 4px 0;">| | |</div>
                    <b style="font-size:1.25rem; color:#0f172a;">3 Extra Single Sticks</b>
                </div>
                <div style="background:#fef08a; border-radius:14px; padding:6px; font-size:1.35rem; font-weight:900; color:#854d0e;">
                    15 Tallies + 3 Tallies
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✅ Yes! This makes 18 Tallies!", key="btn_tally_18", use_container_width=True):
                st.balloons()
                speak("Super job! Fifteen plus three tallies is 18!", "cheer")
                track_score("Number Detective", "Tallies 18")

    # 4. WORD FAMILY SPELLING
    elif active_game == "🔤 Word Family Spelling Lab":
        family_choice = st.radio("Choose Word Family to Spell:", ["🐱 -AT Family (cat, bat, hat, rat, mat)", "🏀 -ALL Family (ball, call, tall, fall, hall)"], horizontal=True)
        if "-AT" in family_choice:
            ending = "at"
            letters = [("C", "🐱 Cat"), ("B", "🦇 Bat"), ("H", "🎩 Hat"), ("R", "🐭 Rat"), ("M", "🧘 Mat")]
        else:
            ending = "all"
            letters = [("B", "🏀 Ball"), ("C", "📞 Call"), ("T", "🦒 Tall"), ("F", "🍂 Fall"), ("H", "🏛️ Hall")]

        render_mascot_guide(f"Tap a letter tile to spell a new rhyming word ending in {ending.upper()}!", "Chickie", "🐥")
        speak(f"Tap a letter tile to spell a new rhyming word ending in {ending.upper()}!")

        st.markdown(f"""
        <div style="background:#faf5ff; border:5px solid #a855f7; border-radius:28px; padding:22px; text-align:center; margin-bottom:18px;">
            <div style="font-size:2rem; font-weight:900; color:#6b21a8;">Ending Family: <span style="font-size:3.5rem; color:#7e22ce;">-{ending.upper()}</span></div>
        </div>
        """, unsafe_allow_html=True)

        sp_cols = st.columns(len(letters))
        for i, (l_char, desc) in enumerate(letters):
            full_word = f"{l_char.lower()}{ending}"
            with sp_cols[i]:
                if st.button(f"🔤 {l_char}\n+{ending}", key=f"wf_{l_char}_{ending}", use_container_width=True):
                    st.balloons()
                    speak(f"{l_char} plus {ending} spells {full_word}! {desc}!", "cheer")
                    track_score("Word Family", full_word)
                    st.success(f"⭐ {full_word.upper()} ({desc})")

    # 5. LETTER I-SPY
    elif active_game == "🔍 Letter I-Spy Safari":
        if "target_letter" not in st.session_state:
            st.session_state.target_letter = random.choice(["B", "M", "D", "S", "A", "T"])
            st.session_state.popped_indices = []

        t_let = st.session_state.target_letter
        render_mascot_guide(f"I spy the letter {t_let}! Tap and pop all the bubbles that match {t_let}!", "Oliver Owl", "🦉")
        speak(f"I spy the letter {t_let}! Tap and pop all the bubbles that match {t_let}!")

        st.markdown(f"""
        <div style="background:#ffffff; border:4px dashed #ec4899; border-radius:24px; padding:14px; text-align:center; font-size:1.8rem; font-weight:900; color:#db2777; margin-bottom:15px; box-shadow:0 6px 16px rgba(0,0,0,0.06);">
            🎯 TARGET: <span style="font-size:3.5rem; color:#be185d;">{t_let}</span> or <span style="font-size:3.5rem; color:#be185d;">{t_let.lower()}</span>
        </div>
        """, unsafe_allow_html=True)

        grid_letters = [t_let, t_let.lower(), "m", "P", t_let, "d", "c", t_let.lower(), "r", "O", t_let, "w", "e", t_let.lower(), "k", "L"]
        cols_grid = st.columns(4)

        for idx, char in enumerate(grid_letters):
            with cols_grid[idx % 4]:
                if idx in st.session_state.popped_indices:
                    st.markdown("""
                    <div style="background:#f1f5f9; border:2px dashed #94a3b8; border-radius:24px; padding:16px; text-align:center; font-size:1.4rem; color:#94a3b8; font-weight:800;">
                        ✅ Popped!
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    if st.button(f"🎈 {char}", key=f"ispy_bubble_{idx}_{t_let}", use_container_width=True):
                        if char.upper() == t_let:
                            st.session_state.popped_indices.append(idx)
                            st.balloons()
                            speak(f"Pop! You found {char}!", "pop")
                            track_score("Letter I-Spy", char)
                            st.rerun()
                        else:
                            speak(f"Oops! That is the letter {char}. Look for {t_let}!", "tryagain")

        if st.button("🔄 Play with a New Target Letter!", use_container_width=True):
            st.session_state.target_letter = random.choice(["B", "M", "D", "S", "A", "T"])
            st.session_state.popped_indices = []
            st.rerun()

    # 6. SEASONS
    elif active_game == "🍁 Seasons & Nature Quest":
        season_scenes = [
            {
                "season": "Winter",
                "q": "Freezing cold weather, snowmen with carrot noses, and warm cozy mittens!",
                "correct": "Winter",
                "choices": [
                    {"name": "Winter", "img": "⛄❄️🧤", "desc": "Snowman & ice skates"},
                    {"name": "Summer", "img": "☀️🏖️🍉", "desc": "Beach & swimming"},
                    {"name": "Spring", "img": "🌸🌱🌧️", "desc": "Rain boots & flowers"},
                    {"name": "Fall / Autumn", "img": "🍂🍁🎃", "desc": "Leaves & pumpkins"}
                ]
            },
            {
                "season": "Summer",
                "q": "Super hot and sunny! Splashing in the swimming pool and eating cold watermelon!",
                "correct": "Summer",
                "choices": [
                    {"name": "Summer", "img": "☀️🏖️🍉", "desc": "Beach & swimming"},
                    {"name": "Winter", "img": "⛄❄️🧤", "desc": "Snowman & mittens"},
                    {"name": "Spring", "img": "🌸🌱🌧️", "desc": "Flowers & rain"},
                    {"name": "Fall / Autumn", "img": "🍂🍁🎃", "desc": "Leaves & pumpkins"}
                ]
            }
        ]
        if "s_idx" not in st.session_state: st.session_state.s_idx = 0
        curr_sc = season_scenes[st.session_state.s_idx % len(season_scenes)]

        render_mascot_guide(f"Look at the weather clue: {curr_sc['q']} Which season is it?", "Bella", "🐶")
        speak(f"Look at the weather clue: {curr_sc['q']} Which season is it?")

        sc_top = st.columns(2)
        sc_bot = st.columns(2)
        sc_all = [sc_top[0], sc_top[1], sc_bot[0], sc_bot[1]]

        for i, choice in enumerate(curr_sc["choices"]):
            with sc_all[i]:
                st.markdown(f"""
                <div style="background:#ffffff; border:3.5px solid #86efac; border-radius:24px; padding:16px; text-align:center; margin-bottom:8px; box-shadow:0 6px 14px rgba(0,0,0,0.06);">
                    <div style="font-size:3.5rem; margin-bottom:4px;">{choice['img']}</div>
                    <div style="font-size:1.4rem; font-weight:900; color:#14532d;">{choice['name']}</div>
                    <div style="font-size:1.05rem; font-weight:700; color:#475569;">{choice['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"👉 Select {choice['name']}", key=f"btn_season_{choice['name']}_{st.session_state.s_idx}", use_container_width=True):
                    if choice["name"] == curr_sc["correct"]:
                        st.balloons()
                        speak(f"Correct! That happens in {choice['name']}!", "cheer")
                        track_score("Seasons", choice["name"])
                        st.session_state.s_idx += 1
                        st.rerun()
                    else:
                        speak("Look at the picture clues again!", "tryagain")

    # 7. COOL MATH
    elif active_game == "➕ Cool Math (10 and Under)":
        if "km_math" not in st.session_state:
            is_add = random.choice([True, False])
            if is_add:
                a = random.randint(1, 5)
                b = random.randint(1, 4)
                st.session_state.km_math = {"a": a, "b": b, "op": "+", "ans": a + b}
            else:
                total = random.randint(3, 8)
                sub = random.randint(1, total - 1)
                st.session_state.km_math = {"a": total, "b": sub, "op": "-", "ans": total - sub}

        m = st.session_state.km_math
        render_mascot_guide(f"What is {m['a']} {m['op']} {m['b']}? Count the apples to solve it!", "Chickie", "🐥")
        speak(f"What is {m['a']} {m['op']} {m['b']}? Count the apples to solve it!")

        st.markdown(f"""
        <div style="background:#ffffff; border:5px solid #a855f7; border-radius:28px; padding:20px; text-align:center; font-size:4.2rem; font-weight:900; color:#7e22ce; margin-bottom:15px; box-shadow:0 8px 20px rgba(0,0,0,0.08);">
            {m['a']} {m['op']} {m['b']} = ?
        </div>
        """, unsafe_allow_html=True)

        if m["op"] == "+":
            st.markdown(f"<div style='text-align:center; font-size:2.2rem; margin-bottom:20px;'>{'🍎 ' * m['a']} + {'🍏 ' * m['b']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:center; font-size:2.2rem; margin-bottom:20px;'>{'🍎 ' * m['ans']} {'❌ ' * m['b']}</div>", unsafe_allow_html=True)

        opts = list(set([m["ans"], m["ans"] + 1, max(1, m["ans"] - 1)]))
        random.shuffle(opts)

        mcols = st.columns(len(opts))
        for i, opt in enumerate(opts):
            with mcols[i]:
                if st.button(f"🔢 {opt}", key=f"km_{opt}", use_container_width=True):
                    if opt == m["ans"]:
                        st.balloons()
                        speak(f"Yes! {m['a']} {m['op']} {m['b']} is {m['ans']}!", "cheer")
                        track_score("Cool Math", f"{m['a']} {m['op']} {m['b']} = {m['ans']}")
                        del st.session_state.km_math
                        st.rerun()
                    else:
                        speak("Count the apples one by one and try again!", "tryagain")

    # 8. PARENT PORTAL
    elif active_game == "📊 Parent Progress Portal":
        today_str = datetime.now().strftime("%A, %B %d, %Y")
        st.markdown(f"### 🗓️ Practice Telemetry for: **{curr_user}** ({today_str})")

        d_log = u_data["daily_log"].get(today_str, {"attempts": 0, "correct": 0, "activities": []})
        attempts = d_log["attempts"]
        correct = d_log["correct"]
        acc = int((correct / attempts) * 100) if attempts > 0 else 100

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Exercises Practiced", f"{attempts}")
        m2.metric("Correct Answers", f"{correct}")
        m3.metric("Daily Accuracy", f"{acc}%")
        m4.metric("i-Ready Readiness", "On Track ⭐" if acc >= 80 else "Practicing")

        st.markdown("---")
        if st.button("🔄 Switch Profile / Back to Profile Selector"):
            st.session_state.screen = "profile_picker"
            st.rerun()

        st.markdown("#### 📝 Detailed Practice Log:")
        if d_log["activities"]:
            for act in reversed(d_log["activities"]):
                st.write(f"• **{act['time']}** — [{act['activity']}] {act['detail']} — **{act['result']}**")
        else:
            st.info("No activities logged yet today.")
