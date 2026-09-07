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

# --- KID ARCADE / HATCH THEMED STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700;800&family=Quicksand:wght@600;700;800&display=swap');

    .stApp {
        background: linear-gradient(180deg, #38bdf8 0%, #6ee7b7 55%, #fef08a 100%) !important;
        font-family: 'Fredoka', 'Quicksand', cursive, sans-serif !important;
    }

    /* High-contrast dropdown cards */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 3.5px solid #0284c7 !important;
        border-radius: 22px !important;
        color: #0f172a !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        box-shadow: 0 6px 0 rgba(0,0,0,0.12) !important;
    }
    div[data-baseweb="select"] * {
        color: #0f172a !important;
        font-weight: 800 !important;
    }
    label[data-testid="stWidgetLabel"] p {
        color: #0c4a6e !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        text-shadow: 0 1px 2px rgba(255,255,255,0.8);
    }

    /* Big Tactile Touch Buttons for iPad */
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

    .hud-chip {
        background: #fef08a;
        color: #854d0e;
        padding: 8px 20px;
        border-radius: 22px;
        font-size: 1.3rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 2.5px solid #facc15;
    }

    .instruction-card {
        background: #ffffff;
        border-radius: 26px;
        padding: 14px 20px;
        border: 3.5px solid #60a5fa;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        margin-bottom: 16px;
        text-align: center;
    }

    .choice-card-img {
        background: #ffffff;
        border: 3.5px solid #93c5fd;
        border-radius: 24px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- WEB SPEECH SYNTHESIS ENGINE ---
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
                snd.volume = 0.5;
                snd.play().catch(e => console.log(e));
            }} catch(e) {{}}

            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                let utter = new SpeechSynthesisUtterance("{clean_text}");
                utter.rate = 0.82;
                utter.pitch = 1.25;
                window.speechSynthesis.speak(utter);
            }}
        }})();
    </script>
    """
    components.html(js, height=0)

# --- FINGER TRACING PAD (FIXED: ONLY DRAWS ON ACTIVE MOUSE CLICK / FINGER TOUCH DOWN) ---
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
                return {{
                    x: e.touches[0].clientX - rect.left,
                    y: e.touches[0].clientY - rect.top
                }};
            }}
            return {{
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            }};
        }}

        function handlePointerDown(e) {{
            // Mouse button check: Only draw on primary left-click
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

        function handlePointerMove(e) {{
            if (!isPressing) return;
            e.preventDefault();
            // Mouse safety fallback: if buttons are 0, user released mouse outside
            if (e.type === 'mousemove' && e.buttons === 0) {{
                isPressing = false;
                ctx.beginPath();
                return;
            }}
            const pt = getCoordinates(e);
            ctx.lineTo(pt.x, pt.y);
            ctx.stroke();
        }}

        function handlePointerUp(e) {{
            if (isPressing) {{
                isPressing = false;
                ctx.beginPath();
            }}
        }}

        // Mouse listeners
        cvs.addEventListener('mousedown', handlePointerDown);
        cvs.addEventListener('mousemove', handlePointerMove);
        window.addEventListener('mouseup', handlePointerUp);

        // Touch listeners for iPad
        cvs.addEventListener('touchstart', handlePointerDown, {{ passive: false }});
        cvs.addEventListener('touchmove', handlePointerMove, {{ passive: false }});
        window.addEventListener('touchend', handlePointerUp, {{ passive: false }});
        window.addEventListener('touchcancel', handlePointerUp, {{ passive: false }});

        function clearPad() {{
            ctx.clearRect(0, 0, cvs.width, cvs.height);
            document.getElementById('cMsg').innerText = '';
        }}

        function checkTrace() {{
            confetti({{ particleCount: 90, spread: 75, origin: {{ y: 0.75 }} }});
            document.getElementById('cMsg').innerText = "🌟 WOW Gracyn! Great handwriting!";
            let a = new Audio('https://cdn.freesound.org/previews/270/270304_5123851-lq.mp3');
            a.play();
        }}
    </script>
    """
    components.html(html, height=330)

