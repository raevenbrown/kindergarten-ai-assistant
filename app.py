import streamlit as st
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
    .card-box { background: rgba(255,255,255,0.03); border: 1px solid rgba(245,158,11,0.2); padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .ten-frame-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; width: 100%; max-width: 320px; margin: 12px 0; }
    .ten-frame-cell { border: 2px solid #f59e0b; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; border-radius: 6px; background: rgba(255,255,255,0.02); }
    .letter-card { font-size: 3.5rem; font-weight: 800; color: #f59e0b; text-align: center; padding: 15px; border: 2px dashed rgba(245,158,11,0.4); border-radius: 12px; margin-bottom: 10px; background: rgba(0,0,0,0.2); width: 120px; }
</style>
""", unsafe_allow_html=True)

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
    st.session_state.student_name = "Skylar"

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

HEART_WORDS_LIST = ["a", "to", "is", "the", "do", "was", "as", "I", "you"]
DECODABLE_WORDS_LIST = ["am", "man", "did", "at", "in", "sit", "an", "it", "can"]

MONTHLY_VOCAB = {
    "August": ["pencil", "crayons", "lemonade", "apple", "beach ball", "flip flop", "school"],
    "September": ["Johnny Appleseed", "backpack", "pumpkin", "bus", "leaf", "pirate", "apple tree"],
    "October": ["jack-o-lantern", "acorn", "candy corn", "Frankenstein", "scarecrow", "pumpkin"],
    "November": ["Native American", "skull", "corn", "poppy", "sun", "pilgrim", "turkey"],
    "December": ["mitten", "peppermint", "gingerbread house", "hot chocolate", "snow globe", "poinsettia", "tree"],
    "January": ["letter", "snowman", "ice skate", "penguin", "MLK Jr.", "polar bear", "snowflake"],
    "February": ["tooth", "groundhog", "football", "Mardi Gras", "heart", "Valentine", "Abe Lincoln"],
    "March": ["flower", "rainbow", "shamrock", "lamb", "kite", "leprechaun", "butterfly"],
    "April": ["tree", "rainboots", "rain", "earth", "umbrella", "bunny", "raincoat"],
    "May": ["Mother's Day", "horse", "shovel", "seeds", "watering can", "sombrero", "nurse"],
    "June": ["picnic", "hot air balloon", "sun", "Father's Day", "sunglasses", "ocean", "sandcastle"],
    "July": ["ice cream", "hotdog", "grill", "fireworks", "star", "shell", "Uncle Sam"]
}

SYNONYMS_DATA = {
    "bad": ["awful", "terrible", "horrific", "dreadful", "shocking"],
    "big": ["large", "huge", "gigantic", "giant", "enormous"],
    "eat": ["gobble", "munch", "chomp", "devour", "swallow"],
    "good": ["superior", "excellent", "decent", "worthy", "talented", "helpful"],
    "like": ["love", "enjoy", "adore", "fancy"],
    "little": ["small", "petite", "tiny", "miniature", "slight"],
    "nice": ["enjoyable", "pleasant", "sweet", "delightful"],
    "pretty": ["attractive", "beautiful", "cute", "appealing", "lovely", "adorable"],
    "said": ["whispered", "murmured", "uttered", "declared", "cried", "exclaimed"],
    "saw": ["observed", "noticed", "witnessed", "spotted", "caught a glimpse of"],
    "shout": ["yell", "cry", "scream", "screech", "holler", "roar"],
    "ugly": ["unattractive", "hideous", "unsightly", "repulsive", "gross"]
}

SIGHT_WORDS_WALL = {
    "A": ["a", "about", "after", "again", "all", "always", "am", "an", "and", "any", "are", "around", "as", "ask", "ate"],
    "B": ["be", "because", "been", "before", "best", "better", "black", "both", "bring", "brown", "but", "buy", "by"],
    "C": ["call", "came", "can", "cannot", "can't", "carry", "clean", "cold", "color", "come", "could", "cut"],
    "D": ["did", "do", "does", "doesn't", "don't", "done", "down", "draw", "drink", "drive", "drop", "dry", "during"],
    "E": ["each", "early", "earth", "east", "easy", "eat", "eight", "even", "every", "everyone", "everything"],
    "F": ["fall", "far", "fast", "find", "first", "five", "fly", "for", "found", "four", "from", "full", "funny"],
    "G": ["get", "girl", "give", "go", "goes", "going", "gold", "good", "got", "green", "grew", "ground", "group"],
    "H": ["had", "has", "have", "he", "help", "her", "here", "him", "his", "hold", "hot", "how", "hurt"],
    "I": ["I", "if", "I'll", "in", "into", "is", "isn't", "it", "its", "it's"],
    "J": ["jump", "just"],
    "K": ["keep", "kind", "know"],
    "L": ["let", "like", "little", "live", "long", "look", "love"],
    "M": ["made", "make", "many", "may", "me", "much", "must", "my", "myself"],
    "N": ["never", "new", "no", "not", "now"],
    "O": ["of", "off", "old", "on", "once", "one", "only", "open", "or", "our", "out", "over", "own"],
    "P": ["pick", "play", "please", "pretty", "pool", "put"],
    "R": ["ran", "read", "red", "right", "round", "run"],
    "S": ["said", "saw", "say", "see", "seven", "shall", "she", "show", "sing", "sit", "six", "sleep", "small", "so", "some", "soon", "start", "stop"],
    "T": ["take", "tell", "ten", "thank", "that", "the", "their", "them", "then", "there", "these", "they", "think", "this", "those", "three", "to", "today", "together", "too", "try", "two"],
    "U": ["under", "up", "upon", "us", "use"],
    "V": ["very"],
    "W": ["walk", "want", "warm", "was", "wash", "we", "well", "went", "were", "what", "when", "where", "which", "white", "who", "why", "will", "wish", "work", "would", "write"],
    "Y": ["yellow", "yes", "you", "your", "you're", "you've"]
}

# --- PERSISTENT QUESTION INITIALIZERS ---
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
    max_num = 5 if st.session_state.level == 1 else (10 if st.session_state.level == 2 else 20)
    st.session_state.current_math_target = random.randint(1, max_num)

def init_letter_question():
    st.session_state.current_letter_pair = random.choice(ALPHABET_PAIRS)

# Initialize on startup if not present
if "current_rhyme" not in st.session_state:
    init_rhyme_question()
if "current_math_target" not in st.session_state:
    init_math_question()
if "current_letter_pair" not in st.session_state:
    init_letter_question()

# --- ADAPTIVE LEVEL PROGRESSION CHECK ---
if st.session_state.stars >= 5 and st.session_state.level == 1:
    st.session_state.level = 2
    log_milestone(st.session_state.student_name, "Level Promotion", "Reached Level 2")
    st.balloons()
    init_rhyme_question()
    init_math_question()
elif st.session_state.stars >= 12 and st.session_state.level == 2:
    st.session_state.level = 3
    log_milestone(st.session_state.student_name, "Level Promotion", "Reached Level 3")
    st.balloons()
    init_rhyme_question()
    init_math_question()

# --- SIDEBAR & HEADER ---
st.markdown('<div class="main-title">✏️ Early Childhood Learning Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Interactive Literacy & Math Lab with Progress Tracking</div>', unsafe_allow_html=True)

st.sidebar.title("🎒 Student Profile")
st.session_state.student_name = st.sidebar.text_input("Student Name:", value=st.session_state.student_name)

if st.sidebar.button("🔄 Reset All Progress"):
    st.session_state.xp = 0
    st.session_state.streak = 0
    st.session_state.level = 1
    st.session_state.stars = 0
    init_rhyme_question()
    init_math_question()
    init_letter_question()
    st.rerun()

# Top Scoreboard Banner
st.markdown(f"""
<div style="background: rgba(245, 158, 11, 0.08); border: 2px solid #f59e0b; padding: 18px; border-radius: 12px; display: flex; justify-content: space-around; align-items: center; margin-bottom: 24px;">
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">STUDENT LEVEL</span><br><b style="font-size: 1.4rem; color: #f59e0b;">Level {st.session_state.level} {'🌱 (Emergent)' if st.session_state.level==1 else '🌟 (On-Level)' if st.session_state.level==2 else '🚀 (Advanced)'}</b></div>
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">STARS COLLECTED</span><br><b style="font-size: 1.4rem; color: #fbbf24;">⭐ {st.session_state.stars}</b></div>
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">CURRENT STREAK</span><br><b style="font-size: 1.4rem; color: #34d399;">🔥 {st.session_state.streak}</b></div>
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">TOTAL XP</span><br><b style="font-size: 1.4rem; color: #38bdf8;">💎 {st.session_state.xp}</b></div>
</div>
""", unsafe_allow_html=True)

# Main Activity Tabs
tab_rhyme, tab_math, tab_letter, tab_story, tab_sound, tab_frames, tab_syn, tab_wall = st.tabs([
    "🎵 Rhyme Quest", 
    "🔢 Ten-Frame Math", 
    "🔤 Letter Match",
    "📖 Story Builder",
    "🗣️ Sound Wall",
    "📝 Writing Frames",
    "🦸 Super Synonyms",
    "🗂️ Sight Word Wall"
])

# ==========================================
# 1. RHYME QUEST (LOCKED FORM)
# ==========================================
with tab_rhyme:
    st.subheader(f"Level {st.session_state.level} Rhyme Challenge")
    q = st.session_state.current_rhyme
    st.markdown(f"### Which word rhymes with **{q['target']}**?")
    
    with st.form("rhyme_form", clear_on_submit=False):
        selected_rhyme = st.radio("Pick the rhyming partner:", q["options"], key="rhyme_radio_select")
        submit_rhyme = st.form_submit_button("Submit Rhyme 🎯")
        
        if submit_rhyme:
            if selected_rhyme in q["valid_rhymes"]:
                st.session_state.stars += 1
                st.session_state.streak += 1
                st.session_state.xp += 50
                log_milestone(st.session_state.student_name, "Rhyme Quest", f"Correct: {q['target']}->{selected_rhyme}")
                st.success(f"🎉 Correct! **{q['target']}** rhymes with **{selected_rhyme}**! (+50 XP, +1 ⭐)")
                init_rhyme_question()
                st.rerun()
            else:
                st.session_state.streak = 0
                log_milestone(st.session_state.student_name, "Rhyme Quest", f"Missed: {q['target']}->{selected_rhyme}")
                st.error(f"Not quite! Listen to the ending rime of **{q['target']}** and try again.")

# ==========================================
# 2. TEN-FRAME MATH (LOCKED FORM)
# ==========================================
with tab_math:
    st.subheader(f"Level {st.session_state.level} Ten-Frame Count")
    target_count = st.session_state.current_math_target
    st.write("Count the yellow dots in the 10-block frame:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Frame 1 (1–10):**")
        cells_1 = ["🟡" if i < min(target_count, 10) else "⬜" for i in range(10)]
        r1 = "".join([f"<div class='ten-frame-cell'>{c}</div>" for c in cells_1[:5]])
        r2 = "".join([f"<div class='ten-frame-cell'>{c}</div>" for c in cells_1[5:]])
        st.markdown(f"<div class='ten-frame-grid'>{r1}{r2}</div>", unsafe_allow_html=True)
    
    if target_count > 10:
        with col_b:
            st.markdown("**Frame 2 (11–20):**")
            rem = target_count - 10
            cells_2 = ["🟡" if i < rem else "⬜" for i in range(10)]
            r1_2 = "".join([f"<div class='ten-frame-cell'>{c}</div>" for c in cells_2[:5]])
            r2_2 = "".join([f"<div class='ten-frame-cell'>{c}</div>" for c in cells_2[5:]])
            st.markdown(f"<div class='ten-frame-grid'>{r1_2}{r2_2}</div>", unsafe_allow_html=True)

    with st.form("math_form", clear_on_submit=False):
        user_count = st.number_input("How many yellow dots did you count?", min_value=0, max_value=20, step=1, key="math_input_count")
        submit_math = st.form_submit_button("Check Count ✅")
        
        if submit_math:
            if user_count == target_count:
                st.session_state.stars += 1
                st.session_state.streak += 1
                st.session_state.xp += 50
                log_milestone(st.session_state.student_name, "Ten-Frame Math", f"Correct Count: {target_count}")
                st.success(f"🎉 Spot on! You counted **{target_count}**! (+50 XP, +1 ⭐)")
                init_math_question()
                st.rerun()
            else:
                st.session_state.streak = 0
                log_milestone(st.session_state.student_name, "Ten-Frame Math", f"Missed Count: {target_count}")
                st.error("Recount the top and bottom rows carefully and try again!")

# ==========================================
# 3. LETTER MATCH (LOCKED FORM)
# ==========================================
with tab_letter:
    st.subheader(f"Level {st.session_state.level} Uppercase to Lowercase Match")
    pair = st.session_state.current_letter_pair
    
    st.markdown(f'<div class="letter-card">{pair[0]}</div>', unsafe_allow_html=True)
    st.caption("Uppercase Target Letter")
    
    with st.form("letter_form", clear_on_submit=True):
        letter_in = st.text_input("Type the matching lowercase letter:", max_chars=1)
        submit_letter = st.form_submit_button("Check Letter 🔤")
        
        if submit_letter:
            if letter_in.strip().lower() == pair[1]:
                st.session_state.stars += 1
                st.session_state.streak += 1
                st.session_state.xp += 50
                log_milestone(st.session_state.student_name, "Letter Match", f"Matched: {pair[0]}->{pair[1]}")
                st.success(f"🎉 Perfect match! **{pair[0]}** pairs with **{pair[1]}**! (+50 XP, +1 ⭐)")
                init_letter_question()
                st.rerun()
            else:
                st.session_state.streak = 0
                log_milestone(st.session_state.student_name, "Letter Match", f"Missed: {pair[0]}")
                st.error(f"Not quite! Look at the shape of uppercase **{pair[0]}** and try again.")

# ==========================================
# 4. STORY BUILDER
# ==========================================
with tab_story:
    st.subheader("Decodable & Heart Word Story Builder")
    col1, col2, col3 = st.columns(3)
    with col1:
        chosen_heart = st.multiselect("Select Heart Words:", HEART_WORDS_LIST, default=["the", "was", "to"])
    with col2:
        chosen_decodable = st.multiselect("Select Decodable Words:", DECODABLE_WORDS_LIST, default=["can", "sit", "man"])
    with col3:
        chosen_month = st.selectbox("Select Theme Month:", list(MONTHLY_VOCAB.keys()), index=1)

    if st.button("✨ Generate Story Practice Sheet"):
        vocab = MONTHLY_VOCAB[chosen_month]
        item1 = random.choice(vocab)
        item2 = random.choice(vocab)
        
        st.info(f"""
        **{st.session_state.student_name} and the {item1.title()}**

        {st.session_state.student_name} saw **{chosen_heart[0] if chosen_heart else 'the'}** {item1} by the school path. 
        **{chosen_heart[1] if len(chosen_heart) > 1 else 'I'}** **{chosen_decodable[0] if chosen_decodable else 'can'}** see a little friend **{chosen_decodable[1] if len(chosen_decodable) > 1 else 'sit'}** nearby. 
        It **{chosen_heart[2] if len(chosen_heart) > 2 else 'was'}** a fun time to look at the **{item2}**. 
        {st.session_state.student_name} will **{chosen_decodable[2] if len(chosen_decodable) > 2 else 'man'}** the station and smile!
        """)

# ==========================================
# 5. SOUND WALL
# ==========================================
with tab_sound:
    st.subheader("Kindergarten Personal Sound Wall & Articulation Guide")
    sound_choice = st.selectbox("Select Target Phoneme Sound:", [
        "/p/ (lips together, unvoiced - pan)",
        "/b/ (lips together, voiced - bat)",
        "/t/ (tongue tap, unvoiced - taco)",
        "/d/ (tongue tap, voiced - duck)",
        "/k/ (back of tongue - kite)",
        "/g/ (back of tongue - goat)",
        "/m/ (nasal humming - mitten)",
        "/n/ (nasal tongue - nest)",
        "/ng/ (nasal back - ring)",
        "/th/ (tongue between teeth - thumb)",
        "/s/ (air hiss, unvoiced - sun)",
        "/sh/ (rounded air - shark)",
        "/ch/ (stop and push - cherry)"
    ])
    st.markdown(f"""
    <div class="card-box">
        <h4>👄 Articulation Profile for <code>{sound_choice.split()[0]}</code></h4>
        <p><b>Mouth Gesture:</b> {sound_choice.split('(')[1].replace(')', '')}</p>
        <p><b>Classroom Prompt:</b> <i>"Watch my mouth! Put your hand gently on your throat to feel if your voice box is ON (voiced) or OFF (unvoiced)."</i></p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 6. WRITING FRAMES
# ==========================================
with tab_frames:
    st.subheader("Structured Writing Scaffolds")
    genre = st.selectbox("Select Writing Genre:", ["Story-Narrative", "Opinion Writing", "Informational Text"])
    topic = st.text_input("Enter Topic:", "My Favorite Season")

    if genre == "Story-Narrative":
        st.markdown(f"""
        <div class="card-box">
            <h4>📖 Story-Narrative Structure for: {topic}</h4>
            <ul>
                <li><b>Opening Sentence:</b> Start with a sentence that gets your reader interested! Introduce the characters.</li>
                <li><b>Beginning:</b> Tell your reader where your characters are. What are they doing?</li>
                <li><b>Middle:</b> Give your character a problem. Describe what the problem is and how it happened.</li>
                <li><b>Last:</b> Have your character solve their problem. What did they do to solve it?</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif genre == "Opinion Writing":
        st.markdown(f"""
        <div class="card-box">
            <h4>💭 Opinion Writing Structure for: {topic}</h4>
            <ul>
                <li><b>Opening Sentence:</b> Tell your reader your own opinion. How you think or feel.</li>
                <li><b>First:</b> Give one reason why you feel that way. Explain with one more sentence.</li>
                <li><b>Next:</b> Give another reason why you feel that way. Explain with one more sentence.</li>
                <li><b>Last:</b> Give your last reason why you feel that way. Explain with one more sentence.</li>
                <li><b>Closing Sentence:</b> Ask a question to your reader.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card-box">
            <h4>📚 Informational Text Structure for: {topic}</h4>
            <ul>
                <li><b>Opening Sentence:</b> Tell an interesting fact or ask a question about your topic.</li>
                <li><b>First:</b> Write something you learned about your topic.</li>
                <li><b>Next:</b> What else did you learn about your topic?</li>
                <li><b>Last:</b> Give one final fact about your topic.</li>
                <li><b>Closing Sentence:</b> Ask a question about your topic.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 7. SUPER SYNONYMS
# ==========================================
with tab_syn:
    st.subheader("Super Synonyms & Sentence Stretcher")
    base_word = st.selectbox("Choose a basic word to upgrade:", list(SYNONYMS_DATA.keys()))
    st.write(f"**Instead of using `{base_word}`, use one of these:**")
    st.write(" • ".join([f"✨ **{s}**" for s in SYNONYMS_DATA[base_word]]))

# ==========================================
# 8. SIGHT WORD WALL
# ==========================================
with tab_wall:
    st.subheader("Complete A–Z Word Wall (Lists 1–14)")
    letter = st.selectbox("Select Letter of the Alphabet:", list(SIGHT_WORDS_WALL.keys()))
    words = SIGHT_WORDS_WALL[letter]
    st.markdown(f"### Words starting with **{letter}**:")
    st.write(" • ".join([f"**{w}**" for w in words]))
