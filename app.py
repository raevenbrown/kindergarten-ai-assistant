import streamlit as st
import streamlit.components.v1 as components
import random
from supabase import create_client, Client

st.set_page_config(
    page_title="Kindergarten Learning Studio",
    page_icon="⭐",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #f59e0b; margin-bottom: 0px; }
    .sub-text { font-size: 1rem; color: #a89f91; margin-bottom: 20px; }
    .card-box { background: rgba(255,255,255,0.04); border: 1px solid rgba(245,158,11,0.25); padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .instruction-box { background: rgba(56, 189, 248, 0.08); border-left: 4px solid #38bdf8; padding: 12px 16px; border-radius: 6px; margin-bottom: 18px; color: #e0f2fe; }
    .explain-card { background: rgba(34, 197, 94, 0.1); border: 2px solid #22c55e; border-radius: 12px; padding: 18px; margin-top: 15px; margin-bottom: 15px; }
    .ladder-card { background: rgba(245, 158, 11, 0.08); border-left: 6px solid #f59e0b; border-radius: 8px; padding: 16px; font-size: 1.6rem; font-weight: 800; color: #fef08a; margin-bottom: 12px; }
    .ten-frame-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; width: 100%; max-width: 320px; margin: 12px 0; }
    .ten-frame-cell { border: 2px solid #f59e0b; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; border-radius: 6px; background: rgba(255,255,255,0.02); }
    .letter-card { font-size: 3.5rem; font-weight: 800; color: #f59e0b; text-align: center; padding: 15px; border: 2px dashed rgba(245,158,11,0.4); border-radius: 12px; margin-bottom: 10px; background: rgba(0,0,0,0.2); width: 120px; }
    .word-card { font-size: 2.8rem; font-weight: 800; color: #38bdf8; letter-spacing: 4px; text-align: center; padding: 15px; border: 2px solid #38bdf8; border-radius: 12px; margin-bottom: 15px; background: rgba(0,0,0,0.2); }
    .audio-btn { background: #38bdf8; color: #000; font-weight: bold; border-radius: 8px; border: none; padding: 8px 14px; cursor: pointer; }
</style>
""", unsafe_allow_html=True)

# Helper HTML5 Natural Speech Audio Component
def speak_button(text_to_speak, label="🔊 Listen"):
    html_code = f"""
    <button class="audio-btn" onclick="
        window.speechSynthesis.cancel();
        let utter = new SpeechSynthesisUtterance('{text_to_speak}');
        utter.rate = 0.85;
        utter.pitch = 1.15;
        window.speechSynthesis.speak(utter);
    ">{label}</button>
    """
    components.html(html_code, height=50)

# Browser Speech Recognition Component with Live Balloon Confetti Engine
def mic_checker_component(target_word):
    clean_target = target_word.replace("'", "").replace(".", "").replace("!", "").strip().lower()
    html_code = f"""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <div style="background: rgba(255,255,255,0.05); border: 2px solid rgba(56,189,248,0.4); border-radius: 12px; padding: 14px;">
        <button id="micBtn" style="background: #ef4444; color: #ffffff; font-weight: bold; font-size: 1.05rem; border: none; border-radius: 10px; padding: 10px 18px; cursor: pointer;" onclick="runSpeechRec()">
            🎙️ Tap to Speak
        </button>
        <div id="heardText" style="margin-top: 8px; font-size: 1.05rem; font-weight: 700; color: #38bdf8;"></div>
        <div id="resultBanner" style="margin-top: 8px; font-size: 1.05rem; font-weight: 800;"></div>
    </div>

    <script>
    function triggerBalloonsAndConfetti() {{
        var count = 200;
        var defaults = {{ origin: {{ y: 0.7 }} }};
        function fire(particleRatio, opts) {{
            confetti(Object.assign({{}}, defaults, opts, {{
                particleCount: Math.floor(count * particleRatio)
            }}));
        }}
        fire(0.25, {{ spread: 26, startVelocity: 55, shapes: ['circle'] }});
        fire(0.2, {{ spread: 60, shapes: ['circle'] }});
        fire(0.35, {{ spread: 100, decay: 0.91, scalar: 1.2 }});
        fire(0.1, {{ spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.5 }});
        fire(0.1, {{ spread: 120, startVelocity: 45 }});
    }}

    async function runSpeechRec() {{
        const btn = document.getElementById('micBtn');
        const heard = document.getElementById('heardText');
        const banner = document.getElementById('resultBanner');

        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) {{
            banner.innerHTML = '<span style="color:#f87171;">⚠️ Speech recognition not supported in this browser. Please use Chrome or Safari.</span>';
            return;
        }}

        try {{
            await navigator.mediaDevices.getUserMedia({{ audio: true }});
        }} catch(err) {{
            banner.innerHTML = '<span style="color:#f87171;">⚠️ Microphone permission denied. Please allow microphone access.</span>';
            return;
        }}

        const recognizer = new SpeechRec();
        recognizer.lang = 'en-US';
        recognizer.interimResults = false;
        recognizer.maxAlternatives = 1;

        btn.style.background = '#22c55e';
        btn.innerText = '🔴 Listening... Say it now!';
        heard.innerText = '';
        banner.innerText = '';

        recognizer.start();

        recognizer.onresult = function(event) {{
            const said = event.results[0][0].transcript.toLowerCase().replace(/[^a-z0-9 ]/g, "").trim();
            const expected = "{clean_target}";
            
            heard.innerHTML = '🗣️ You said: <u>"' + said + '"</u>';
            
            if (said.includes(expected) || expected.includes(said)) {{
                banner.innerHTML = '<div style="background: rgba(34,197,94,0.25); border: 2px solid #22c55e; color: #4ade80; padding: 10px; border-radius: 8px;">🎉 YOU SAID IT CORRECTLY! Awesome job! ⭐🎈</div>';
                triggerBalloonsAndConfetti();
                let audio = new Audio('https://cdn.freesound.org/previews/270/270304_5123851-lq.mp3');
                audio.play();
            }} else {{
                banner.innerHTML = '<div style="background: rgba(239,68,68,0.25); border: 2px solid #ef4444; color: #f87171; padding: 10px; border-radius: 8px;">❌ Not quite! Try saying it again clearly.</div>';
            }}

            btn.style.background = '#ef4444';
            btn.innerText = '🎙️ Tap to Speak Again';
        }};

        recognizer.onerror = function(event) {{
            btn.style.background = '#ef4444';
            btn.innerText = '🎙️ Tap to Speak';
            if (event.error === 'no-speech') {{
                banner.innerHTML = '<span style="color:#f87171;">⚠️ No voice heard. Tap and speak into your mic!</span>';
            }} else {{
                banner.innerHTML = '<span style="color:#f87171;">⚠️ Mic notice: ' + event.error + '. Try again!</span>';
            }}
        }};
    }}
    </script>
    """
    components.html(html_code, height=140)

# --- SUPABASE CONFIGURATION ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        pass

def log_milestone(student_name, activity, result):
    if supabase:
        try:
            supabase.table("student_milestones").insert({
                "student_name": student_name,
                "level": st.session_state.level,
                "stars": st.session_state.stars,
                "streak": st.session_state.streak,
                "xp": st.session_state.xp,
                "activity_type": activity,
                "action_result": result
            }).execute()
        except Exception:
            pass

# --- SESSION STATE INITIALIZATION ---
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "stars" not in st.session_state:
    st.session_state.stars = 0
if "student_name" not in st.session_state:
    st.session_state.student_name = "Gracyn"
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "🎵 Rhyme Quest"
if "prev_nav" not in st.session_state:
    st.session_state.prev_nav = "🎵 Rhyme Quest"
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "vowel_submitted" not in st.session_state:
    st.session_state.vowel_submitted = False
if "vowel_explanation" not in st.session_state:
    st.session_state.vowel_explanation = None
if "ladder_step" not in st.session_state:
    st.session_state.ladder_step = 1

# --- DATASETS ---
LEVEL_WORDS = {
    1: [
        {"target": "CAT", "rhymes": ["hat", "bat", "mat", "sat", "rat"], "wrong": ["dog", "sun", "pig", "cup"]},
        {"target": "PIN", "rhymes": ["win", "tin", "fin", "bin"], "wrong": ["bed", "box", "hat", "rug"]},
        {"target": "BED", "rhymes": ["red", "fed", "led"], "wrong": ["car", "sun", "top", "pig"]}
    ],
    2: [
        {"target": "HOP", "rhymes": ["mop", "top", "pop", "stop", "drop"], "wrong": ["bed", "fish", "cup", "pen"]},
        {"target": "PIG", "rhymes": ["big", "dig", "wig", "fig"], "wrong": ["pan", "star", "hot", "sun"]},
        {"target": "MUG", "rhymes": ["bug", "hug", "rug", "jug"], "wrong": ["cat", "pen", "leg", "top"]}
    ],
    3: [
        {"target": "TRUCK", "rhymes": ["duck", "stuck", "cluck", "luck"], "wrong": ["shoe", "star", "tree", "milk"]},
        {"target": "BOAT", "rhymes": ["goat", "coat", "float", "throat"], "wrong": ["kite", "fish", "jump", "lamp"]},
        {"target": "TRAIN", "rhymes": ["rain", "brain", "chain", "pain"], "wrong": ["book", "door", "leaf", "bird"]}
    ]
}

ALPHABET_PAIRS = [
    ("A", "a"), ("B", "b"), ("C", "c"), ("D", "d"), ("E", "e"), ("F", "f"),
    ("G", "g"), ("H", "h"), ("I", "i"), ("J", "j"), ("K", "k"), ("L", "l"),
    ("M", "m"), ("N", "n"), ("O", "o"), ("P", "p"), ("Q", "q"), ("R", "r"),
    ("S", "s"), ("T", "t"), ("U", "u"), ("V", "v"), ("W", "w"), ("X", "x"),
    ("Y", "y"), ("Z", "z")
]

VOWEL_GAME_WORDS = [
    {
        "word": "GRACYN",
        "vowels": ["A", "Y"],
        "breakdown": "• **A**: Standard vowel in the first syllable ('GRA-').<br>• **Y**: Acts as a **vowel** because it makes the short /ih/ or /ee/ sound in '-CYN'.",
        "why_y": "Y makes a vowel sound in this word, so it counts as a vowel!"
    },
    {
        "word": "SKY",
        "vowels": ["Y"],
        "breakdown": "• **Y**: Acts as the **only vowel** in the word, making the long /I/ sound!",
        "why_y": "Every word needs a vowel. In SKY, Y is the vowel sound!"
    },
    {
        "word": "HAPPY",
        "vowels": ["A", "Y"],
        "breakdown": "• **A**: Standard short /a/ vowel in 'HAP-'.<br>• **Y**: Acts as a **vowel** making the long /E/ sound at the end of '-PY'.",
        "why_y": "At the end of happy words, Y makes the 'ee' vowel sound!"
    },
    {
        "word": "YELLOW",
        "vowels": ["E", "O"],
        "breakdown": "• **E**: Standard short /e/ vowel in 'YEL-'.<br>• **O**: Standard long /o/ vowel in '-LOW'.<br>• **Y**: Acts as a **CONSONANT** because it begins the word with the /y/ sound!",
        "why_y": "Y is NOT a vowel here because it is at the start of the word making its consonant sound."
    },
    {
        "word": "FROG",
        "vowels": ["O"],
        "breakdown": "• **O**: Standard short /o/ vowel in the middle of the word.",
        "why_y": None
    },
    {
        "word": "SUN",
        "vowels": ["U"],
        "breakdown": "• **U**: Standard short /u/ vowel in the middle of the word.",
        "why_y": None
    },
    {
        "word": "APPLE",
        "vowels": ["A", "E"],
        "breakdown": "• **A**: Standard short /a/ vowel at the beginning.<br>• **E**: Silent vowel at the end.",
        "why_y": None
    },
    {
        "word": "TIGER",
        "vowels": ["I", "E"],
        "breakdown": "• **I**: Standard long /i/ vowel in 'TI-'.<br>• **E**: Standard vowel in '-GER'.",
        "why_y": None
    },
    {
        "word": "CANDY",
        "vowels": ["A", "Y"],
        "breakdown": "• **A**: Standard short /a/ vowel in 'CAN-'.<br>• **Y**: Acts as a **vowel** making the long /E/ sound at the end of '-DY'.",
        "why_y": "Y is a vowel here because it makes the 'ee' sound at the end!"
    },
    {
        "word": "YARN",
        "vowels": ["A"],
        "breakdown": "• **A**: Standard vowel sound in the middle.<br>• **Y**: Acts as a **CONSONANT** because it starts the word with the /y/ sound.",
        "why_y": "Y is NOT a vowel here because it begins the word making its consonant sound."
    }
]

LADDER_STORIES = {
    "🐱 The Fat Cat": [
        "This",
        "This is",
        "This is a cat.",
        "This is a fat cat.",
        "This fat cat sat on the mat."
    ],
    "🐷 The Big Pig": [
        "I",
        "I see",
        "I see a pig.",
        "I see a big pig.",
        "I see the big pig dig in mud."
    ],
    "🐔 The Red Hen": [
        "The",
        "The red",
        "The red hen",
        "The red hen has ten",
        "The red hen has ten eggs in the pen."
    ],
    "☀️ The Hot Sun": [
        "The",
        "The sun",
        "The sun is hot.",
        "We can run in the sun.",
        "We can run and have fun in the hot sun."
    ],
    "🐛 The Little Bug": [
        "The",
        "The bug",
        "The little bug",
        "The little bug sat",
        "The little bug sat on the big rug."
    ]
}

SOUND_WALL_WORDS = {
    "/p/ (Lips together, unvoiced)": {
        "word": "pan",
        "voice": "OFF (Unvoiced air burst)",
        "tip": "Press lips together and release a crisp puff of air without vibrating your voice box."
    },
    "/b/ (Lips together, voiced)": {
        "word": "bat",
        "voice": "ON (Voiced vibration)",
        "tip": "Press lips together and turn your voice box ON so your throat vibrates."
    },
    "/t/ (Tongue tap, unvoiced)": {
        "word": "top",
        "voice": "OFF (Unvoiced tap)",
        "tip": "Tap the tip of your tongue behind your top front teeth with a puff of air."
    },
    "/d/ (Tongue tap, voiced)": {
        "word": "duck",
        "voice": "ON (Voiced tap)",
        "tip": "Tap the tip of your tongue behind your front teeth with your voice box buzzing."
    },
    "/k/ (Back of tongue, unvoiced)": {
        "word": "kite",
        "voice": "OFF (Unvoiced)",
        "tip": "Push the back of your tongue against the roof of your mouth and release air."
    },
    "/m/ (Lips closed, nasal hum)": {
        "word": "map",
        "voice": "ON (Nasal Humming)",
        "tip": "Keep your lips closed and hum gently through your nose."
    },
    "/s/ (Air hiss, unvoiced)": {
        "word": "sun",
        "voice": "OFF (Unvoiced)",
        "tip": "Close your teeth lightly and hiss continuous air out like a friendly snake."
    },
    "/sh/ (Rounded lips air)": {
        "word": "ship",
        "voice": "OFF (Unvoiced)",
        "tip": "Round your lips forward into a circle and push gentle air through your teeth."
    }
}

# --- STRUCTURED KINDERGARTEN SIGHT WORD LISTS (1 & 2 FIRST) ---
SIGHT_WORD_LISTS = {
    "⭐ List 1 (Kindergarten Core)": [
        "the", "to", "and", "a", "I", "you", "it", "in", "said", "for"
    ],
    "🌟 List 2 (Kindergarten Core)": [
        "up", "look", "is", "go", "we", "little", "down", "can", "see", "not"
    ],
    "🚀 List 3 (Advanced)": [
        "one", "my", "me", "big", "come", "blue", "red", "where", "jump", "away"
    ],
    "💎 List 4 (Advanced)": [
        "here", "help", "make", "yellow", "two", "play", "run", "find", "three", "funny"
    ]
}

SYNONYMS_DATA = {
    "bad": ["awful", "terrible", "horrific", "dreadful"],
    "big": ["large", "huge", "gigantic", "giant"],
    "eat": ["gobble", "munch", "chomp", "devour"],
    "good": ["super", "excellent", "talented", "helpful"],
    "like": ["love", "enjoy", "adore"],
    "little": ["small", "tiny", "miniature"],
    "nice": ["pleasant", "sweet", "delightful"],
    "pretty": ["beautiful", "cute", "lovely"],
    "said": ["whispered", "shouted", "cried", "exclaimed"],
    "saw": ["spotted", "noticed", "observed"]
}

# --- INITIALIZE QUESTION GENERATORS ---
def init_rhyme_question():
    pool = LEVEL_WORDS[st.session_state.level]
    item = random.choice(pool)
    correct = random.choice(item["rhymes"])
    wrong_count = 2 if st.session_state.level == 1 else 3
    wrongs = random.sample(item["wrong"], wrong_count)
    opts = wrongs + [correct]
    random.shuffle(opts)
    st.session_state.current_rhyme = {
        "target": item["target"],
        "correct": correct,
        "options": opts,
        "valid_rhymes": item["rhymes"]
    }

def init_math_question():
    if st.session_state.level == 1:
        st.session_state.math_type = "count"
        st.session_state.current_math_target = random.randint(1, 5)
        st.session_state.sub_start = 0
        st.session_state.sub_take = 0
    elif st.session_state.level == 2:
        st.session_state.math_type = "add"
        a = random.randint(1, 5)
        b = random.randint(1, 4)
        st.session_state.add_a = a
        st.session_state.add_b = b
        st.session_state.current_math_target = a + b
    else:
        st.session_state.math_type = "subtract"
        start = random.randint(4, 9)
        takeaway = random.randint(1, start - 1)
        st.session_state.sub_start = start
        st.session_state.sub_take = takeaway
        st.session_state.current_math_target = start - takeaway

def init_letter_question():
    target = random.choice(ALPHABET_PAIRS)
    other_lowers = [l for u, l in ALPHABET_PAIRS if l != target[1]]
    distractors = random.sample(other_lowers, 3)
    opts = distractors + [target[1]]
    random.shuffle(opts)
    st.session_state.current_letter_target = target
    st.session_state.current_letter_options = opts

def init_vowel_word_game():
    st.session_state.current_vowel_game = random.choice(VOWEL_GAME_WORDS)
    st.session_state.vowel_submitted = False
    st.session_state.vowel_explanation = None

if "current_rhyme" not in st.session_state:
    init_rhyme_question()
if "current_math_target" not in st.session_state:
    init_math_question()
if "current_letter_target" not in st.session_state:
    init_letter_question()
if "current_vowel_game" not in st.session_state:
    init_vowel_word_game()

# --- ADAPTIVE LEVEL PROGRESSION CHECK ---
if st.session_state.stars >= 5 and st.session_state.level == 1:
    st.session_state.level = 2
    log_milestone(st.session_state.student_name, "Level Promotion", "Reached Level 2 (Addition Unlocked)")
    st.session_state.feedback = {"type": "success", "msg": "🚀 LEVEL UP! You reached Level 2 (Addition Unlocked)!", "celebrate": True}
    init_rhyme_question()
    init_math_question()
elif st.session_state.stars >= 12 and st.session_state.level == 2:
    st.session_state.level = 3
    log_milestone(st.session_state.student_name, "Level Promotion", "Reached Level 3 (Subtraction Unlocked)")
    st.session_state.feedback = {"type": "success", "msg": "👑 MASTER LEVEL! You reached Level 3 (Subtraction Unlocked)!", "celebrate": True}
    init_rhyme_question()
    init_math_question()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🎒 Navigation & Profile")
st.session_state.student_name = st.sidebar.text_input("Student Name:", value=st.session_state.student_name)

nav_options = [
    "🎵 Rhyme Quest", 
    "🔢 Ten-Frame Math", 
    "🔤 Letter Match",
    "🍎 Vowel Hunter",
    "🪜 Sentence Ladder Fluency",
    "🗣️ Sound Wall Lab",
    "📝 Sentence Scaffolds",
    "🦸 Super Synonyms",
    "🗂️ Sight Word Test"
]

selected_nav = st.sidebar.radio(
    "Choose Learning Area:", 
    nav_options, 
    index=nav_options.index(st.session_state.active_nav) if st.session_state.active_nav in nav_options else 0
)

if selected_nav != st.session_state.prev_nav:
    st.session_state.feedback = None
    st.session_state.active_nav = selected_nav
    st.session_state.prev_nav = selected_nav

if st.sidebar.button("🔄 Reset All Progress"):
    st.session_state.xp = 0
    st.session_state.streak = 0
    st.session_state.level = 1
    st.session_state.stars = 0
    st.session_state.feedback = None
    st.session_state.ladder_step = 1
    init_rhyme_question()
    init_math_question()
    init_letter_question()
    init_vowel_word_game()
    st.rerun()

# Top Scoreboard Banner
st.markdown(f"""
<div style="background: rgba(245, 158, 11, 0.08); border: 2px solid #f59e0b; padding: 18px; border-radius: 12px; display: flex; justify-content: space-around; align-items: center; margin-bottom: 24px;">
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">STUDENT LEVEL</span><br><b style="font-size: 1.4rem; color: #f59e0b;">Level {st.session_state.level} {'🌱 (Counting 1-5)' if st.session_state.level==1 else '🌟 (Addition 1-10)' if st.session_state.level==2 else '🚀 (Subtraction 1-10)'}</b></div>
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">STARS COLLECTED</span><br><b style="font-size: 1.4rem; color: #fbbf24;">⭐ {st.session_state.stars}</b></div>
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">CURRENT STREAK</span><br><b style="font-size: 1.4rem; color: #34d399;">🔥 {st.session_state.streak}</b></div>
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">TOTAL XP</span><br><b style="font-size: 1.4rem; color: #38bdf8;">💎 {st.session_state.xp}</b></div>
</div>
""", unsafe_allow_html=True)

# One-time feedback display
if st.session_state.feedback:
    fb = st.session_state.feedback
    if fb.get("celebrate"):
        st.balloons()
    if fb["type"] == "success":
        st.success(fb["msg"])
    else:
        st.error(fb["msg"])
    st.session_state.feedback = None

# ==========================================
# MODULE 1: RHYME QUEST
# ==========================================
if st.session_state.active_nav == "🎵 Rhyme Quest":
    st.subheader(f"Level {st.session_state.level} Rhyme Quest")
    st.markdown('<div class="instruction-box">👉 <b>Instructions for Kindergartener:</b> Click the sound button under each word to hear how it sounds! Then pick the word that rhymes with the target word and click <b>Submit Rhyme</b>!</div>', unsafe_allow_html=True)
    
    q = st.session_state.current_rhyme
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"### Target Word: **{q['target']}**")
        speak_button(q['target'], label=f"🔊 Say '{q['target']}'")
    
    with col2:
        st.markdown("#### Listen to the choices:")
        opt_cols = st.columns(len(q["options"]))
        for i, opt in enumerate(q["options"]):
            with opt_cols[i]:
                st.markdown(f"**{opt.upper()}**")
                speak_button(opt, label=f"🔊 {opt}")

        with st.form("rhyme_form_locked", clear_on_submit=False):
            selected_rhyme = st.radio("Which word rhymes?", q["options"], key="rhyme_radio_fixed")
            submit_rhyme = st.form_submit_button("Submit Rhyme 🎯")
            
            if submit_rhyme:
                if selected_rhyme in q["valid_rhymes"]:
                    st.session_state.stars += 1
                    st.session_state.streak += 1
                    st.session_state.xp += 50
                    log_milestone(st.session_state.student_name, "Rhyme Quest", f"Correct: {q['target']}->{selected_rhyme}")
                    st.session_state.feedback = {
                        "type": "success",
                        "msg": f"🎉 AWESOME JOB! '{q['target']}' and '{selected_rhyme}' rhyme! (+50 XP, +1 ⭐) Here is your next question:",
                        "celebrate": True
                    }
                    init_rhyme_question()
                    st.rerun()
                else:
                    st.session_state.streak = 0
                    log_milestone(st.session_state.student_name, "Rhyme Quest", f"Missed: {q['target']}->{selected_rhyme}")
                    st.session_state.feedback = {
                        "type": "error",
                        "msg": f"❌ Not quite! Listen closely to the ending sound of '{q['target']}' and try again.",
                        "celebrate": False
                    }
                    st.rerun()

# ==========================================
# MODULE 2: TEN-FRAME MATH LAB
# ==========================================
elif st.session_state.active_nav == "🔢 Ten-Frame Math":
    st.subheader(f"Level {st.session_state.level} Ten-Frame Math Lab")
    
    if st.session_state.level == 1:
        st.markdown('<div class="instruction-box">👉 <b>Instructions:</b> Count how many <b>yellow counters (🟡)</b> are in the 10-frame. Type your number and click <b>Check Count</b>!</div>', unsafe_allow_html=True)
        target = st.session_state.current_math_target
        cells = ["🟡" if i < target else "⬜" for i in range(10)]
    elif st.session_state.level == 2:
        st.markdown(f'<div class="instruction-box">👉 <b>Addition Challenge:</b> First we put <b>{st.session_state.add_a}</b> yellow dots (🟡), then we added <b>{st.session_state.add_b}</b> blue dots (🔵). How many dots in total?</div>', unsafe_allow_html=True)
        target = st.session_state.current_math_target
        cells = []
        for i in range(10):
            if i < st.session_state.add_a:
                cells.append("🟡")
            elif i < st.session_state.add_a + st.session_state.add_b:
                cells.append("🔵")
            else:
                cells.append("⬜")
    else:
        st.markdown(f'<div class="instruction-box">👉 <b>Subtraction Challenge:</b> We started with <b>{st.session_state.sub_start}</b> dots, but we took away <b>{st.session_state.sub_take}</b> (shown with ❌). Count only the remaining 🟡 dots!</div>', unsafe_allow_html=True)
        target = st.session_state.current_math_target
        cells = []
        for i in range(10):
            if i < target:
                cells.append("🟡")
            elif i < st.session_state.sub_start:
                cells.append("❌")
            else:
                cells.append("⬜")

    r1 = "".join([f"<div class='ten-frame-cell'>{c}</div>" for c in cells[:5]])
    r2 = "".join([f"<div class='ten-frame-cell'>{c}</div>" for c in cells[5:]])
    st.markdown(f"<div class='ten-frame-grid'>{r1}{r2}</div>", unsafe_allow_html=True)

    with st.form("math_form_locked", clear_on_submit=False):
        user_num = st.number_input("What is your answer?", min_value=0, max_value=20, step=1, key="math_input_locked")
        submit_math = st.form_submit_button("Check Math Answer ✅")
        
        if submit_math:
            if user_num == target:
                st.session_state.stars += 1
                st.session_state.streak += 1
                st.session_state.xp += 50
                log_milestone(st.session_state.student_name, "Ten-Frame Math", f"Correct Answer: {target}")
                st.session_state.feedback = {
                    "type": "success",
                    "msg": f"🎉 SPOT ON! The answer is {target}! (+50 XP, +1 ⭐) Here is your next math puzzle:",
                    "celebrate": True
                }
                init_math_question()
                st.rerun()
            else:
                st.session_state.streak = 0
                log_milestone(st.session_state.student_name, "Ten-Frame Math", f"Missed Math: expected {target} got {user_num}")
                st.session_state.feedback = {
                    "type": "error",
                    "msg": "❌ Not quite! Recount the active yellow dots (🟡) and try again.",
                    "celebrate": False
                }
                st.rerun()

# ==========================================
# MODULE 3: LETTER MATCH
# ==========================================
elif st.session_state.active_nav == "🔤 Letter Match":
    st.subheader(f"Level {st.session_state.level} Uppercase to Lowercase Match")
    st.markdown('<div class="instruction-box">👉 <b>Instructions:</b> Look at the BIG uppercase letter. Listen to the small lowercase choices below, select the matching partner, and click <b>Check Letter</b>!</div>', unsafe_allow_html=True)
    
    target_pair = st.session_state.current_letter_target
    options = st.session_state.current_letter_options
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f'<div class="letter-card">{target_pair[0]}</div>', unsafe_allow_html=True)
        speak_button(f"Uppercase letter {target_pair[0]}", label=f"🔊 Say '{target_pair[0]}'")
    
    with col2:
        st.markdown("#### Listen to the lowercase options:")
        opt_cols = st.columns(len(options))
        for i, opt in enumerate(options):
            with opt_cols[i]:
                st.markdown(f"<div style='font-size:1.8rem; font-weight:bold; color:#38bdf8;'>{opt}</div>", unsafe_allow_html=True)
                speak_button(f"Lowercase {opt}", label=f"🔊 {opt}")

        with st.form("letter_form_locked", clear_on_submit=False):
            user_char = st.radio("Which lowercase letter matches?", options, horizontal=True, key="letter_radio_opt")
            submit_let = st.form_submit_button("Check Letter 🔤")
            
            if submit_let:
                if user_char == target_pair[1]:
                    st.session_state.stars += 1
                    st.session_state.streak += 1
                    st.session_state.xp += 50
                    log_milestone(st.session_state.student_name, "Letter Match", f"Matched: {target_pair[0]}->{target_pair[1]}")
                    st.session_state.feedback = {
                        "type": "success",
                        "msg": f"🎉 PERFECT! Big '{target_pair[0]}' pairs with little '{target_pair[1]}'! (+50 XP, +1 ⭐) Ready for the next letter:",
                        "celebrate": True
                    }
                    init_letter_question()
                    st.rerun()
                else:
                    st.session_state.streak = 0
                    log_milestone(st.session_state.student_name, "Letter Match", f"Missed: {target_pair[0]} picked {user_char}")
                    st.session_state.feedback = {
                        "type": "error",
                        "msg": f"❌ Look closely! Big '{target_pair[0]}' pairs with lowercase '{target_pair[1]}'. Try another one!",
                        "celebrate": False
                    }
                    st.rerun()

# ==========================================
# MODULE 4: VOWEL HUNTER LAB
# ==========================================
elif st.session_state.active_nav == "🍎 Vowel Hunter":
    st.subheader("🍎 Interactive Vowel Hunter Lab")
    st.markdown("""
    <div class="instruction-box">
        👉 <b>What are Vowels?</b> The vowels are <b>A, E, I, O, U</b> — and <b>SOMETIMES Y</b>!
        <br>💡 <b>When is Y a Vowel?</b>
        <ul>
            <li><b>Y is a VOWEL</b> when it is in the middle or end of a word making a vowel sound like <i>'ee'</i> or <i>'eye'</i> (such as in <b>GRACYN</b>, <b>RUBY</b>, or <b>SKY</b>).</li>
            <li><b>Y is a CONSONANT</b> when it begins a word or syllable making the <i>/y/</i> sound (such as in <b>YELLOW</b> or <b>YOYO</b>).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    v_game_tab, v_name_tab, v_audio_tab = st.tabs([
        "🎮 Vowel Hunt Game & Explanation", 
        "👧 Analyze My Name (Gracyn)", 
        "🔊 Short vs. Long Vowel Sounds"
    ])
    
    with v_game_tab:
        vg = st.session_state.current_vowel_game
        st.markdown(f'<div class="word-card">{vg["word"]}</div>', unsafe_allow_html=True)
        speak_button(f"The word is {vg['word']}", label=f"🔊 Hear '{vg['word']}'")
        
        st.markdown("#### Check ALL the vowels inside this word:")
        
        with st.form("vowel_hunt_form", clear_on_submit=False):
            c_a, c_e, c_i, c_o, c_u, c_y = st.columns(6)
            check_a = c_a.checkbox("A")
            check_e = c_e.checkbox("E")
            check_i = c_i.checkbox("I")
            check_o = c_o.checkbox("O")
            check_u = c_u.checkbox("U")
            check_y = c_y.checkbox("Y (Sometimes)")
            
            submit_vowels = st.form_submit_button("Check Vowels & Explain 🎯")
            
            if submit_vowels:
                user_selected = []
                if check_a: user_selected.append("A")
                if check_e: user_selected.append("E")
                if check_i: user_selected.append("I")
                if check_o: user_selected.append("O")
                if check_u: user_selected.append("U")
                if check_y: user_selected.append("Y")
                
                correct_vowels = sorted(vg["vowels"])
                user_selected_sorted = sorted(user_selected)
                
                st.session_state.vowel_submitted = True
                is_correct = (user_selected_sorted == correct_vowels)
                
                if is_correct:
                    st.session_state.stars += 1
                    st.session_state.streak += 1
                    st.session_state.xp += 50
                    log_milestone(st.session_state.student_name, "Vowel Hunt", f"Found vowels in: {vg['word']}")
                    st.session_state.vowel_explanation = {
                        "status": "correct",
                        "title": f"🎉 SPOT ON! The vowels in {vg['word']} are: {', '.join(correct_vowels)}!",
                        "breakdown": vg["breakdown"],
                        "why_y": vg.get("why_y")
                    }
                else:
                    st.session_state.streak = 0
                    log_milestone(st.session_state.student_name, "Vowel Hunt", f"Missed vowels in: {vg['word']}")
                    st.session_state.vowel_explanation = {
                        "status": "incorrect",
                        "title": f"💡 Let's Learn: The vowels in {vg['word']} are actually: {', '.join(correct_vowels)}!",
                        "breakdown": vg["breakdown"],
                        "why_y": vg.get("why_y")
                    }
                st.rerun()

        if st.session_state.vowel_submitted and st.session_state.vowel_explanation:
            exp = st.session_state.vowel_explanation
            if exp["status"] == "correct":
                st.balloons()
            
            st.markdown(f"""
            <div class="explain-card">
                <h3>{exp['title']}</h3>
                <h4>📖 Phonics Explanation:</h4>
                <p>{exp['breakdown']}</p>
                {f"<p><b>🌟 The 'Y' Rule for this word:</b> {exp['why_y']}</p>" if exp.get('why_y') else ""}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("➡️ Next Vowel Word 🎯"):
                init_vowel_word_game()
                st.rerun()

    with v_name_tab:
        st.markdown(f"### 🔍 Vowel Breakdown for: **{st.session_state.student_name}**")
        name_clean = st.session_state.student_name.upper().strip()
        
        found_standard = [c for c in name_clean if c in "AEIOU"]
        has_y = "Y" in name_clean
        
        st.markdown(f"- Standard Vowels (A, E, I, O, U): **{', '.join(set(found_standard)) if found_standard else 'None'}**")
        
        if has_y:
            if not name_clean.startswith("Y"):
                st.success(f"⭐ **Y is acting as a VOWEL in {name_clean}!** Because it is inside the name making the short /ih/ or /ee/ sound, **{name_clean} has {len(found_standard) + name_clean.count('Y')} total vowels**: `{' + '.join(set(found_standard + ['Y']))}`!")
            else:
                st.info(f"In **{name_clean}**, Y starts the name, so it functions as a **consonant**.")
        else:
            st.write(f"- Total vowels in name: **{len(found_standard)}**")
        
        st.write("---")
        custom_input = st.text_input("Type any other name or word to test:", "Gracyn")
        if custom_input:
            cw = custom_input.upper().strip()
            cw_std = [c for c in cw if c in "AEIOU"]
            cw_y = "Y" in cw
            st.write(f"Vowel breakdown for **{cw}**:")
            if cw_y and not cw.startswith("Y"):
                st.write(f"• Includes **A,E,I,O,U**: `{', '.join(set(cw_std)) if cw_std else 'None'}`")
                st.write(f"• Includes **Y as a vowel**: `Yes` (makes a vowel sound in this position)")
                st.success(f"Total vowels in **{cw}**: **{len(cw_std) + cw.count('Y')}**")
            else:
                st.write(f"• Standard Vowels: `{', '.join(set(cw_std)) if cw_std else 'None'}`")
                st.write(f"• Y included as vowel: `{'No (Consonant position)' if cw.startswith('Y') else 'No Y in word'}`")
                st.success(f"Total vowels in **{cw}**: **{len(cw_std)}**")

    with v_audio_tab:
        vowel_choice = st.selectbox("Select a Vowel:", ["A (Short: Apple | Long: Acorn)", "E (Short: Egg | Long: Eagle)", "I (Short: Igloo | Long: Ice)", "O (Short: Octopus | Long: Ocean)", "U (Short: Umbrella | Long: Unicorn)", "Y (Vowel sound: Sky & Happy)"])
        v_letter = vowel_choice[0]
        speak_button(f"The letter {v_letter}. Short sound is {v_letter} like apple. Long sound is {v_letter} like acorn.", label=f"🔊 Listen to Vowel '{v_letter}' Sounds")

# ==========================================
# MODULE 5: SENTENCE LADDER FLUENCY WITH COMPACT MIC CHECKER
# ==========================================
elif st.session_state.active_nav == "🪜 Sentence Ladder Fluency":
    st.subheader("🪜 Sentence Ladder Fluency Reader")
    st.markdown("""
    <div class="instruction-box">
        👉 <b>How to Practice:</b> 
        1. Click <b>🔊 Listen</b> to hear the goal sentence.
        2. Click <b>🎙️ Tap to Speak</b> and read the phrase aloud.
        3. Watch for the 🎈 celebration, then click <b>⭐ Verified! Next Step</b> to climb the ladder!
    </div>
    """, unsafe_allow_html=True)

    story_name = st.selectbox("Choose a Sentence Ladder Story:", list(LADDER_STORIES.keys()))
    ladder_steps = LADDER_STORIES[story_name]
    max_step = len(ladder_steps)
    current_idx = min(st.session_state.ladder_step - 1, max_step - 1)
    current_phrase = ladder_steps[current_idx]

    st.markdown(f"### 🪜 Ladder Step {current_idx + 1} of {max_step}:")
    st.markdown(f'<div class="ladder-card">{current_phrase}</div>', unsafe_allow_html=True)

    col_tts, col_rec = st.columns([1, 2])
    with col_tts:
        speak_button(current_phrase, label=f"🔊 Hear '{current_phrase}'")
    
    with col_rec:
        mic_checker_component(current_phrase)

    st.write("---")
    
    c_verify, c_restart, _ = st.columns([2, 1, 2])
    with c_verify:
        if current_idx < max_step - 1:
            if st.button("⭐ Verified! Next Step (+50 XP, +1 ⭐) ➡️"):
                st.session_state.stars += 1
                st.session_state.streak += 1
                st.session_state.xp += 50
                log_milestone(st.session_state.student_name, "Sentence Ladder", f"Read Step {current_idx+1}: {current_phrase}")
                st.session_state.ladder_step += 1
                st.session_state.feedback = {
                    "type": "success",
                    "msg": f"🎉 EXCELLENT READING! '{current_phrase}' was read correctly! (+50 XP, +1 ⭐) Moving to Step {st.session_state.ladder_step}...",
                    "celebrate": True
                }
                st.rerun()
        else:
            if st.button("👑 Finished Entire Story! (+100 XP, +2 ⭐) 🎉"):
                st.session_state.stars += 2
                st.session_state.streak += 1
                st.session_state.xp += 100
                log_milestone(st.session_state.student_name, "Sentence Ladder", f"Mastered Whole Story: {story_name}")
                st.session_state.feedback = {
                    "type": "success",
                    "msg": f"🏆 STORY MASTER! You read all steps of '{story_name}' aloud perfectly! (+100 XP, +2 ⭐)",
                    "celebrate": True
                }
                st.session_state.ladder_step = 1
                st.rerun()

    with c_restart:
        if st.button("🔄 Restart Story"):
            st.session_state.ladder_step = 1
            st.session_state.feedback = None
            st.rerun()

# ==========================================
# MODULE 6: SOUND WALL LAB (COMPACT SPEECH BOX)
# ==========================================
elif st.session_state.active_nav == "🗣️ Sound Wall Lab":
    st.subheader("🗣️ Kindergarten Personal Sound Wall & Speech Lab")
    st.markdown("""
    <div class="instruction-box">
        👉 <b>How to Practice:</b> 
        1. <b>Hear Word:</b> Click the blue button to hear the target word pronounced cleanly. 
        2. <b>Say It:</b> Click <b>🎙️ Tap to Speak</b> and pronounce the word into your microphone!
    </div>
    """, unsafe_allow_html=True)

    choice = st.selectbox("Select Target Sound:", list(SOUND_WALL_WORDS.keys()))
    s_info = SOUND_WALL_WORDS[choice]

    col_profile, col_audio = st.columns([1, 1])
    with col_profile:
        st.markdown(f"""
        <div class="card-box">
            <h4>👄 Sound Profile: <code>{choice.split()[0]}</code></h4>
            <p><b>Target Word:</b> ✨ <b style="font-size: 1.8rem; color: #38bdf8;">{s_info['word'].upper()}</b></p>
            <p><b>Voice Box Status:</b> <code>{s_info['voice']}</code></p>
            <p><b>Mouth Gesture Tip:</b> {s_info['tip']}</p>
        </div>
        """, unsafe_allow_html=True)
        speak_button(s_info['word'], label=f"🔊 Hear Word '{s_info['word'].upper()}'")

    with col_audio:
        st.markdown("#### 🎙️ Student Speaking Practice:")
        st.write(f"Say **'{s_info['word'].upper()}'** into your microphone:")
        mic_checker_component(s_info["word"])
        
        if st.button(f"⭐ Add Stars for '{s_info['word'].upper()}' (+50 XP, +1 ⭐)"):
            st.session_state.stars += 1
            st.session_state.streak += 1
            st.session_state.xp += 50
            log_milestone(st.session_state.student_name, "Sound Wall", f"Mastered: {s_info['word']}")
            st.session_state.feedback = {
                "type": "success",
                "msg": f"🎉 AWESOME! You practiced '{s_info['word'].upper()}'! (+50 XP, +1 ⭐)",
                "celebrate": True
            }
            st.rerun()

# ==========================================
# MODULE 7: WRITING SCAFFOLDS
# ==========================================
elif st.session_state.active_nav == "📝 Sentence Scaffolds":
    st.subheader("📝 Kindergarten Interactive Sentence Scaffolds")
    st.markdown("""
    <div class="instruction-box">
        👉 <b>How Kindergarteners Build a 5-Star Sentence:</b>
        Every good sentence starts with a <b>Capital letter</b>, has <b>Finger spaces</b> between words, and ends with a <b>Period (.)</b>!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧩 Build-A-Sentence Activity")
    who = st.selectbox("Who is in the story? (Noun):", ["The cute puppy", "My big brother", "The happy frog", "Gracyn"])
    did_what = st.selectbox("What did they do? (Verb):", ["ran quickly", "jumped high", "read a book", "ate sweet apples"])
    where = st.selectbox("Where were they? (Setting):", ["in the green park.", "at kindergarten school.", "under the tall tree."])

    built_sentence = f"{who} {did_what} {where}"
    st.success(f"**Your Complete Sentence:** {built_sentence}")
    speak_button(built_sentence, label="🔊 Hear Your Sentence Read Aloud")

    st.markdown("#### ✅ Sentence Quality Checklist:")
    c1, c2, c3 = st.columns(3)
    c1.checkbox("Capital letter at the start", value=True)
    c2.checkbox("Finger spaces used", value=True)
    c3.checkbox("Punctuation mark at the end (.)", value=True)

# ==========================================
# MODULE 8: SUPER SYNONYMS
# ==========================================
elif st.session_state.active_nav == "🦸 Super Synonyms":
    st.subheader("🦸 Super Synonyms & Sentence Stretcher")
    st.markdown('<div class="instruction-box">👉 <b>Instructions:</b> Trade boring, tired words for powerful words! Click any upgraded synonym to hear how it sounds in a sentence.</div>', unsafe_allow_html=True)

    base = st.selectbox("Pick a simple word to upgrade:", list(SYNONYMS_DATA.keys()))
    syns = SYNONYMS_DATA[base]

    st.markdown(f"### Super Words for **{base.upper()}**:")
    cols = st.columns(len(syns))
    for idx, s in enumerate(syns):
        with cols[idx]:
            st.markdown(f"✨ **{s.upper()}**")
            speak_button(f"Instead of {base}, we can say {s}.", label=f"🔊 {s}")

# ==========================================
# MODULE 9: SIGHT WORD TEST (LIST 1 & LIST 2 FIRST)
# ==========================================
elif st.session_state.active_nav == "🗂️ Sight Word Test":
    st.subheader("🗂️ Kindergarten Sight Word Reading Test")
    st.markdown("""
    <div class="instruction-box">
        👉 <b>Instructions:</b> We start with <b>List 1 and List 2</b> (Core Kindergarten Words). 
        Look at the word, click <b>🎙️ Tap to Speak</b> and read it into your microphone!
    </div>
    """, unsafe_allow_html=True)

    selected_list = st.selectbox("Choose Sight Word List:", list(SIGHT_WORD_LISTS.keys()), index=0)
    word_bank = SIGHT_WORD_LISTS[selected_list]

    if "current_sight_word" not in st.session_state or st.session_state.current_sight_word not in word_bank:
        st.session_state.current_sight_word = random.choice(word_bank)

    sw = st.session_state.current_sight_word
    col_x, col_y = st.columns([1, 2])
    with col_x:
        st.markdown(f'<div class="letter-card" style="font-size:2.8rem; width:220px; color:#fbbf24;">{sw}</div>', unsafe_allow_html=True)
        speak_button(sw, label=f"🔊 Pronounce '{sw}'")

    with col_y:
        st.markdown("#### 🎙️ Speech Mic Check:")
        mic_checker_component(sw)
        
        c_yes, c_next = st.columns(2)
        with c_yes:
            if st.button("⭐ Verified & Mastered (+50 XP, +1 ⭐)"):
                st.session_state.stars += 1
                st.session_state.streak += 1
                st.session_state.xp += 50
                log_milestone(st.session_state.student_name, "Sight Word Test", f"Mastered {selected_list}: {sw}")
                st.session_state.feedback = {
                    "type": "success",
                    "msg": f"🎉 AWESOME! You read '{sw}' correctly! (+50 XP, +1 ⭐)",
                    "celebrate": True
                }
                st.session_state.current_sight_word = random.choice(word_bank)
                st.rerun()
        with c_next:
            if st.button("➡️ Next Word"):
                st.session_state.feedback = None
                st.session_state.current_sight_word = random.choice(word_bank)
                st.rerun()
