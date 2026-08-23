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
    .ten-frame-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; width: 100%; max-width: 320px; margin: 12px 0; }
    .ten-frame-cell { border: 2px solid #f59e0b; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; border-radius: 6px; background: rgba(255,255,255,0.02); }
    .letter-card { font-size: 3.5rem; font-weight: 800; color: #f59e0b; text-align: center; padding: 15px; border: 2px dashed rgba(245,158,11,0.4); border-radius: 12px; margin-bottom: 10px; background: rgba(0,0,0,0.2); width: 120px; }
    .word-card { font-size: 2.8rem; font-weight: 800; color: #38bdf8; letter-spacing: 4px; text-align: center; padding: 15px; border: 2px solid #38bdf8; border-radius: 12px; margin-bottom: 15px; background: rgba(0,0,0,0.2); }
    .audio-btn { background: #38bdf8; color: #000; font-weight: bold; border-radius: 8px; border: none; padding: 6px 12px; cursor: pointer; }
</style>
""", unsafe_allow_html=True)

# Helper HTML5 Text-To-Speech Component
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
    components.html(html_code, height=45)

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
    """Logs live game progress and level updates to Supabase backend."""
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
    {"word": "GRACYN", "vowels": ["A", "Y"], "y_rule": "In GRACYN, Y is a vowel because it makes the short /ih/ or /ee/ vowel sound in the second syllable!"},
    {"word": "SKY", "vowels": ["Y"], "y_rule": "In SKY, Y is the only vowel sound and makes the long /I/ sound!"},
    {"word": "HAPPY", "vowels": ["A", "Y"], "y_rule": "In HAPPY, Y makes the long /E/ vowel sound at the end!"},
    {"word": "YELLOW", "vowels": ["E", "O"], "y_rule": "In YELLOW, Y is a CONSONANT because it starts the word with the /y/ sound!"},
    {"word": "FROG", "vowels": ["O"], "y_rule": None},
    {"word": "SUN", "vowels": ["U"], "y_rule": None},
    {"word": "APPLE", "vowels": ["A", "E"], "y_rule": None},
    {"word": "TIGER", "vowels": ["I", "E"], "y_rule": None},
    {"word": "CANDY", "vowels": ["A", "Y"], "y_rule": "In CANDY, Y makes the long /E/ sound at the end, so it acts as a vowel!"},
    {"word": "YARN", "vowels": ["A"], "y_rule": "In YARN, Y is a CONSONANT because it begins the word making the /y/ sound!"}
]

HEART_WORDS_LIST = ["a", "to", "is", "the", "do", "was", "as", "I", "you"]
DECODABLE_WORDS_LIST = ["am", "man", "did", "at", "in", "sit", "an", "it", "can"]

MONTHLY_VOCAB = {
    "August": ["pencil", "crayons", "lemonade", "apple", "school"],
    "September": ["backpack", "pumpkin", "bus", "leaf", "apple tree"],
    "October": ["jack-o-lantern", "acorn", "candy corn", "scarecrow"],
    "November": ["corn", "poppy", "sun", "turkey"],
    "December": ["mitten", "peppermint", "hot chocolate", "snow globe"],
    "January": ["snowman", "ice skate", "penguin", "snowflake"],
    "February": ["groundhog", "heart", "Valentine"],
    "March": ["rainbow", "shamrock", "kite", "butterfly"],
    "April": ["rainboots", "rain", "earth", "umbrella"],
    "May": ["seeds", "watering can", "horse", "flower"]
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

SIGHT_WORDS_WALL = {
    "A": ["a", "about", "after", "again", "all", "always", "am", "an", "and", "are", "as", "ask", "ate"],
    "B": ["be", "because", "been", "before", "best", "black", "both", "bring", "brown", "but", "buy", "by"],
    "C": ["call", "came", "can", "cannot", "carry", "clean", "cold", "color", "come", "could", "cut"],
    "D": ["did", "do", "does", "done", "down", "draw", "drink", "drive", "drop", "dry"],
    "E": ["each", "early", "earth", "easy", "eat", "eight", "every"],
    "F": ["fall", "far", "fast", "find", "first", "five", "fly", "for", "found", "four", "funny"],
    "G": ["get", "girl", "give", "go", "goes", "gold", "good", "got", "green", "grew"],
    "H": ["had", "has", "have", "he", "help", "her", "here", "him", "his", "hold", "hot"],
    "I": ["I", "if", "in", "into", "is", "it", "its"],
    "J": ["jump", "just"],
    "K": ["keep", "kind", "know"],
    "L": ["let", "like", "little", "live", "long", "look", "love"],
    "M": ["made", "make", "many", "may", "me", "much", "must", "my"],
    "N": ["never", "new", "no", "not", "now"],
    "O": ["of", "off", "old", "on", "once", "one", "only", "open", "or", "our", "out", "over"],
    "P": ["pick", "play", "please", "pretty", "pool", "put"],
    "R": ["ran", "read", "red", "right", "round", "run"],
    "S": ["said", "saw", "say", "see", "seven", "she", "show", "sing", "sit", "six", "sleep", "small", "so", "some", "soon", "stop"],
    "T": ["take", "tell", "ten", "thank", "that", "the", "their", "them", "then", "there", "these", "they", "this", "three", "to", "today", "two"],
    "U": ["under", "up", "upon", "us", "use"],
    "V": ["very"],
    "W": ["walk", "want", "warm", "was", "wash", "we", "well", "went", "were", "what", "when", "where", "which", "white", "who", "why", "will", "wish", "work"],
    "Y": ["yellow", "yes", "you", "your"]
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

def init_sight_word_test():
    letter = random.choice(list(SIGHT_WORDS_WALL.keys()))
    st.session_state.current_sight_word = random.choice(SIGHT_WORDS_WALL[letter])

if "current_rhyme" not in st.session_state:
    init_rhyme_question()
if "current_math_target" not in st.session_state:
    init_math_question()
if "current_letter_target" not in st.session_state:
    init_letter_question()
if "current_vowel_game" not in st.session_state:
    init_vowel_word_game()
if "current_sight_word" not in st.session_state:
    init_sight_word_test()

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
    "📖 Decodable Story Builder",
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

# Clear old feedback if sidebar tab changed
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
    init_rhyme_question()
    init_math_question()
    init_letter_question()
    init_vowel_word_game()
    init_sight_word_test()
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
# MODULE 4: VOWEL HUNTER LAB (UPGRADED WITH Y-RULES & CHECKBOX GAME)
# ==========================================
elif st.session_state.active_nav == "🍎 Vowel Hunter":
    st.subheader("🍎 Interactive Vowel Hunter Lab")
    st.markdown("""
    <div class="instruction-box">
        👉 <b>What are Vowels?</b> The vowels are <b>A, E, I, O, U</b> — and <b>SOMETIMES Y</b>!
        <br>💡 <b>When is Y a Vowel?</b>
        <ul>
            <li><b>Y is a VOWEL</b> when it is at the end of a word or makes an <i>'ee'</i> or <i>'eye'</i> sound (like in <b>GRACYN</b>, <b>RUBY</b>, or <b>SKY</b>).</li>
            <li><b>Y is a CONSONANT</b> when it is at the start of a word making the <i>/y/</i> sound (like in <b>YELLOW</b> or <b>YOYO</b>).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    v_game_tab, v_name_tab, v_audio_tab = st.tabs([
        "🎮 Checkbox Vowel Hunt Game", 
        "👧 Analyze My Name (Gracyn / Skylar)", 
        "🔊 Short vs. Long Vowel Sounds"
    ])
    
    # 1. Interactive Checkbox Game
    with v_game_tab:
        vg = st.session_state.current_vowel_game
        st.markdown(f'<div class="word-card">{vg["word"]}</div>', unsafe_allow_html=True)
        speak_button(f"The word is {vg['word']}", label=f"🔊 Listen to '{vg['word']}'")
        
        st.markdown("#### Check ALL the vowels that are inside this word:")
        
        with st.form("vowel_hunt_form", clear_on_submit=False):
            c_a, c_e, c_i, c_o, c_u, c_y = st.columns(6)
            check_a = c_a.checkbox("A")
            check_e = c_e.checkbox("E")
            check_i = c_i.checkbox("I")
            check_o = c_o.checkbox("O")
            check_u = c_u.checkbox("U")
            check_y = c_y.checkbox("Y (Sometimes)")
            
            submit_vowels = st.form_submit_button("Check Vowels 🎯")
            
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
                
                if user_selected_sorted == correct_vowels:
                    st.session_state.stars += 1
                    st.session_state.streak += 1
                    st.session_state.xp += 50
                    log_milestone(st.session_state.student_name, "Vowel Hunt", f"Found vowels in: {vg['word']}")
                    
                    rule_msg = f"<br>💡 <i>{vg['y_rule']}</i>" if vg.get("y_rule") else ""
                    st.session_state.feedback = {
                        "type": "success",
                        "msg": f"🎉 VOWEL DETECTIVE! You found all vowels in {vg['word']} ({', '.join(correct_vowels)})! (+50 XP, +1 ⭐){rule_msg}",
                        "celebrate": True
                    }
                    init_vowel_word_game()
                    st.rerun()
                else:
                    st.session_state.streak = 0
                    log_milestone(st.session_state.student_name, "Vowel Hunt", f"Missed vowels in: {vg['word']}")
                    st.session_state.feedback = {
                        "type": "error",
                        "msg": f"❌ Not quite! In **{vg['word']}**, the correct vowels are: **{', '.join(correct_vowels)}**. {vg.get('y_rule', '')}",
                        "celebrate": False
                    }
                    st.rerun()

    # 2. Name & Custom Word Analyzer
    with v_name_tab:
        st.markdown(f"### 🔍 Vowel Breakdown for: **{st.session_state.student_name}**")
        name_clean = st.session_state.student_name.upper().strip()
        
        found_standard = [c for c in name_clean if c in "AEIOU"]
        has_y = "Y" in name_clean
        
        st.markdown(f"- Standard Vowels (A, E, I, O, U): **{', '.join(set(found_standard)) if found_standard else 'None'}**")
        
        if has_y:
            if not name_clean.startswith("Y"):
                st.success(f"⭐ **Y is acting as a VOWEL in {name_clean}!** Because it is inside or at the end of the name making a vowel sound, **{name_clean} has {len(found_standard) + name_clean.count('Y')} total vowels**: `{' + '.join(set(found_standard + ['Y']))}`!")
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

    # 3. Audio Guide
    with v_audio_tab:
        vowel_choice = st.selectbox("Select a Vowel:", ["A (Short: Apple | Long: Acorn)", "E (Short: Egg | Long: Eagle)", "I (Short: Igloo | Long: Ice)", "O (Short: Octopus | Long: Ocean)", "U (Short: Umbrella | Long: Unicorn)", "Y (Vowel sound: Sky & Happy)"])
        v_letter = vowel_choice[0]
        speak_button(f"The letter {v_letter}. Short sound is {v_letter} like apple. Long sound is {v_letter} like acorn.", label=f"🔊 Listen to Vowel '{v_letter}' Sounds")

# ==========================================
# MODULE 5: DECODABLE STORY BUILDER
# ==========================================
elif st.session_state.active_nav == "📖 Decodable Story Builder":
    st.subheader("📖 Decodable & Heart Word Story Builder")
    st.markdown("""
    <div class="instruction-box">
        👉 <b>What to do:</b> 
        <ol>
            <li>Pick <b>Heart Words</b> (words to memorize by sight, like <i>the, was, to</i>).</li>
            <li>Pick <b>Decodable Words</b> (words you can sound out with phonics, like <i>can, sit, man</i>).</li>
            <li>Choose a monthly theme, then click <b>Build Story</b> to generate a custom story with full read-aloud audio!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        hw = st.multiselect("1. Heart Words (Sight):", HEART_WORDS_LIST, default=["the", "was", "to"])
    with col2:
        dw = st.multiselect("2. Decodable Words (Phonics):", DECODABLE_WORDS_LIST, default=["can", "sit", "man"])
    with col3:
        month = st.selectbox("3. Monthly Theme:", list(MONTHLY_VOCAB.keys()), index=1)

    if st.button("✨ Build Story Practice Sheet"):
        item1 = random.choice(MONTHLY_VOCAB[month])
        item2 = random.choice(MONTHLY_VOCAB[month])
        
        story_text = f"{st.session_state.student_name} saw {hw[0] if hw else 'the'} {item1} by the school path. " \
                     f"{hw[1] if len(hw) > 1 else 'I'} {dw[0] if dw else 'can'} see a little friend {dw[1] if len(dw) > 1 else 'sit'} nearby. " \
                     f"It {hw[2] if len(hw) > 2 else 'was'} a fun time to look at the {item2}. " \
                     f"{st.session_state.student_name} will smile and enjoy the {month} day!"
        
        st.markdown(f"### 📄 {st.session_state.student_name}'s {month} Story")
        st.info(story_text)
        speak_button(story_text, label="🔊 Read Entire Story Aloud")

# ==========================================
# MODULE 6: SOUND WALL LAB
# ==========================================
elif st.session_state.active_nav == "🗣️ Sound Wall Lab":
    st.subheader("🗣️ Kindergarten Personal Sound Wall & Articulation Guide")
    st.markdown("""
    <div class="instruction-box">
        👉 <b>Instructions for Students & Parents:</b> 
        Look at how your lips and mouth move when making each sound. Click the sound button to hear the sound pronounced clearly!
    </div>
    """, unsafe_allow_html=True)

    sound_list = {
        "/p/ (Lips together, unvoiced - pan)": ("p", "pan", "Put lips together and pop air out without your voice box."),
        "/b/ (Lips together, voiced - bat)": ("b", "bat", "Put lips together and turn your voice box ON."),
        "/t/ (Tongue tap, unvoiced - taco)": ("t", "taco", "Tap the tip of your tongue behind your top teeth."),
        "/d/ (Tongue tap, voiced - duck)": ("d", "duck", "Tap your tongue behind your teeth with voice ON."),
        "/s/ (Air hiss, unvoiced - sun)": ("s", "sun", "Hiss air through your teeth like a snake."),
        "/sh/ (Rounded lips air - shark)": ("sh", "shark", "Round your lips like you are telling someone to be quiet."),
        "/ch/ (Stop and push - cherry)": ("ch", "cherry", "Touch your tongue to the roof of your mouth and push out air.")
    }

    choice = st.selectbox("Select Target Phoneme Sound:", list(sound_list.keys()))
    char, word_ex, tip = sound_list[choice]

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown(f"""
        <div class="card-box">
            <h4>👄 Sound Profile: <code>{choice.split()[0]}</code></h4>
            <p><b>Example Word:</b> ✨ <b>{word_ex.upper()}</b></p>
            <p><b>Mouth Gesture Tip:</b> {tip}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.write("Hear Sound & Word:")
        speak_button(f"The sound is {char}. As in {word_ex}.", label=f"🔊 Hear {choice.split()[0]} Sound")

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
# MODULE 9: SIGHT WORD TEST
# ==========================================
elif st.session_state.active_nav == "🗂️ Sight Word Test":
    st.subheader("🗂️ Sight Word Reading Test")
    st.markdown('<div class="instruction-box">👉 <b>Instructions:</b> Look at the sight word on the flashcard. Try reading it out loud, then click <b>Listen</b> to verify. If you knew it, click <b>I Got It Right!</b> to earn stars!</div>', unsafe_allow_html=True)

    sw = st.session_state.current_sight_word
    col_x, col_y = st.columns([1, 2])
    with col_x:
        st.markdown(f'<div class="letter-card" style="font-size:2.5rem; width:220px;">{sw}</div>', unsafe_allow_html=True)
        speak_button(sw, label=f"🔊 Pronounce '{sw}'")

    with col_y:
        st.markdown("#### Did you read the word correctly?")
        c_yes, c_next = st.columns(2)
        with c_yes:
            if st.button("⭐ Yes, I Got It Right! (+50 XP)"):
                st.session_state.stars += 1
                st.session_state.streak += 1
                st.session_state.xp += 50
                log_milestone(st.session_state.student_name, "Sight Word Test", f"Mastered: {sw}")
                st.session_state.feedback = {
                    "type": "success",
                    "msg": f"🎉 AWESOME! You read '{sw}' correctly! (+50 XP, +1 ⭐)",
                    "celebrate": True
                }
                init_sight_word_test()
                st.rerun()
        with c_next:
            if st.button("➡️ Next Word"):
                st.session_state.feedback = None
                init_sight_word_test()
                st.rerun()