# --- INSTANT ZERO-LATENCY SPEECH RECOGNITION (NO SPOILERS) ---
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
            
            if (!SpeechRec) {{ 
                res.innerHTML = "<span style='color:red;'>Please use Safari or Chrome!</span>"; 
                return; 
            }}

            answered = false;
            rec = new SpeechRec();
            rec.lang = 'en-US';
            rec.continuous = false;
            rec.interimResults = true;

            btn.innerText = "👂 Listening to Gracyn...";
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
                if (target === "see" && (heard.includes("sea") || heard.includes("c"))) match = true;
                if (target === "be" && (heard.includes("bee") || heard.includes("b"))) match = true;

                if (match) {{
                    answered = true;
                    try {{ rec.stop(); }} catch(err) {{}}
                    
                    confetti({{ particleCount: 120, spread: 80, origin: {{ y: 0.7 }} }});
                    let a = new Audio('https://cdn.freesound.org/previews/270/270304_5123851-lq.mp3');
                    a.play();

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

            rec.onerror = () => {{
                btn.innerText = '🎙️ Tap to Say Your Word';
                btn.style.background = "#f97316";
                if (!answered) {{
                    res.innerHTML = "<span style='color:#ea580c;'>Speak loud and clear!</span>";
                }}
            }};

            rec.start();
        }}
    </script>
    """
    components.html(html, height=125)

# --- EXACT CURRICULUM SIGHT WORD REPOSITORY ---
SIGHT_WORD_LISTS = {
    "⭐ List 1 (12 Words)": ["a", "at", "do", "was", "the", "as", "I", "you", "am", "to", "is", "an"],
    "🌟 List 2 (12 Words)": ["man", "did", "of", "your", "in", "sit", "for", "said", "it", "can", "from", "all"]
}

# --- SUPABASE & DAILY TELEMETRY TRACKER ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        pass

def track_performance(activity, is_correct, detail=""):
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    if "daily_log" not in st.session_state:
        st.session_state.daily_log = {}

    if today_str not in st.session_state.daily_log:
        st.session_state.daily_log[today_str] = {"attempts": 0, "correct": 0, "activities": []}

    st.session_state.daily_log[today_str]["attempts"] += 1
    if is_correct:
        st.session_state.daily_log[today_str]["correct"] += 1
    st.session_state.daily_log[today_str]["activities"].append({
        "time": datetime.now().strftime("%I:%M %p"),
        "activity": activity,
        "result": "Passed" if is_correct else "Reviewing",
        "detail": detail
    })

    if supabase:
        try:
            supabase.table("student_milestones").insert({
                "student_name": "Gracyn",
                "date_stamp": today_str,
                "activity_type": activity,
                "action_result": "Passed" if is_correct else "Reviewing",
                "detail": detail,
                "coins": st.session_state.coins,
                "stars": st.session_state.stars
            }).execute()
        except Exception:
            pass

# --- SESSION STATE INITIALIZATION ---
if "stars" not in st.session_state: st.session_state.stars = 0
if "coins" not in st.session_state: st.session_state.coins = 50
if "streak" not in st.session_state: st.session_state.streak = 0
if "current_game" not in st.session_state: st.session_state.current_game = "📖 Sight Words"
if "selected_sw_list" not in st.session_state: st.session_state.selected_sw_list = "⭐ List 1 (12 Words)"
if "sw_score_count" not in st.session_state: st.session_state.sw_score_count = 0
if "trigger_treasure" not in st.session_state: st.session_state.trigger_treasure = False

# Avatar State
if "av_head" not in st.session_state: st.session_state.av_head = "👑"
if "av_pet" not in st.session_state: st.session_state.av_pet = "🐥"
if "av_bg" not in st.session_state: st.session_state.av_bg = "#ecfeff"

def award_score(activity, detail, points=10, stars=1):
    st.session_state.coins += points
    st.session_state.stars += stars
    st.session_state.streak += 1
    track_performance(activity, True, detail)

# --- TOP HUD RIBBON ---
hud_c1, hud_c2, hud_c3 = st.columns([1.8, 2.2, 1.4])
with hud_c1:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="font-size:3.2rem; background:{st.session_state.av_bg}; border-radius:50%; border:3.5px solid #38bdf8; width:72px; height:72px; display:flex; align-items:center; justify-content:center; position:relative; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
            {st.session_state.av_head}
            <span style="position:absolute; bottom:-6px; right:-6px; font-size:1.6rem;">{st.session_state.av_pet}</span>
        </div>
        <div>
            <b style="font-size:1.4rem; color:#0f172a;">Gracyn's Quest</b><br>
            <span style="color:#0284c7; font-weight:800; font-size:1.05rem;">Kindergarten Superstar ⭐</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hud_c2:
    progress_val = min(1.0, (st.session_state.sw_score_count % 12) / 6.0) if st.session_state.sw_score_count <= 6 else min(1.0, (st.session_state.sw_score_count % 12) / 12.0)
    st.progress(progress_val)
    st.markdown(f"<div style='text-align:center; font-weight:800; color:#0369a1;'>🎁 {st.session_state.sw_score_count % 6}/6 Words to Treasure Box! (Streak: 🔥 {st.session_state.streak})</div>", unsafe_allow_html=True)

with hud_c3:
    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='hud-chip'>🪙 {st.session_state.coins}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='hud-chip'>⭐ {st.session_state.stars}</div>", unsafe_allow_html=True)

# --- TREASURE BOX POPUP MODAL (6-WORD MILESTONE) ---
if st.session_state.trigger_treasure:
    st.markdown("""
    <div style="background:#fffbeb; border:6px dashed #f59e0b; border-radius:32px; padding:24px; text-align:center; margin-bottom:25px; box-shadow:0 12px 30px rgba(0,0,0,0.15);">
        <div style="font-size:3.5rem;">🎉🎁👑</div>
        <h1 style="color:#b45309; font-size:2.4rem; margin-bottom:6px;">TREASURE BOX UNLOCKED!</h1>
        <p style="font-size:1.35rem; color:#78350f; font-weight:700;">Amazing job Gracyn! You mastered 6 words! Pick a prize to dress up your avatar, then we'll finish your list!</p>
    </div>
    """, unsafe_allow_html=True)

    speak("Gracyn! You did it! You mastered six words! Pick a prize from the treasure box to dress up your avatar!", "tada")

    tab_hat, tab_pet = st.tabs(["👑 Hats & Crowns", "🐾 Pet Buddies"])
    with tab_hat:
        hcols = st.columns(4)
        for i, h in enumerate(["👑 Crown", "🎀 Pink Bow", "🎓 Scholar Cap", "🦄 Unicorn", "🌸 Blossom", "🤠 Cowgirl", "🦸 Hero Mask", "🎩 Magician"]):
            sym = h.split()[0]
            with hcols[i % 4]:
                if st.button(h, key=f"p_{sym}", use_container_width=True):
                    st.session_state.av_head = sym
                    st.session_state.trigger_treasure = False
                    st.rerun()
    with tab_pet:
        pcols = st.columns(4)
        for i, p in enumerate(["🐥 Chickie", "🐶 Puppy", "🐱 Kitty", "🐰 Bunny", "🐼 Panda", "🦄 Sparkle", "🐬 Dolphin", "🦊 Fox"]):
            sym = p.split()[0]
            with pcols[i % 4]:
                if st.button(p, key=f"p_{sym}", use_container_width=True):
                    st.session_state.av_pet = sym
                    st.session_state.trigger_treasure = False
                    st.rerun()
    st.stop()

# --- CARD SCAFFOLDED GAME NAVIGATION ---
st.markdown("""
<div class="instruction-card">
    <span style="font-size:1.3rem; font-weight:800; color:#0369a1;">🎮 Choose Your Learning Adventure Station:</span>
