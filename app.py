import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime
from supabase import create_client, Client

st.set_page_config(
    page_title="Gracyn's Hatch Learning Studio",
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

# --- DIRECT UNIVERSAL AUTOPLAY (IPAD & LAPTOP NATIVE BRIDGE) ---
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
            // 1. Play SFX
            try {{
                let snd = new Audio("{sound_url}");
                snd.volume = 0.55;
                snd.play().catch(() => {{}});
            }} catch(e) {{}}

            // 2. Cross-window SpeechSynthesis for iOS Safari & Desktop
            function runSpeech() {{
                const synth = (window.parent && window.parent.speechSynthesis) ? window.parent.speechSynthesis : window.speechSynthesis;
                if (!synth) return;
                
                try {{
                    synth.cancel();
                    if (synth.paused) synth.resume();
                }} catch(e) {{}}

                const utter = new SpeechSynthesisUtterance("{clean_text}");
                utter.rate = 0.84;
                utter.pitch = 1.25;
                utter.lang = 'en-US';

                const voices = synth.getVoices();
                if (voices && voices.length > 0) {{
                    const preferred = voices.find(v => (v.name.includes("Samantha") || v.name.includes("Victoria") || v.name.includes("Karen") || v.lang === "en-US") && !v.name.includes("Bad"));
                    if (preferred) utter.voice = preferred;
                }}

                synth.speak(utter);
            }}

            runSpeech();
            setTimeout(runSpeech, 150);
        }})();
    </script>
    """
    components.html(js, height=0)

# --- FINGER TRACING PAD (DISCRETE STROKES ONLY ON ACTIVE MOUSE/TOUCH DOWN) ---
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

        cvs.addEventListener('mousedown', handlePointerDown);
        cvs.addEventListener('mousemove', handlePointerMove);
        window.addEventListener('mouseup', handlePointerUp);

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
            a.play().catch(() => {{}});
        }}
    </script>
    """
    components.html(html, height=330)

# --- INSTANT SPEECH RECOGNITION (NO SPOILERS) ---
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

# --- SIGHT WORD REPOSITORY ---
SIGHT_WORD_LISTS = {
    "⭐ List 1 (12 Words)": ["a", "at", "do", "was", "the", "as", "I", "you", "am", "to", "is", "an"],
    "🌟 List 2 (12 Words)": ["man", "did", "of", "your", "in", "sit", "for", "said", "it", "can", "from", "all"]
}

# --- SUPABASE & TELEMETRY ---
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

# --- SESSION STATE ---
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

# --- TREASURE BOX POPUP MODAL ---
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

# --- PRIMARY NAVIGATION ---
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

