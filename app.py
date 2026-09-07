import streamlit as st
import streamlit.components.v1 as components
import random
from supabase import create_client, Client

st.set_page_config(
    page_title="Gracyn's Learning Adventure Studio",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PLAYFUL ARCADE / HATCH IGNITE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Quicksand:wght@600;700;800&display=swap');

    /* Global Game Theme */
    .stApp {
        background: linear-gradient(180deg, #38bdf8 0%, #a7f3d0 60%, #fef08a 100%);
        font-family: 'Fredoka', 'Quicksand', cursive, sans-serif;
    }

    /* iPad Friendly Large Tap Targets */
    .stButton > button {
        border-radius: 24px !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        padding: 14px 28px !important;
        box-shadow: 0 8px 0 rgba(0,0,0,0.18) !important;
        transition: all 0.1s ease !important;
        border: 3px solid #ffffff !important;
    }
    .stButton > button:active {
        transform: translateY(6px) !important;
        box-shadow: 0 2px 0 rgba(0,0,0,0.18) !important;
    }

    /* Top HUD / Mascot Bar */
    .hud-banner {
        background: #ffffff;
        border-radius: 28px;
        padding: 16px 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 4px solid #facc15;
    }

    .badge-pill {
        background: #fef08a;
        color: #854d0e;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 1.25rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 2px solid #facc15;
    }

    /* Game Cards */
    .game-board {
        background: #ffffff;
        border-radius: 32px;
        padding: 24px;
        box-shadow: 0 14px 35px rgba(0,0,0,0.1);
        border: 5px solid #60a5fa;
        text-align: center;
        margin-bottom: 20px;
    }

    .game-title {
        font-size: 2rem;
        color: #1e3a8a;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .game-subtitle {
        font-size: 1.2rem;
        color: #4b5563;
        margin-bottom: 18px;
        font-weight: 600;
    }

    .avatar-preview {
        font-size: 5rem;
        background: #ecfeff;
        border: 4px dashed #06b6d4;
        border-radius: 50%;
        width: 140px;
        height: 140px;
        line-height: 130px;
        margin: 0 auto 10px auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# --- WEB AUDIO SYNTH & SOUND ENGINE ---
def play_sound_and_speak(text, sound_type="cheer"):
    sound_fx = {
        "cheer": "https://cdn.freesound.org/previews/270/270304_5123851-lq.mp3",
        "pop": "https://cdn.freesound.org/previews/536/536108_11565331-lq.mp3",
        "tada": "https://cdn.freesound.org/previews/397/397355_4284968-lq.mp3"
    }.get(sound_type, "")

    html_code = f"""
    <script>
        // SFX
        let sfx = new Audio("{sound_fx}");
        sfx.volume = 0.6;
        sfx.play().catch(e => console.log(e));

        // Kid-friendly slow voice
        window.speechSynthesis.cancel();
        let msg = new SpeechSynthesisUtterance("{text}");
        msg.rate = 0.82;
        msg.pitch = 1.25;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(html_code, height=0)

def kid_button(label, sound_text="", key=None):
    btn = st.button(label, key=key, use_container_width=True)
    if btn and sound_text:
        play_sound_and_speak(sound_text)
    return btn

# --- IPAD DRAWING PAD FOR TRACING & HEART WORDS ---
def kid_canvas(target_word):
    html = f"""
    <div style="background:#f8fafc; border:4px dashed #38bdf8; border-radius:24px; padding:12px; text-align:center;">
        <canvas id="cPad" width="340" height="150" style="background:#ffffff; border-radius:18px; touch-action:none; cursor:crosshair;"></canvas>
        <div style="margin-top:10px;">
            <button onclick="clearPad()" style="background:#ef4444; color:#fff; font-size:1.1rem; font-weight:800; border:none; border-radius:14px; padding:8px 20px; box-shadow:0 4px 0 #b91c1c;">🧹 Erase</button>
            <button onclick="cheerWrite()" style="background:#22c55e; color:#fff; font-size:1.1rem; font-weight:800; border:none; border-radius:14px; padding:8px 20px; box-shadow:0 4px 0 #15803d; margin-left:8px;">⭐ Check My Writing!</button>
        </div>
        <div id="cMsg" style="font-size:1.3rem; font-weight:bold; color:#16a34a; margin-top:8px;"></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
        const cvs = document.getElementById('cPad');
        const ctx = cvs.getContext('2d');
        let drawing = false;

        function start(e) {{ drawing = true; draw(e); }}
        function end() {{ drawing = false; ctx.beginPath(); }}
        function draw(e) {{
            if(!drawing) return;
            e.preventDefault();
            const rect = cvs.getBoundingClientRect();
            const x = (e.clientX || (e.touches && e.touches[0].clientX)) - rect.left;
            const y = (e.clientY || (e.touches && e.touches[0].clientY)) - rect.top;
            ctx.lineWidth = 8;
            ctx.lineCap = 'round';
            ctx.strokeStyle = '#ec4899';
            ctx.lineTo(x, y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(x, y);
        }}
        cvs.addEventListener('mousedown', start);
        cvs.addEventListener('mouseup', end);
        cvs.addEventListener('mousemove', draw);
        cvs.addEventListener('touchstart', start);
        cvs.addEventListener('touchend', end);
        cvs.addEventListener('touchmove', draw);
        function clearPad() {{ ctx.clearRect(0, 0, cvs.width, cvs.height); document.getElementById('cMsg').innerText = ''; }}
        function cheerWrite() {{
            confetti({{ particleCount: 80, spread: 70, origin: {{ y: 0.7 }} }});
            document.getElementById('cMsg').innerText = "🌟 WOW! Beautiful handwriting!";
            let a = new Audio('https://cdn.freesound.org/previews/270/270304_5123851-lq.mp3');
            a.play();
        }}
    </script>
    """
    components.html(html, height=250)

# --- SPEECH RECOGNITION WITH CONFETTI ---
def mic_speaker_box(target_word):
    clean_target = target_word.strip().lower()
    html = f"""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <div style="text-align:center;">
        <button id="micB" style="background:#f97316; color:#ffffff; font-size:1.3rem; font-weight:800; border:none; border-radius:24px; padding:14px 28px; box-shadow:0 6px 0 #c2410c; cursor:pointer;" onclick="startMic()">
            🎙️ Tap & Say: "{target_word.upper()}"
        </button>
        <div id="mRes" style="font-size:1.4rem; font-weight:bold; margin-top:12px;"></div>
    </div>
    <script>
        function startMic() {{
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            const res = document.getElementById('mRes');
            const btn = document.getElementById('micB');
            if(!SpeechRec) {{ res.innerHTML = "<span style='color:red;'>Use Safari or Chrome for mic!</span>"; return; }}
            const rec = new SpeechRec();
            rec.lang = 'en-US';
            btn.innerText = "👂 Listening to Gracyn...";
            btn.style.background = "#22c55e";
            rec.start();
            rec.onresult = (e) => {{
                let heard = e.results[0][0].transcript.toLowerCase().trim();
                let target = "{clean_target}";
                let match = (heard.includes(target) || target.includes(heard));
                if (target === "to" && (heard === "two" || heard === "too" || heard === "2")) match = true;
                if (target === "for" && (heard === "four" || heard === "4")) match = true;
                if (target === "i" && (heard === "eye")) match = true;
                if (target === "see" && (heard === "sea" || heard === "c")) match = true;
                if (match) {{
                    res.innerHTML = "<span style='color:#15803d;'>🎉 YES! You said it! 🌟🎈</span>";
                    confetti({{ particleCount: 150, spread: 80, origin: {{ y: 0.7 }} }});
                    let a = new Audio('https://cdn.freesound.org/previews/270/270304_5123851-lq.mp3');
                    a.play();
                }} else {{
                    res.innerHTML = "<span style='color:#b91c1c;'>👂 You said '" + heard + "' - Try once more!</span>";
                }}
                btn.innerText = '🎙️ Tap & Say Again';
                btn.style.background = "#f97316";
            }};
            rec.onerror = () => {{
                btn.innerText = '🎙️ Tap & Say';
                btn.style.background = "#f97316";
                res.innerHTML = "<span style='color:#ea580c;'>Tap and speak loud and clear!</span>";
            }}
        }}
    </script>
    """
    components.html(html, height=130)

# --- SUPABASE CONFIG ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        pass

def log_progress(activity, result):
    if supabase:
        try:
            supabase.table("student_milestones").insert({
                "student_name": "Gracyn",
                "level": st.session_state.level,
                "stars": st.session_state.stars,
                "streak": st.session_state.streak,
                "xp": st.session_state.coins,
                "activity_type": activity,
                "action_result": result
            }).execute()
        except Exception:
            pass

# --- SESSION STATE SETUP ---
if "stars" not in st.session_state: st.session_state.stars = 0
if "coins" not in st.session_state: st.session_state.coins = 50
if "streak" not in st.session_state: st.session_state.streak = 0
if "level" not in st.session_state: st.session_state.level = 1
if "questions_done" not in st.session_state: st.session_state.questions_done = 0
if "unlocked_treasure" not in st.session_state: st.session_state.unlocked_treasure = False
if "current_game" not in st.session_state: st.session_state.current_game = "📖 Heart Words"
if "avatar_head" not in st.session_state: st.session_state.avatar_head = "👑"
if "avatar_pet" not in st.session_state: st.session_state.avatar_pet = "🐥"
if "avatar_bg" not in st.session_state: st.session_state.avatar_bg = "#ecfeff"

# CURRICULUM VOCABULARY LISTS (Core List 1 & List 2)
HEART_WORDS_LIST = [
    "a", "the", "am", "at", "as", "to", "do", "I", "is", "was", "you", "and", 
    "man", "in", "it", "did", "sit", "can", "of", "for", "from", "your", "said", "all",
    "go", "like", "me", "see", "we", "dad", "mom", "my", "up", "he", "look", "are", 
    "come", "got", "here", "not", "play", "day", "down", "into", "she", "they", "where", "went", "will"
]

def award_win(points=10, stars=1):
    st.session_state.coins += points
    st.session_state.stars += stars
    st.session_state.streak += 1
    st.session_state.questions_done += 1
    if st.session_state.questions_done % 10 == 0:
        st.session_state.unlocked_treasure = True
        st.session_state.celebrate_text = "🎉 10 QUESTIONS COMPLETE! TREASURE BOX UNLOCKED! 🎁"
    else:
        st.session_state.celebrate_text = f"🌟 AWESOME JOB! +{points} Coins, +{stars} Star!"
    st.rerun()

# --- TOP HUD HEADER ---
hud_col1, hud_col2, hud_col3 = st.columns([1.5, 2.5, 1.5])
with hud_col1:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="font-size:3.5rem; background:{st.session_state.avatar_bg}; border-radius:50%; border:3px solid #38bdf8; width:70px; height:70px; display:flex; align-items:center; justify-content:center;">
            {st.session_state.avatar_head}
        </div>
        <div>
            <b style="font-size:1.4rem; color:#1e293b;">Gracyn's Quest</b><br>
            <span style="color:#0284c7; font-weight:700;">Level {st.session_state.level} Superstar</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hud_col2:
    progress_val = (st.session_state.questions_done % 10) / 10.0
    st.progress(progress_val)
    st.markdown(f"<div style='text-align:center; font-weight:700; color:#0369a1;'>🎯 {st.session_state.questions_done % 10}/10 to Open Treasure Box! (Streak: 🔥 {st.session_state.streak})</div>", unsafe_allow_html=True)

with hud_col3:
    c_coin, c_star = st.columns(2)
    c_coin.markdown(f"<div class='badge-pill'>🪙 {st.session_state.coins}</div>", unsafe_allow_html=True)
    c_star.markdown(f"<div class='badge-pill'>⭐ {st.session_state.stars}</div>", unsafe_allow_html=True)

if st.session_state.unlocked_treasure:
    st.balloons()
    st.success("🎁 TREASURE BOX OPEN! Head to the Avatar Closet to spend your coins!")

# --- GAME SELECTOR TABS ---
st.markdown("---")
game_modes = [
    "📖 Heart Words",
    "📚 Parts of a Book",
    "🕵️ Number Detective (18 & Beyond)",
    "🔤 Letter I-Spy",
    "🍁 Seasons & Nature Quest",
    "➕ Kumon Math Challenge",
    "🎁 Treasure Closet"
]
active_game = st.selectbox("🎮 Choose an Adventure Game:", game_modes, index=game_modes.index(st.session_state.current_game))
st.session_state.current_game = active_game

# ==========================================
# 1. HEART WORDS: READ, TRACE, WRITE & SAY
# ==========================================
if active_game == "📖 Heart Words":
    st.markdown("""
    <div class="game-board">
        <div class="game-title">💖 Heart Word Explorer</div>
        <div class="game-subtitle">Sight words you have to know by heart! Read it, trace it, write it, and say it loud!</div>
    </div>
    """, unsafe_allow_html=True)

    if "current_hw" not in st.session_state:
        st.session_state.current_hw = random.choice(HEART_WORDS_LIST)

    word = st.session_state.current_hw
    col_w1, col_w2 = st.columns([1, 1.2])

    with col_w1:
        st.markdown(f"""
        <div style="background:#fef2f2; border:5px solid #f87171; border-radius:30px; padding:30px; text-align:center; margin-bottom:15px;">
            <div style="font-size:1.8rem; color:#ef4444; font-weight:800;">❤️ HEART WORD:</div>
            <div style="font-size:5rem; font-weight:900; color:#dc2626; letter-spacing:6px;">{word.upper()}</div>
        </div>
        """, unsafe_allow_html=True)
        mic_speaker_box(word)

    with col_w2:
        st.markdown("#### ✏️ Trace & Write with Your Finger / Stylus:")
        kid_canvas(word.upper())
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🌟 I Mastered This Word! (+10 🪙)", use_container_width=True):
                log_progress("Heart Word", f"Mastered {word}")
                st.session_state.current_hw = random.choice(HEART_WORDS_LIST)
                award_win(10, 1)
        with c2:
            if st.button("➡️ Next Word 🎲", use_container_width=True):
                st.session_state.current_hw = random.choice(HEART_WORDS_LIST)
                st.rerun()

# ==========================================
# 2. PARTS OF A BOOK (i-Ready Kindergarten Reading)
# ==========================================
elif active_game == "📚 Parts of a Book":
    st.markdown("""
    <div class="game-board">
        <div class="game-title">📚 Parts of a Book Detective</div>
        <div class="game-subtitle">Tap the matching part of the book to help Chickie get ready to read!</div>
    </div>
    """, unsafe_allow_html=True)

    book_questions = [
        {"q": "Where is the FRONT COVER that protects the book?", "correct": "Front Cover", "opts": ["Front Cover", "Spine", "Back Cover", "Page Numbers"], "desc": "The front cover welcomes you to the story!"},
        {"q": "What tells you what the book is called?", "correct": "The Title", "opts": ["The Title", "The Barcode", "The Spine", "The Illustrator"], "desc": "The Title is the name of the book!"},
        {"q": "Who WRITES the words in the book?", "correct": "The Author", "opts": ["The Author", "The Illustrator", "The Character", "The Reader"], "desc": "The Author writes all the wonderful words!"},
        {"q": "Who DRAWS the colorful pictures in the book?", "correct": "The Illustrator", "opts": ["The Illustrator", "The Author", "The Library", "The Teacher"], "desc": "The Illustrator creates the artwork!"},
        {"q": "What holds the pages together tightly like your backbone?", "correct": "The Spine", "opts": ["The Spine", "The Cover", "The Bookmark", "The Glue"], "desc": "The spine connects and holds all the pages!"}
    ]

    if "book_q_idx" not in st.session_state:
        st.session_state.book_q_idx = 0

    bq = book_questions[st.session_state.book_q_idx % len(book_questions)]
    
    st.markdown(f"""
    <div style="background:#eff6ff; border:4px solid #3b82f6; border-radius:24px; padding:24px; text-align:center; font-size:1.8rem; font-weight:800; color:#1e40af; margin-bottom:20px;">
        ❓ {bq['q']}
    </div>
    """, unsafe_allow_html=True)

    b_cols = st.columns(2)
    for i, opt in enumerate(bq["opts"]):
        with b_cols[i % 2]:
            if st.button(f"👉 {opt}", key=f"bk_{opt}", use_container_width=True):
                if opt == bq["correct"]:
                    st.balloons()
                    st.success(f"🎉 CORRECT! {bq['desc']}")
                    log_progress("Parts of Book", f"Correct: {opt}")
                    st.session_state.book_q_idx += 1
                    award_win(15, 1)
                else:
                    st.error("❌ Try again! Think about what holds or names the book!")

# ==========================================
# 3. NUMBER DETECTIVE: REPRESENTING 18 & BEYOND
# ==========================================
elif active_game == "🕵️ Number Detective (18 & Beyond)":
    st.markdown("""
    <div class="game-board">
        <div class="game-title">🕵️ Number Detective: Target 18!</div>
        <div class="game-subtitle">Numbers can hide in tens frames, tallies, blocks, and addition! Spot the TRUE 18s!</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#fef3c7; border:4px solid #f59e0b; border-radius:24px; padding:18px; text-align:center; font-size:3rem; font-weight:900; color:#b45309; margin-bottom:20px;">
        🎯 TARGET NUMBER: 18 (Eighteen)
    </div>
    """, unsafe_allow_html=True)

    # 4 Cards for Gracyn to inspect
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    with c1:
        st.markdown("""
        <div style="background:#ffffff; border:3px solid #60a5fa; border-radius:20px; padding:16px; text-align:center;">
            <b>Double Ten-Frame:</b><br>
            [ 🟡 🟡 🟡 🟡 🟡 ] [ 🟡 🟡 🟡 🟡 🟡 ] (10)<br>
            [ 🟡 🟡 🟡 🟡 🟡 ] [ 🟡 🟡 🟡 ⬜ ⬜ ] (8)<br>
            <div style="font-size:1.2rem; color:#2563eb; font-weight:bold;">10 + 8</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✅ Yes, this is 18!", key="tenframe_18"):
            st.balloons()
            st.success("🌟 YES! 1 full ten frame + 8 more counters = 18!")
            award_win(10, 1)

    with c2:
        st.markdown("""
        <div style="background:#ffffff; border:3px solid #60a5fa; border-radius:20px; padding:16px; text-align:center;">
            <b>Base Ten Rods & Cubes:</b><br>
            🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦 (1 Rod = 10)<br>
            🟩 🟩 🟩 🟩 🟩 🟩 🟩 🟩 (8 ones)<br>
            <div style="font-size:1.2rem; color:#2563eb; font-weight:bold;">1 Ten and 8 Ones</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✅ Yes, this is 18!", key="base10_18"):
            st.balloons()
            st.success("🌟 YES! 1 Ten block and 8 One cubes make 18!")
            award_win(10, 1)

    with c3:
        st.markdown("""
        <div style="background:#ffffff; border:3px solid #f87171; border-radius:20px; padding:16px; text-align:center;">
            <b>Cookie Jars:</b><br>
            🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪 (10 cookies)<br>
            🍪🍪🍪🍪 (4 cookies)<br>
            <div style="font-size:1.2rem; color:#dc2626; font-weight:bold;">10 + 4</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Is this 18? 🤔", key="jars_14"):
            st.error("❌ Count carefully! 10 + 4 is 14, not 18!")

    with c4:
        st.markdown("""
        <div style="background:#ffffff; border:3px solid #60a5fa; border-radius:20px; padding:16px; text-align:center;">
            <b>Tally Marks:</b><br>
            卌 卌 卌 |||<br>
            (5 + 5 + 5 + 3)<br>
            <div style="font-size:1.2rem; color:#2563eb; font-weight:bold;">15 + 3</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✅ Yes, this is 18!", key="tally_18"):
            st.balloons()
            st.success("🌟 YES! 5 + 5 + 5 is 15, plus 3 tallies makes 18!")
            award_win(10, 1)

# ==========================================
# 4. LETTER I-SPY: UPPERCASE & LOWERCASE
# ==========================================
elif active_game == "🔤 Letter I-Spy":
    st.markdown("""
    <div class="game-board">
        <div class="game-title">🔍 Letter I-Spy Safari</div>
        <div class="game-subtitle">Find and tap all the lowercase matches to help the baby letters find their mommas!</div>
    </div>
    """, unsafe_allow_html=True)

    pairs = [("G", "g"), ("B", "b"), ("D", "d"), ("M", "m"), ("R", "r"), ("E", "e"), ("A", "a")]
    if "ispy_pair" not in st.session_state:
        st.session_state.ispy_pair = random.choice(pairs)

    big, small = st.session_state.ispy_pair

    st.markdown(f"""
    <div style="background:#fdf2f8; border:4px dashed #ec4899; border-radius:24px; padding:20px; text-align:center; font-size:2.8rem; font-weight:900; color:#db2777; margin-bottom:20px;">
        I SPY THE BIG LETTER: <span style="font-size:4rem; color:#be185d;">{big}</span><br>
        <span style="font-size:1.4rem; color:#475569;">Tap the lowercase baby letter partner:</span>
    </div>
    """, unsafe_allow_html=True)

    # Distractors
    other_letters = [l for _, l in pairs if l != small]
    choices = random.sample(other_letters, 3) + [small]
    random.shuffle(choices)

    cols = st.columns(4)
    for idx, c in enumerate(choices):
        with cols[idx]:
            if st.button(f"🎈 {c}", key=f"ispy_{c}_{idx}", use_container_width=True):
                if c == small:
                    st.balloons()
                    st.success(f"🎉 BINGO! Big {big} matches baby {small}!")
                    log_progress("Letter ISpy", f"Matched {big} to {small}")
                    st.session_state.ispy_pair = random.choice(pairs)
                    award_win(10, 1)
                else:
                    st.error(f"❌ That's '{c}'. Look for '{small}'!")

# ==========================================
# 5. SEASONS & NATURE QUEST
# ==========================================
elif active_game == "🍁 Seasons & Nature Quest":
    st.markdown("""
    <div class="game-board">
        <div class="game-title">🍂 Seasons & Weather Weather-Caster</div>
        <div class="game-subtitle">Look at the weather clue and pick the right season!</div>
    </div>
    """, unsafe_allow_html=True)

    season_questions = [
        {"clue": "🎃 Leaves turn red, yellow, and brown and fall to the ground. We wear warm sweaters!", "ans": "Fall / Autumn", "opts": ["Fall / Autumn", "Summer", "Spring", "Winter"]},
        {"clue": "❄️ It is freezing cold, snow falls, and we build snowmen and wear mittens!", "ans": "Winter", "opts": ["Winter", "Spring", "Summer", "Fall"]},
        {"clue": "🌸 Flowers begin to bloom, baby birds hatch, and rain helps the green grass grow!", "ans": "Spring", "opts": ["Spring", "Winter", "Fall", "Summer"]},
        {"clue": "☀️ It is hot and sunny! We go swimming in the pool and eat cold watermelon!", "ans": "Summer", "opts": ["Summer", "Winter", "Spring", "Fall"]}
    ]

    if "season_idx" not in st.session_state:
        st.session_state.season_idx = 0

    sq = season_questions[st.session_state.season_idx % len(season_questions)]
    st.markdown(f"""
    <div style="background:#f0fdf4; border:4px solid #22c55e; border-radius:24px; padding:24px; text-align:center; font-size:1.8rem; font-weight:800; color:#166534; margin-bottom:20px;">
        {sq['clue']}
    </div>
    """, unsafe_allow_html=True)

    scols = st.columns(2)
    for i, opt in enumerate(sq["opts"]):
        with scols[i % 2]:
            if st.button(f"🌤️ {opt}", key=f"s_{opt}", use_container_width=True):
                if opt == sq["ans"]:
                    st.balloons()
                    st.success(f"🎉 CORRECT! That is what happens in {opt}!")
                    log_progress("Seasons", f"Correct: {opt}")
                    st.session_state.season_idx += 1
                    award_win(15, 1)
                else:
                    st.error("❌ Not quite! Think about the temperature and nature clues!")

# ==========================================
# 6. KUMON MATH CHALLENGE (BEYOND 10)
# ==========================================
elif active_game == "➕ Kumon Math Challenge":
    st.markdown("""
    <div class="game-board">
        <div class="game-title">🧮 Kumon Speed Math: Beyond 10!</div>
        <div class="game-subtitle">Solve the math problem using blocks to power up your brain!</div>
    </div>
    """, unsafe_allow_html=True)

    if "math_q" not in st.session_state:
        # Generate addition or subtraction beyond 10
        is_add = random.choice([True, False])
        if is_add:
            a = random.randint(7, 12)
            b = random.randint(3, 8)
            st.session_state.math_q = {"a": a, "b": b, "op": "+", "ans": a + b}
        else:
            total = random.randint(12, 19)
            sub = random.randint(3, 7)
            st.session_state.math_q = {"a": total, "b": sub, "op": "-", "ans": total - sub}

    mq = st.session_state.math_q

    st.markdown(f"""
    <div style="background:#faf5ff; border:5px solid #a855f7; border-radius:28px; padding:24px; text-align:center; font-size:4.5rem; font-weight:900; color:#7e22ce; margin-bottom:20px;">
        {mq['a']} {mq['op']} {mq['b']} = ?
    </div>
    """, unsafe_allow_html=True)

    # Visual aids
    if mq["op"] == "+":
        st.markdown(f"<div style='text-align:center; font-size:1.5rem; margin-bottom:15px;'>{'🟦 ' * mq['a']} + {'🟨 ' * mq['b']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:center; font-size:1.5rem; margin-bottom:15px;'>{'🟦 ' * mq['ans']} {'❌ ' * mq['b']}</div>", unsafe_allow_html=True)

    wrong1 = mq["ans"] + random.choice([-2, -1, 1, 2])
    wrong2 = mq["ans"] + random.choice([-3, 3])
    opts = list(set([mq["ans"], wrong1, wrong2]))
    random.shuffle(opts)

    mcols = st.columns(len(opts))
    for i, opt in enumerate(opts):
        with mcols[i]:
            if st.button(f"🔢 {opt}", key=f"ans_{opt}", use_container_width=True):
                if opt == mq["ans"]:
                    st.balloons()
                    st.success(f"🎉 BRAVO! {mq['a']} {mq['op']} {mq['b']} is {mq['ans']}!")
                    log_progress("Kumon Math", f"Solved {mq['a']} {mq['op']} {mq['b']} = {mq['ans']}")
                    del st.session_state.math_q
                    award_win(15, 1)
                else:
                    st.error("❌ Recount the blocks and try again!")

# ==========================================
# 7. TREASURE CLOSET & AVATAR DRESS-UP
# ==========================================
elif active_game == "🎁 Treasure Closet":
    st.markdown("""
    <div class="game-board">
        <div class="game-title">🛍️ Gracyn's Treasure Closet & Arcade</div>
        <div class="game-subtitle">Spend your hard-earned Coins on cool hats, cute pet companions, and colorful stages!</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="avatar-preview" style="background:{st.session_state.avatar_bg};">
        {st.session_state.avatar_head}
    </div>
    <div style="font-size:1.5rem; font-weight:800; color:#0369a1; text-align:center; margin-bottom:20px;">
        Pet Companion: {st.session_state.avatar_pet}
    </div>
    """, unsafe_allow_html=True)

    t_tab1, t_tab2, t_tab3 = st.tabs(["👑 Hats & Crowns", "🐾 Pet Companions", "🎨 Stage Colors"])

    with t_tab1:
        st.markdown("#### Pick Your Crown / Hat (Free with your earned points!):")
        h_cols = st.columns(4)
        hats = ["👑 Crown", "🎀 Bow", "🎓 Scholar", "🦄 Unicorn", "🌸 Flower", "🤠 Cowgirl", "🎩 Top Hat", "🦸 Superhero"]
        for idx, h in enumerate(hats):
            sym = h.split()[0]
            with h_cols[idx % 4]:
                if st.button(h, key=f"hat_{sym}", use_container_width=True):
                    st.session_state.avatar_head = sym
                    st.rerun()

    with t_tab2:
        st.markdown("#### Adopt a Learning Buddy Pet:")
        p_cols = st.columns(4)
        pets = ["🐥 Chickie", "🐶 Puppy", "🐱 Kitty", "🐰 Bunny", "🐼 Panda", "🦊 Fox", "🦄 Unicorn", "🐬 Dolphin"]
        for idx, p in enumerate(pets):
            sym = p.split()[0]
            with p_cols[idx % 4]:
                if st.button(p, key=f"pet_{sym}", use_container_width=True):
                    st.session_state.avatar_pet = sym
                    st.rerun()

    with t_tab3:
        st.markdown("#### Choose Your Stage Background:")
        b_cols = st.columns(4)
        bgs = [("Sky Blue", "#e0f2fe"), ("Pink Bubblegum", "#fce7f3"), ("Lemon Drop", "#fef9c3"), ("Mint Green", "#dcfce7")]
        for idx, (name, hex_code) in enumerate(bgs):
            with b_cols[idx]:
                if st.button(f"🎨 {name}", key=f"bg_{idx}", use_container_width=True):
                    st.session_state.avatar_bg = hex_code
                    st.rerun()