</div>
""", unsafe_allow_html=True)

game_modes = [
    "📖 Sight Words",
    "📚 Parts of a Book",
    "🕵️ Number Detective (18 & Beyond)",
    "🔍 Letter I-Spy Safari",
    "🍁 Seasons & Nature Quest",
    "➕ Cool Math (10 and Under)",
    "📊 Parent Progress Portal"
]
active_game = st.selectbox("", game_modes, index=game_modes.index(st.session_state.current_game), label_visibility="collapsed")
if active_game != st.session_state.current_game:
    st.session_state.current_game = active_game
    st.rerun()

# ==========================================
# 1. SIGHT WORDS (INDEPENDENT READING - NO SPOILERS)
# ==========================================
if active_game == "📖 Sight Words":
    col_title, col_audio = st.columns([3, 1.2])
    with col_title:
        st.markdown("""
        <div style="background:#ffffff; border-radius:22px; padding:12px 20px; border:3.5px solid #38bdf8; box-shadow:0 6px 16px rgba(0,0,0,0.06);">
            <div style="font-size:1.6rem; font-weight:900; color:#0284c7;">📖 Sight Word Explorer</div>
            <div style="font-size:1.05rem; font-weight:700; color:#475569;">1. Read the word  •  2. Tap orange button to say it  •  3. Trace and tap green button!</div>
        </div>
        """, unsafe_allow_html=True)
    with col_audio:
        if st.button("🔊 Hear Directions", use_container_width=True):
            speak("Hey Gracyn! Read this word on your card. Tap the orange button to say your word, then trace it with your finger and tap the green button when you're done!")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

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
        picked = st.selectbox(
            "Target Word",
            active_bank,
            index=active_bank.index(st.session_state.current_sw),
            label_visibility="collapsed"
        )
        if picked != st.session_state.current_sw:
            st.session_state.current_sw = picked
            st.rerun()

    word = st.session_state.current_sw

    if "last_sw_spoken" not in st.session_state or st.session_state.last_sw_spoken != word:
        speak("Read this word! Tap the orange button to say your word into the microphone, then trace it with your finger and tap the green button!")
        st.session_state.last_sw_spoken = word

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

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
                st.session_state.sw_score_count += 1
                award_score("Sight Words", f"Mastered {word}")
                if st.session_state.sw_score_count % 6 == 0:
                    st.session_state.trigger_treasure = True
                curr_i = active_bank.index(word)
                st.session_state.current_sw = active_bank[(curr_i + 1) % len(active_bank)]
                st.rerun()
        with b2:
            if st.button("➡️ Next Word 🎲", use_container_width=True):
                rem = [w for w in active_bank if w != word]
                st.session_state.current_sw = random.choice(rem) if rem else word
                st.rerun()

# ==========================================
# 2. VISUAL PARTS OF A BOOK (WITH PICTURE CHOICES)
# ==========================================
elif active_game == "📚 Parts of a Book":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#1e40af;">📚 Interactive Book Detective</div>
        <div style="font-size:1.1rem; font-weight:700; color:#475569;">Look at where the yellow bouncy arrow points, look at the picture choices, and tap the right answer!</div>
    </div>
    """, unsafe_allow_html=True)

    book_questions = [
        {
            "target": "Front Cover", "highlight": "cover",
            "q": "Look at the front of the book! What do we call this protective front part?",
            "wrong_exp": "The front cover protects the book and welcomes you to the story! Look for the Front Cover card.",
            "correct": "Front Cover",
            "opts": [
                {"name": "Front Cover", "img": "📕", "sub": "Whole Front Cover with Picture"},
                {"name": "The Spine", "img": "📏", "sub": "Side Edge Backbone"},
                {"name": "Back Cover", "img": "📘", "sub": "Back with Barcode"},
                {"name": "Page Numbers", "img": "📄", "sub": "Bottom Corner Numbers"}
            ]
        },
        {
            "target": "Title", "highlight": "title",
            "q": "The yellow arrow is pointing to THE BRAVE PUPPY. What is the name of a book called?",
            "wrong_exp": "The title is the big name of the story! Look for The Title card.",
            "correct": "The Title",
            "opts": [
                {"name": "The Title", "img": "🏷️", "sub": "Name of the Book"},
                {"name": "The Author", "img": "✍️", "sub": "Writer of Words"},
                {"name": "The Spine", "img": "📏", "sub": "Side Edge Backbone"},
                {"name": "The Illustrator", "img": "🎨", "sub": "Picture Painter"}
            ]
        },
        {
            "target": "Author", "highlight": "author",
            "q": "The arrow points to By Raeven Brown. Who writes the words in the book?",
            "wrong_exp": "The author is the person who writes all the words! Look for The Author card.",
            "correct": "The Author",
            "opts": [
                {"name": "The Author", "img": "✍️", "sub": "Writes the Words"},
                {"name": "The Illustrator", "img": "🎨", "sub": "Draws Pictures"},
                {"name": "Front Cover", "img": "📕", "sub": "Front of Book"},
                {"name": "Page Numbers", "img": "📄", "sub": "Bottom Corner Numbers"}
            ]
        },
        {
            "target": "Illustrator", "highlight": "illustrator",
            "q": "The arrow points to Art by Gracyn. Who draws all the colorful pictures in the book?",
            "wrong_exp": "The illustrator draws all the beautiful pictures! Look for The Illustrator card.",
            "correct": "The Illustrator",
            "opts": [
                {"name": "The Illustrator", "img": "🎨", "sub": "Draws Pictures"},
                {"name": "The Author", "img": "✍️", "sub": "Writes Words"},
                {"name": "The Title", "img": "🏷️", "sub": "Name of the Book"},
                {"name": "The Spine", "img": "📏", "sub": "Side Edge Backbone"}
            ]
        },
        {
            "target": "Spine", "highlight": "spine",
            "q": "The yellow arrow points to the side edge. What holds all the pages together like a backbone?",
            "wrong_exp": "The spine holds the pages tightly together like your backbone! Look for The Spine card.",
            "correct": "The Spine",
            "opts": [
                {"name": "The Spine", "img": "📏", "sub": "Holds Pages Together"},
                {"name": "Front Cover", "img": "📕", "sub": "Protects Front"},
                {"name": "Back Cover", "img": "📘", "sub": "Back with Barcode"},
                {"name": "The Title", "img": "🏷️", "sub": "Name of the Book"}
            ]
        }
    ]

    if "bq_idx" not in st.session_state: st.session_state.bq_idx = 0
    curr_q = book_questions[st.session_state.bq_idx % len(book_questions)]

    if "last_bq_spoken" not in st.session_state or st.session_state.last_bq_spoken != curr_q["q"]:
        speak(f"Gracyn! {curr_q['q']}")
        st.session_state.last_bq_spoken = curr_q["q"]

    t_key = curr_q["highlight"]
    html_book = f"""
    <div style="display:flex; justify-content:center; align-items:center; margin:10px 0 20px 0;">
        <div style="display:flex; width:380px; height:280px; box-shadow:0 16px 30px rgba(0,0,0,0.25); border-radius:12px 24px 24px 12px; position:relative;">
            <div style="width:50px; background:linear-gradient(90deg, #1e3a8a, #3b82f6); border-radius:12px 0 0 12px; color:#fff; writing-mode:vertical-rl; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.1rem; letter-spacing:4px; border:{'4px solid #facc15' if t_key == 'spine' else 'none'};">
                {'<span style="position:absolute; left:-55px; font-size:3rem;">👉</span>' if t_key == 'spine' else ''}
                SPINE
            </div>
            <div style="flex:1; background:linear-gradient(135deg, #60a5fa, #93c5fd); border-radius:0 20px 20px 0; padding:16px; display:flex; flex-direction:column; justify-content:space-between; align-items:center; border:{'5px solid #facc15' if t_key == 'cover' else 'none'};">
                {'<span style="position:absolute; top:-50px; font-size:3rem;">👇</span>' if t_key == 'cover' else ''}
                <div style="background:#fff; border:{'4px solid #facc15' if t_key == 'title' else '2px solid #2563eb'}; border-radius:16px; padding:6px 14px; font-size:1.35rem; font-weight:900; color:#1e3a8a;">
                    {'<span style="position:absolute; right:15px; font-size:2.8rem;">👈</span>' if t_key == 'title' else ''}
                    📖 THE BRAVE PUPPY
                </div>
                <div style="font-size:3.8rem;">🐶🐾</div>
                <div style="font-size:1.05rem; font-weight:800; color:#0f172a; background:{'#fef08a' if t_key == 'author' else '#ffffffcc'}; border-radius:12px; padding:4px 12px; border:{'3px solid #f59e0b' if t_key == 'author' else 'none'};">
                    {'<span style="position:absolute; left:60px; font-size:2.6rem;">👉</span>' if t_key == 'author' else ''}
                    ✍️ By Raeven Brown
                </div>
                <div style="font-size:1rem; font-weight:800; color:#0f172a; background:{'#fef08a' if t_key == 'illustrator' else '#ffffffcc'}; border-radius:12px; padding:4px 12px; border:{'3px solid #f59e0b' if t_key == 'illustrator' else 'none'};">
                    {'<span style="position:absolute; right:20px; font-size:2.6rem;">👈</span>' if t_key == 'illustrator' else ''}
                    🎨 Art by Gracyn
                </div>
            </div>
        </div>
    </div>
    """
    components.html(html_book, height=310)

    st.markdown(f"""
    <div style="background:#ffffff; border:4px solid #3b82f6; border-radius:24px; padding:18px; text-align:center; font-size:1.6rem; font-weight:800; color:#1e40af; margin-bottom:18px; box-shadow:0 8px 20px rgba(0,0,0,0.08);">
        ❓ {curr_q['q']}
    </div>
    """, unsafe_allow_html=True)

    # 4 Visual Picture Choices with Illustrated Cards
    bcols_top = st.columns(2)
    bcols_bot = st.columns(2)
    all_bcols = [bcols_top[0], bcols_top[1], bcols_bot[0], bcols_bot[1]]

    for i, choice in enumerate(curr_q["opts"]):
        with all_bcols[i]:
            st.markdown(f"""
            <div class="choice-card-img">
                <div style="font-size:3.5rem; margin-bottom:4px;">{choice['img']}</div>
                <div style="font-size:1.35rem; font-weight:900; color:#0f172a;">{choice['name']}</div>
                <div style="font-size:1.05rem; font-weight:700; color:#64748b;">{choice['sub']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"👉 Select {choice['name']}", key=f"bk_opt_{choice['name']}_{st.session_state.bq_idx}", use_container_width=True):
                if choice["name"] == curr_q["correct"]:
                    st.balloons()
                    speak(f"Yes! Awesome job Gracyn! That is {choice['name']}!", "cheer")
                    award_score("Parts of a Book", f"Correct on {choice['name']}")
                    st.session_state.bq_idx += 1
                    st.rerun()
                else:
                    speak(f"Not quite. {curr_q['wrong_exp']}", "tryagain")
                    track_performance("Parts of a Book", False, f"Chose {choice['name']}")

# ==========================================
# 3. NUMBER DETECTIVE: 18 & BEYOND
# ==========================================
elif active_game == "🕵️ Number Detective (18 & Beyond)":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#b45309;">🕵️ Number Detective: Target 18!</div>
        <div style="font-size:1.1rem; font-weight:700; color:#475569;">Find and tap the pictures that show EXACTLY 18!</div>
    </div>
    """, unsafe_allow_html=True)

    if "last_num_spoken" not in st.session_state:
        speak("Gracyn! We are hunting for the number 18! Look at the jelly beans, tallies, and blocks. Tap the pictures that show 18!")
        st.session_state.last_num_spoken = True

    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    with c1:
        st.markdown("""
        <div style="background:#ffffff; border:4px solid #38bdf8; border-radius:22px; padding:16px; text-align:center; box-shadow:0 6px 16px rgba(0,0,0,0.06);">
            <b style="font-size:1.3rem; color:#0369a1;">🍬 Jelly Bean Jars:</b><br>
            <div style="background:#e0f2fe; border-radius:18px; padding:12px; margin:8px 0; font-size:1.4rem;">
                Jar 1: 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 (10 Beans)<br>
                Jar 2: 🟢🟢🟢🟢🟢🟢🟢🟢 (8 Beans)
            </div>
            <b style="font-size:1.2rem; color:#0284c7;">10 Beans + 8 Beans</b>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✅ Yes! This is 18 Beans!", key="btn_beans_18", use_container_width=True):
            st.balloons()
            speak("Yes! Ten beans plus eight beans equals 18!", "cheer")
            award_score("Number Detective", "10+8 Beans = 18")

    with c2:
        st.markdown("""
        <div style="background:#ffffff; border:4px solid #38bdf8; border-radius:22px; padding:16px; text-align:center; box-shadow:0 6px 16px rgba(0,0,0,0.06);">
            <b style="font-size:1.3rem; color:#0369a1;">🟧 Base-Ten Tower & Cubes:</b><br>
            <div style="background:#e0f2fe; border-radius:18px; padding:12px; margin:8px 0; font-size:1.4rem;">
                🟦 1 Ten-Stick (10)<br>
                🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟩 (8 Ones)
            </div>
            <b style="font-size:1.2rem; color:#0284c7;">1 Ten and 8 Ones</b>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✅ Yes! This is 18!", key="btn_base10_18", use_container_width=True):
            st.balloons()
            speak("Super! One ten-rod and eight ones makes 18!", "cheer")
            award_score("Number Detective", "Base Ten 18")

    with c3:
        st.markdown("""
        <div style="background:#ffffff; border:4px solid #f87171; border-radius:22px; padding:16px; text-align:center; box-shadow:0 6px 16px rgba(0,0,0,0.06);">
            <b style="font-size:1.3rem; color:#dc2626;">🍪 Cookie Jar:</b><br>
            <div style="background:#fee2e2; border-radius:18px; padding:12px; margin:8px 0; font-size:1.4rem;">
                🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪 (10)<br>
                🍪🍪🍪🍪 (4)
            </div>
            <b style="font-size:1.2rem; color:#dc2626;">10 Cookies + 4 Cookies</b>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Is this 18? 🤔", key="btn_cookies_14", use_container_width=True):
            speak("Count carefully Gracyn! Ten plus four is 14, not 18!", "tryagain")
            track_performance("Number Detective", False, "Chose 14 instead of 18")

    with c4:
        st.markdown("""
        <div style="background:#ffffff; border:4px solid #38bdf8; border-radius:22px; padding:16px; text-align:center; box-shadow:0 6px 16px rgba(0,0,0,0.06);">
            <b style="font-size:1.3rem; color:#0369a1;">🥢 Wooden Tallies:</b><br>
            <div style="background:#e0f2fe; border-radius:18px; padding:12px; margin:8px 0; font-size:1.6rem; letter-spacing:4px;">
                卌 卌 卌 |||<br>
                <span style="font-size:1.1rem; color:#475569;">(5 + 5 + 5 + 3)</span>
            </div>
            <b style="font-size:1.2rem; color:#0284c7;">15 + 3 Tallies</b>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✅ Yes! This is 18 Tallies!", key="btn_tally_18", use_container_width=True):
            st.balloons()
            speak("Bingo! Fifteen plus three tallies is 18!", "cheer")
            award_score("Number Detective", "Tallies 18")

# ==========================================
# 4. LETTER I-SPY: 16-BUBBLE SAFARI GRID
# ==========================================
elif active_game == "🔍 Letter I-Spy Safari":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#db2777;">🔍 Letter I-Spy Safari Grid</div>
        <div style="font-size:1.1rem; font-weight:700; color:#475569;">Find and pop all the bubbles matching our target letter!</div>
    </div>
    """, unsafe_allow_html=True)

    if "target_letter" not in st.session_state:
        st.session_state.target_letter = random.choice(["B", "M", "D", "S", "A", "T"])

    t_let = st.session_state.target_letter
    speak(f"Gracyn! I spy the letter {t_let}! Look at the safari bubbles and pop all the {t_let}'s you see!")

    st.markdown(f"""
    <div style="background:#ffffff; border:4px dashed #ec4899; border-radius:24px; padding:14px; text-align:center; font-size:1.8rem; font-weight:900; color:#db2777; margin-bottom:15px; box-shadow:0 6px 16px rgba(0,0,0,0.06);">
        🎯 I-SPY TARGET: <span style="font-size:3.5rem; color:#be185d;">{t_let}</span> or <span style="font-size:3.5rem; color:#be185d;">{t_let.lower()}</span>
    </div>
    """, unsafe_allow_html=True)

    grid_letters = [t_let, t_let.lower(), "m", "P", t_let, "d", "c", t_let.lower(), "r", "O", t_let, "w", "e", t_let.lower(), "k", "L"]
    cols_grid = st.columns(4)
    for idx, char in enumerate(grid_letters):
        with cols_grid[idx % 4]:
            if st.button(f"🎈 {char}", key=f"ispy_bubble_{idx}_{t_let}", use_container_width=True):
                if char.upper() == t_let:
                    st.balloons()
                    speak(f"You popped a {char}! Great eye!", "pop")
                    award_score("Letter I-Spy", f"Found {char}")
                else:
                    speak(f"Oops! That is the letter {char}. Look for {t_let}!", "tryagain")

    if st.button("🔄 Play with a New Letter!", use_container_width=True):
        st.session_state.target_letter = random.choice(["B", "M", "D", "S", "A", "T"])
        st.rerun()

# ==========================================
# 5. SEASONS WEATHER-CASTER
# ==========================================
elif active_game == "🍁 Seasons & Nature Quest":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#166534;">🍂 Seasons Weather-Caster</div>
        <div style="font-size:1.1rem; font-weight:700; color:#475569;">Look at the picture clues and tap the right season!</div>
    </div>
    """, unsafe_allow_html=True)

    season_db = [
        {
            "season": "Fall / Autumn",
            "img": "🍂🍁🎃🍎🧥",
            "clue": "Leaves turn bright orange, red, and yellow and fall from trees! We pick pumpkins and wear cozy sweaters!",
            "opts": ["Fall / Autumn", "Summer", "Spring", "Winter"]
        },
        {
            "season": "Winter",
            "img": "❄️⛄🧤🧣🧊",
            "clue": "It is freezing cold outside! Snowflakes fall and we build cute snowmen with hats and warm mittens!",
            "opts": ["Winter", "Spring", "Summer", "Fall / Autumn"]
        },
        {
            "season": "Spring",
            "img": "🌸🌷🌱🐣🌧️",
            "clue": "April showers bring pretty flowers! Green grass grows and cute baby birds hatch in their nests!",
            "opts": ["Spring", "Winter", "Fall / Autumn", "Summer"]
        },
        {
            "season": "Summer",
            "img": "☀️🏖️🍉🕶️🏊‍♀️",
            "clue": "It is hot and sunny! We jump in the swimming pool, wear sunglasses, and eat sweet watermelon!",
            "opts": ["Summer", "Winter", "Spring", "Fall / Autumn"]
        }
    ]

    if "s_idx" not in st.session_state: st.session_state.s_idx = 0
    curr_s = season_db[st.session_state.s_idx % len(season_db)]

    speak(f"Look at the picture clue: {curr_s['clue']} What season is it?")

    st.markdown(f"""
    <div style="background:#ffffff; border:4px solid #22c55e; border-radius:28px; padding:20px; text-align:center; margin-bottom:18px; box-shadow:0 8px 20px rgba(0,0,0,0.08);">
        <div style="font-size:4.8rem; margin-bottom:8px;">{curr_s['img']}</div>
        <div style="font-size:1.55rem; font-weight:800; color:#15803d;">{curr_s['clue']}</div>
    </div>
    """, unsafe_allow_html=True)

    scols = st.columns(2)
    for i, opt in enumerate(curr_s["opts"]):
        with scols[i % 2]:
            if st.button(f"🌤️ {opt}", key=f"btn_s_{opt}_{st.session_state.s_idx}", use_container_width=True):
                if opt == curr_s["season"]:
                    st.balloons()
                    speak(f"Correct! That happens in {opt}!", "cheer")
                    award_score("Seasons Quest", opt)
                    st.session_state.s_idx += 1
                    st.rerun()
                else:
                    speak("Look at the picture clues again! Think about the weather!", "tryagain")

# ==========================================
# 6. COOL MATH (10 AND UNDER)
# ==========================================
elif active_game == "➕ Cool Math (10 and Under)":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#7e22ce;">🧮 Cool Math: 10 and Under!</div>
        <div style="font-size:1.1rem; font-weight:700; color:#475569;">Count the delicious apples and solve the problem!</div>
    </div>
    """, unsafe_allow_html=True)

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
    speak(f"Gracyn! What is {m['a']} {m['op']} {m['b']}? Count the apples on the screen!")

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
                    award_score("Cool Math", f"{m['a']} {m['op']} {m['b']} = {m['ans']}")
                    del st.session_state.km_math
                    st.rerun()
                else:
                    speak("Count the apples one by one and try again!", "tryagain")

# ==========================================
# 7. PARENT PROGRESS PORTAL
# ==========================================
elif active_game == "📊 Parent Progress Portal":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#0f172a;">📊 Gracyn's Daily Learning Telemetry</div>
        <div style="font-size:1.1rem; font-weight:700; color:#475569;">Track daily scores, accuracy, and i-Ready proficiency milestones.</div>
    </div>
    """, unsafe_allow_html=True)

    today_str = datetime.now().strftime("%A, %B %d, %Y")
    st.markdown(f"### 🗓️ Report for: **{today_str}**")

    d_log = st.session_state.get("daily_log", {}).get(today_str, {"attempts": 0, "correct": 0, "activities": []})
    attempts = d_log["attempts"]
    correct = d_log["correct"]
    acc = int((correct / attempts) * 100) if attempts > 0 else 100

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Exercises Practiced", f"{attempts}")
    m2.metric("Correct Answers", f"{correct}")
    m3.metric("Daily Accuracy", f"{acc}%")
    m4.metric("i-Ready Readiness", "On Track ⭐" if acc >= 80 else "Practicing")

    st.markdown("---")
    st.markdown("#### 📝 Detailed Practice Log:")
    if d_log["activities"]:
        for act in reversed(d_log["activities"]):
            st.write(f"• **{act['time']}** — [{act['activity']}] {act['detail']} — **{act['result']}**")
    else:
        st.info("No activities logged yet today. Have Gracyn play any adventure station to begin recording!")