# ==========================================
# 1. SIGHT WORDS (AUTOMATIC AUDIO INSTRUCTIONS - NO SPOILERS)
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
        if st.button("🔊 Hear Directions Again", use_container_width=True):
            speak("Hey Gracyn! Read this word on your card. Tap the orange button to say your word, then trace it with your finger and tap the green button when you are done!")

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

    # Automatic prompt on navigation without spoiling the word
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
# 2. PARTS OF A BOOK & STORY TIME (TEACH FIRST -> STORY RECALL -> TEST)
# ==========================================
elif active_game == "📚 Parts of a Book & Story Time":
    book_tab1, book_tab2, book_tab3 = st.tabs(["🎓 Step 1: Learn the Parts", "📖 Step 2: Read Story & Recall", "🕵️ Step 3: Detective Quiz"])

    # STEP 1: INTERACTIVE LESSON
    with book_tab1:
        st.markdown("""
        <div class="instruction-card">
            <div style="font-size:1.6rem; font-weight:900; color:#1e40af;">🎓 Lesson: What Makes a Book?</div>
            <div style="font-size:1.15rem; font-weight:700; color:#475569;">Every book has special parts! Let's explore each one:</div>
        </div>
        """, unsafe_allow_html=True)

        l_c1, l_c2 = st.columns(2)
        with l_c1:
            st.markdown("""
            <div style="background:#ffffff; border:4px solid #3b82f6; border-radius:24px; padding:16px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="font-size:2.8rem;">📕</div>
                    <div>
                        <b style="font-size:1.3rem; color:#1e3a8a;">1. The Front Cover</b><br>
                        <span style="font-size:1.05rem; color:#475569; font-weight:600;">The heavy front door that protects all the pages inside and shows you the big picture!</span>
                    </div>
                </div>
            </div>

            <div style="background:#ffffff; border:4px solid #f59e0b; border-radius:24px; padding:16px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="font-size:2.8rem;">🏷️</div>
                    <div>
                        <b style="font-size:1.3rem; color:#b45309;">2. The Title</b><br>
                        <span style="font-size:1.05rem; color:#475569; font-weight:600;">The big name of the book that tells you what the whole story is about!</span>
                    </div>
                </div>
            </div>

            <div style="background:#ffffff; border:4px solid #10b981; border-radius:24px; padding:16px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="font-size:2.8rem;">🧑‍🏫</div>
                    <div>
                        <b style="font-size:1.3rem; color:#065f46;">3. The Author</b><br>
                        <span style="font-size:1.05rem; color:#475569; font-weight:600;">The person who writes all the wonderful words and thoughts in the story!</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with l_c2:
            st.markdown("""
            <div style="background:#ffffff; border:4px solid #ec4899; border-radius:24px; padding:16px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="font-size:2.8rem;">🎨</div>
                    <div>
                        <b style="font-size:1.3rem; color:#9d174d;">4. The Illustrator</b><br>
                        <span style="font-size:1.05rem; color:#475569; font-weight:600;">The artist who paints and draws all the colorful illustrations and pictures!</span>
                    </div>
                </div>
            </div>

            <div style="background:#ffffff; border:4px solid #8b5cf6; border-radius:24px; padding:16px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="font-size:2.8rem;">📏</div>
                    <div>
                        <b style="font-size:1.3rem; color:#5b21b6;">5. The Spine</b><br>
                        <span style="font-size:1.05rem; color:#475569; font-weight:600;">The strong backbone on the side that binds and holds all the pages tightly together!</span>
                    </div>
                </div>
            </div>

            <div style="background:#ffffff; border:4px solid #64748b; border-radius:24px; padding:16px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="font-size:2.8rem;">📘</div>
                    <div>
                        <b style="font-size:1.3rem; color:#334155;">6. The Back Cover</b><br>
                        <span style="font-size:1.05rem; color:#475569; font-weight:600;">The back of the book that has the store barcode and a short summary of the story!</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🔊 Read All Lesson Parts Out Loud", use_container_width=True):
            speak("Let's learn about books! The front cover protects the book. The title is the book's name. The author writes the words. The illustrator draws the pictures. The spine holds the pages together like your backbone, and the back cover has the barcode!")

    # STEP 2: MINI STORY & RECALL
    with book_tab2:
        st.markdown("""
        <div class="instruction-card">
            <div style="font-size:1.6rem; font-weight:900; color:#0369a1;">📖 Story Time: Bella the Brave Pup</div>
            <div style="font-size:1.15rem; font-weight:700; color:#475569;">Listen to the short story and remember what happens!</div>
        </div>
        """, unsafe_allow_html=True)

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
                Written by: Raeven Brown  •  Illustrated by: Gracyn
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔊 Read Story Aloud to Gracyn", use_container_width=True):
            speak("Bella's Big Sunny Day! Once upon a time, a fluffy golden pup named Bella found a bright red balloon stuck in a tree. Bella wagged her tail, jumped with all her puppy might, and tapped the balloon with her nose! Pop! The balloon floated into the clouds and Bella made a new friend named Oliver the Owl! Written by Raeven Brown, Illustrated by Gracyn!")

        st.markdown("#### 🧠 Story Recall Check:")
        rc1, rc2 = st.columns(2)
        with rc1:
            if st.button("🐶 Who was the hero? (A) Bella the Pup", use_container_width=True):
                st.balloons()
                speak("Yes! Bella the fluffy pup was the main character!", "cheer")
                award_score("Story Recall", "Bella the pup")
        with rc2:
            if st.button("🐱 Was the hero a Kitty named Cleo?", use_container_width=True):
                speak("Think back to our story! It was about Bella the brave pup!", "tryagain")

    # STEP 3: INTERACTIVE DETECTIVE QUIZ
    with book_tab3:
        book_questions = [
            {
                "target": "Front Cover", "highlight": "cover",
                "q": "Look at the big illustrated front. What part protects the book and welcomes you in?",
                "wrong_exp": "The Front Cover is the whole front of the book! Look at the Front Cover card.",
                "correct": "Front Cover",
                "opts": [
                    {"name": "Front Cover", "icon": "📕", "desc": "Whole Front Cover with Puppy Picture"},
                    {"name": "The Spine", "icon": "📏", "desc": "Side Edge Backbone"},
                    {"name": "Back Cover", "icon": "📘", "desc": "Back of Book with Barcode"},
                    {"name": "Page Numbers", "icon": "📄", "desc": "Bottom Corner Numbers"}
                ]
            },
            {
                "target": "The Title", "highlight": "title",
                "q": "Look at the bold words at the top: THE BRAVE PUPPY. What is the name of a book called?",
                "wrong_exp": "The Title is the name of the book! Look for The Title card.",
                "correct": "The Title",
                "opts": [
                    {"name": "The Title", "icon": "🏷️", "desc": "Name of the Book at the top"},
                    {"name": "The Author", "icon": "🧑‍🏫", "desc": "The Person who writes words"},
                    {"name": "The Spine", "icon": "📏", "desc": "Side Edge Backbone"},
                    {"name": "The Illustrator", "icon": "🎨", "desc": "Draws pictures"}
                ]
            },
            {
                "target": "The Author", "highlight": "author",
                "q": "Look at 'By Raeven Brown'. Who writes all the words in the book?",
                "wrong_exp": "The Author writes all the words in the story! Look for The Author card.",
                "correct": "The Author",
                "opts": [
                    {"name": "The Author", "icon": "🧑‍🏫", "desc": "Person writing with glasses & paper"},
                    {"name": "The Illustrator", "icon": "🎨", "desc": "Artist painting with brush"},
                    {"name": "Front Cover", "icon": "📕", "desc": "Front of book"},
                    {"name": "The Spine", "icon": "📏", "desc": "Side backbone"}
                ]
            },
            {
                "target": "The Illustrator", "highlight": "illustrator",
                "q": "Look at 'Art by Gracyn'. Who draws all the colorful pictures in the book?",
                "wrong_exp": "The Illustrator paints and draws all the pictures! Look for The Illustrator card.",
                "correct": "The Illustrator",
                "opts": [
                    {"name": "The Illustrator", "icon": "🎨", "desc": "Artist with easel & paint palette"},
                    {"name": "The Author", "icon": "🧑‍🏫", "desc": "Writes the words"},
                    {"name": "Back Cover", "icon": "📘", "desc": "Back with barcode"},
                    {"name": "The Title", "icon": "🏷️", "desc": "Name of book"}
                ]
            },
            {
                "target": "The Spine", "highlight": "spine",
                "q": "Look at the side edge. What holds all the pages tightly together like your backbone?",
                "wrong_exp": "The Spine binds and holds all the pages together! Look for The Spine card.",
                "correct": "The Spine",
                "opts": [
                    {"name": "The Spine", "icon": "📏", "desc": "Side Binding Backbone"},
                    {"name": "Front Cover", "icon": "📕", "desc": "Front Cover"},
                    {"name": "Back Cover", "icon": "📘", "desc": "Back Cover with Barcode"},
                    {"name": "The Title", "icon": "🏷️", "desc": "Name of the Book"}
                ]
            }
        ]

        if "bq_idx" not in st.session_state: st.session_state.bq_idx = 0
        curr_q = book_questions[st.session_state.bq_idx % len(book_questions)]

        if "last_bq_spoken" not in st.session_state or st.session_state.last_bq_spoken != curr_q["q"]:
            speak(f"Gracyn! {curr_q['q']}")
            st.session_state.last_bq_spoken = curr_q["q"]

        # Realistic Physical Book Mockup
        t_key = curr_q["highlight"]
        html_book = f"""
        <div style="display:flex; justify-content:center; align-items:center; margin:10px 0 20px 0;">
            <div style="display:flex; width:400px; height:290px; box-shadow:0 18px 36px rgba(0,0,0,0.25); border-radius:14px 26px 26px 14px; position:relative; background:#fff;">
                <div style="width:55px; background:linear-gradient(90deg, #1e3a8a, #3b82f6); border-radius:14px 0 0 14px; color:#fff; writing-mode:vertical-rl; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.15rem; letter-spacing:4px; border:{'5px solid #facc15' if t_key == 'spine' else 'none'};">
                    {'<span style="position:absolute; left:-55px; font-size:3rem;">👉</span>' if t_key == 'spine' else ''}
                    SPINE
                </div>
                <div style="flex:1; background:linear-gradient(135deg, #60a5fa, #93c5fd); border-radius:0 22px 22px 0; padding:16px; display:flex; flex-direction:column; justify-content:space-between; align-items:center; border:{'5px solid #facc15' if t_key == 'cover' else 'none'};">
                    {'<span style="position:absolute; top:-50px; font-size:3rem;">👇</span>' if t_key == 'cover' else ''}
                    <div style="background:#fff; border:{'4px solid #facc15' if t_key == 'title' else '2px solid #2563eb'}; border-radius:16px; padding:6px 16px; font-size:1.35rem; font-weight:900; color:#1e3a8a;">
                        {'<span style="position:absolute; right:15px; font-size:2.8rem;">👈</span>' if t_key == 'title' else ''}
                        📖 THE BRAVE PUPPY
                    </div>
                    <div style="font-size:4rem;">🐶🐾</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#0f172a; background:{'#fef08a' if t_key == 'author' else '#ffffffcc'}; border-radius:12px; padding:4px 14px; border:{'3px solid #f59e0b' if t_key == 'author' else 'none'};">
                        {'<span style="position:absolute; left:60px; font-size:2.6rem;">👉</span>' if t_key == 'author' else ''}
                        🧑‍🏫 By Raeven Brown (Author)
                    </div>
                    <div style="font-size:1.05rem; font-weight:800; color:#0f172a; background:{'#fef08a' if t_key == 'illustrator' else '#ffffffcc'}; border-radius:12px; padding:4px 14px; border:{'3px solid #f59e0b' if t_key == 'illustrator' else 'none'};">
                        {'<span style="position:absolute; right:20px; font-size:2.6rem;">👈</span>' if t_key == 'illustrator' else ''}
                        🎨 Art by Gracyn (Illustrator)
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(html_book, height=320)

        st.markdown(f"""
        <div style="background:#ffffff; border:4px solid #3b82f6; border-radius:24px; padding:18px; text-align:center; font-size:1.6rem; font-weight:800; color:#1e40af; margin-bottom:18px; box-shadow:0 8px 20px rgba(0,0,0,0.08);">
            ❓ {curr_q['q']}
        </div>
        """, unsafe_allow_html=True)

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
                        speak(f"Yes! Awesome job Gracyn! That is {opt['name']}!", "cheer")
                        award_score("Parts of a Book", f"Correct on {opt['name']}")
                        st.session_state.bq_idx += 1
                        st.rerun()
                    else:
                        speak(f"Not quite. {curr_q['wrong_exp']}", "tryagain")
                        track_performance("Parts of a Book", False, f"Chose {opt['name']}")

# ==========================================
# 3. NUMBER DETECTIVE (20 & UNDER) WITH REAL JARS & HIGH CONTRAST
# ==========================================
elif active_game == "🕵️ Number Detective (20 & Under)":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#b45309;">🕵️ Number Detective: Target 18!</div>
        <div style="font-size:1.15rem; font-weight:700; color:#475569;">Look inside the real glass candy jars and count the tallies! Tap the pictures that show EXACTLY 18!</div>
    </div>
    """, unsafe_allow_html=True)

    if "last_num_spoken" not in st.session_state:
        speak("Gracyn! We are looking for the number 18! Look at the shiny jelly bean jars, blocks, and wooden tallies. Tap the cards that equal 18!")
        st.session_state.last_num_spoken = True

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
            speak("Yes! Ten beans in the big jar plus eight beans in the second jar equals 18!", "cheer")
            award_score("Number Detective", "10+8 Beans = 18")

    with c2:
        st.markdown("""
        <div class="jar-container">
            <b style="font-size:1.4rem; color:#0369a1;">🟧 Base-Ten Rods & Ones:</b><br>
            <div style="background:#e0f2fe; border:2.5px solid #0284c7; border-radius:18px; padding:14px; margin:10px 0;">
                <div style="font-size:2rem; margin-bottom:4px;">🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦</div>
                <b style="font-size:1.25rem; color:#0f172a;">1 Ten-Rod (Counts as 10)</b>
                <div style="font-size:2rem; margin:8px 0 4px 0;">🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟩</div>
                <b style="font-size:1.25rem; color:#0f172a;">8 Individual Unit Cubes</b>
            </div>
            <div style="background:#fef08a; border-radius:14px; padding:6px; font-size:1.35rem; font-weight:900; color:#854d0e;">
                1 Ten + 8 Ones
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✅ Yes! This is 18!", key="btn_base10_18", use_container_width=True):
            st.balloons()
            speak("Bingo! 1 ten rod and 8 single cubes makes 18!", "cheer")
            award_score("Number Detective", "Base Ten 18")

    with c3:
        st.markdown("""
        <div class="jar-container" style="border-color:#f87171;">
            <b style="font-size:1.4rem; color:#dc2626;">🍪 Cookie Bakery Jar:</b><br>
            <div style="background:#fee2e2; border:2.5px solid #ef4444; border-radius:18px; padding:14px; margin:10px 0;">
                <div style="font-size:2rem; margin-bottom:4px;">🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪</div>
                <b style="font-size:1.25rem; color:#0f172a;">Jar 1: 10 Chocolate Cookies</b>
                <div style="font-size:2rem; margin:8px 0 4px 0;">🍪🍪🍪🍪</div>
                <b style="font-size:1.25rem; color:#0f172a;">Jar 2: 4 Sugar Cookies</b>
            </div>
            <div style="background:#fee2e2; border-radius:14px; padding:6px; font-size:1.35rem; font-weight:900; color:#b91c1c;">
                10 Cookies + 4 Cookies
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Is this 18 Cookies? 🤔", key="btn_cookies_14", use_container_width=True):
            speak("Count carefully Gracyn! Ten plus four is 14, not 18!", "tryagain")
            track_performance("Number Detective", False, "Chose 14 instead of 18")

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
            award_score("Number Detective", "Tallies 18")

# ==========================================
# 4. WORD FAMILY SPELLING LAB (-AT & -ALL FAMILIES)
# ==========================================
elif active_game == "🔤 Word Family Spelling Lab":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#7c3aed;">🔤 Word Family Phonics & Spelling Lab</div>
        <div style="font-size:1.15rem; font-weight:700; color:#475569;">Pick a beginning letter to build and spell real rhyming words!</div>
    </div>
    """, unsafe_allow_html=True)

    family_choice = st.radio("Choose Word Family to Spell:", ["🐱 -AT Family (cat, bat, hat, rat, mat)", "🏀 -ALL Family (ball, call, tall, fall, hall)"], horizontal=True)

    if "-AT" in family_choice:
        ending = "at"
        letters = [("C", "🐱 Cat"), ("B", "🦇 Bat"), ("H", "🎩 Hat"), ("R", "🐭 Rat"), ("M", "🧘 Mat")]
    else:
        ending = "all"
        letters = [("B", "🏀 Ball"), ("C", "📞 Call"), ("T", "🦒 Tall"), ("F", "🍂 Fall"), ("H", "🏛️ Hall")]

    if "last_spelling_spoken" not in st.session_state or st.session_state.last_spelling_spoken != ending:
        speak(f"Welcome to the {ending} word family! Tap a letter tile to spell a new rhyming word!")
        st.session_state.last_spelling_spoken = ending

    st.markdown(f"""
    <div style="background:#faf5ff; border:5px solid #a855f7; border-radius:28px; padding:22px; text-align:center; margin-bottom:18px;">
        <div style="font-size:2rem; font-weight:900; color:#6b21a8;">Target Word Family: <span style="font-size:3.5rem; color:#7e22ce;">-{ending.upper()}</span></div>
    </div>
    """, unsafe_allow_html=True)

    sp_cols = st.columns(len(letters))
    for i, (l_char, desc) in enumerate(letters):
        full_word = f"{l_char.lower()}{ending}"
        with sp_cols[i]:
            if st.button(f"🔤 {l_char}\n+{ending}", key=f"wf_{l_char}_{ending}", use_container_width=True):
                st.balloons()
                speak(f"{l_char} plus {ending} spells {full_word}! {desc}!", "cheer")
                award_score("Word Family Spelling", f"Spelled {full_word}")
                st.markdown(f"""
                <div style="background:#ffffff; border:4px solid #22c55e; border-radius:20px; padding:12px; text-align:center; font-size:1.8rem; font-weight:900; color:#15803d; margin-top:8px;">
                    ⭐ {full_word.upper()}! ({desc})
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 5. LETTER I-SPY SAFARI (DISAPPEARING BUBBLES)
# ==========================================
elif active_game == "🔍 Letter I-Spy Safari":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#db2777;">🔍 Letter I-Spy Safari Grid</div>
        <div style="font-size:1.15rem; font-weight:700; color:#475569;">Pop all the matching bubbles! Once popped, they disappear!</div>
    </div>
    """, unsafe_allow_html=True)

    if "target_letter" not in st.session_state:
        st.session_state.target_letter = random.choice(["B", "M", "D", "S", "A", "T"])
        st.session_state.popped_indices = []

    t_let = st.session_state.target_letter
    speak(f"Gracyn! I spy the letter {t_let}! Look at the bubbles and pop all the {t_let}'s you see!")

    st.markdown(f"""
    <div style="background:#ffffff; border:4px dashed #ec4899; border-radius:24px; padding:14px; text-align:center; font-size:1.8rem; font-weight:900; color:#db2777; margin-bottom:15px; box-shadow:0 6px 16px rgba(0,0,0,0.06);">
        🎯 I-SPY TARGET: <span style="font-size:3.5rem; color:#be185d;">{t_let}</span> or <span style="font-size:3.5rem; color:#be185d;">{t_let.lower()}</span>
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
                        award_score("Letter I-Spy", f"Found {char}")
                        st.rerun()
                    else:
                        speak(f"Oops! That is the letter {char}. Look for {t_let}!", "tryagain")

    if st.button("🔄 Play with a New Target Letter!", use_container_width=True):
        st.session_state.target_letter = random.choice(["B", "M", "D", "S", "A", "T"])
        st.session_state.popped_indices = []
        st.rerun()

# ==========================================
# 6. SEASONS WEATHER-CASTER (WITH ILLUSTRATED REAL-WORLD SCENES)
# ==========================================
elif active_game == "🍁 Seasons & Nature Quest":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#166534;">🍂 Seasons & Nature Weather-Caster</div>
        <div style="font-size:1.15rem; font-weight:700; color:#475569;">Look at the full picture card for each season and tap the matching answer!</div>
    </div>
    """, unsafe_allow_html=True)

    season_scenes = [
        {
            "season": "Winter",
            "q": "Freezing cold weather, snowmen with carrot noses, and warm cozy mittens!",
            "correct": "Winter",
            "choices": [
                {"name": "Winter", "img": "⛄❄️🧤", "desc": "Snowman, ice skates & snowflakes"},
                {"name": "Summer", "img": "☀️🏖️🍉", "desc": "Sunny beach & swimming"},
                {"name": "Spring", "img": "🌸🌱🌧️", "desc": "Rain boots & baby flowers"},
                {"name": "Fall / Autumn", "img": "🍂🍁🎃", "desc": "Orange leaves & pumpkin patch"}
            ]
        },
        {
            "season": "Summer",
            "q": "Super hot and sunny! Splashing in the swimming pool and eating cold watermelon!",
            "correct": "Summer",
            "choices": [
                {"name": "Summer", "img": "☀️🏖️🍉", "desc": "Sunny beach & swimming"},
                {"name": "Winter", "img": "⛄❄️🧤", "desc": "Snowman & snow boots"},
                {"name": "Spring", "img": "🌸🌱🌧️", "desc": "Green grass & rain boots"},
                {"name": "Fall / Autumn", "img": "🍂🍁🎃", "desc": "Crisp air & falling leaves"}
            ]
        },
        {
            "season": "Spring",
            "q": "Rain showers, green grass sprouting, and baby chicks hatching in their nests!",
            "correct": "Spring",
            "choices": [
                {"name": "Spring", "img": "🌸🌱🌧️", "desc": "Blooming flowers & rain boots"},
                {"name": "Summer", "img": "☀️🏖️🍉", "desc": "Hot sun & swimming pool"},
                {"name": "Winter", "img": "⛄❄️🧤", "desc": "Ice & snowman"},
                {"name": "Fall / Autumn", "img": "🍂🍁🎃", "desc": "Pumpkin spice & sweaters"}
            ]
        },
        {
            "season": "Fall / Autumn",
            "q": "Leaves turn red, orange, and gold and fall from the trees! Time for pumpkins and sweaters!",
            "correct": "Fall / Autumn",
            "choices": [
                {"name": "Fall / Autumn", "img": "🍂🍁🎃", "desc": "Pumpkin patch & orange leaves"},
                {"name": "Winter", "img": "⛄❄️🧤", "desc": "Snowflakes & freezing ice"},
                {"name": "Summer", "img": "☀️🏖️🍉", "desc": "Hot pool day"},
                {"name": "Spring", "img": "🌸🌱🌧️", "desc": "Flower blossoms"}
            ]
        }
    ]

    if "s_idx" not in st.session_state: st.session_state.s_idx = 0
    curr_sc = season_scenes[st.session_state.s_idx % len(season_scenes)]

    speak(f"Look at the weather clue: {curr_sc['q']} Which season is it?")

    st.markdown(f"""
    <div style="background:#ffffff; border:4px solid #22c55e; border-radius:28px; padding:22px; text-align:center; margin-bottom:18px; box-shadow:0 8px 20px rgba(0,0,0,0.08);">
        <div style="font-size:1.7rem; font-weight:800; color:#15803d;">{curr_sc['q']}</div>
    </div>
    """, unsafe_allow_html=True)

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
                    speak(f"Correct! That is what happens in {choice['name']}!", "cheer")
                    award_score("Seasons Quest", choice["name"])
                    st.session_state.s_idx += 1
                    st.rerun()
                else:
                    speak("Look at the picture clues again! Think about the weather!", "tryagain")

# ==========================================
# 7. COOL MATH (10 AND UNDER)
# ==========================================
elif active_game == "➕ Cool Math (10 and Under)":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#7e22ce;">🧮 Cool Math: 10 and Under!</div>
        <div style="font-size:1.15rem; font-weight:700; color:#475569;">Count the delicious apples and solve the problem!</div>
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
# 8. PARENT PROGRESS PORTAL
# ==========================================
elif active_game == "📊 Parent Progress Portal":
    st.markdown("""
    <div class="instruction-card">
        <div style="font-size:1.7rem; font-weight:900; color:#0f172a;">📊 Gracyn's Daily Learning Telemetry</div>
        <div style="font-size:1.15rem; font-weight:700; color:#475569;">Track daily scores, accuracy, and i-Ready proficiency milestones.</div>
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
