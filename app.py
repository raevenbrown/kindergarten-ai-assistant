import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Adventure Academy Kids",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- VIBRANT KHAN KIDS / HATCH IGNITE CSS THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700;800&family=Quicksand:wght@600;700;800&display=swap');

    /* Global Arcade Canvas */
    .stApp {
        background: linear-gradient(180deg, #38bdf8 0%, #6ee7b7 55%, #fef08a 100%) !important;
        font-family: 'Fredoka', 'Quicksand', cursive, sans-serif !important;
    }

    /* Tactile Child-Friendly Touch Buttons */
    .stButton > button {
        border-radius: 30px !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        padding: 18px 28px !important;
        background: #ffffff !important;
        color: #0369a1 !important;
        border: 4px solid #38bdf8 !important;
        box-shadow: 0 10px 0 #0284c7, 0 15px 25px rgba(0,0,0,0.15) !important;
        transition: transform 0.08s ease, box-shadow 0.08s ease !important;
        margin: 8px 0 !important;
    }
    .stButton > button:hover {
        background: #f0f9ff !important;
        color: #0284c7 !important;
        border-color: #0284c7 !important;
    }
    .stButton > button:active {
        transform: translateY(8px) !important;
        box-shadow: 0 2px 0 #0284c7 !important;
    }

    /* Top HUD Ribbon */
    .hud-banner {
        background: #ffffff;
        border-radius: 32px;
        padding: 16px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 4px solid #facc15;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        margin-bottom: 20px;
    }
    .hud-stat {
        background: #fef08a;
        color: #854d0e;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 1.3rem;
        font-weight: 800;
        border: 2px solid #facc15;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Mascot Speech Card */
    .mascot-card {
        background: #ffffff;
        border-radius: 32px;
        padding: 20px 26px;
        border: 4.5px solid #38bdf8;
        box-shadow: 0 14px 28px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 22px;
    }
    .mascot-avatar {
        font-size: 4.5rem;
        background: #ecfeff;
        border: 3.5px solid #38bdf8;
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
        0% { transform: translateY(0px) rotate(-4deg); }
        100% { transform: translateY(-8px) rotate(4deg); }
    }
    .mascot-prompt {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.35;
    }

    /* Center Play Arena Card */
    .play-card {
        background: #ffffff;
        border-radius: 36px;
        padding: 28px;
        text-align: center;
        border: 5px solid #60a5fa;
        box-shadow: 0 16px 36px rgba(0,0,0,0.12);
        margin-bottom: 24px;
    }

    /* Non-Punitive Scaffolding Clue Box */
    .hint-box {
        background: #fffbeb;
        border: 4px dashed #f59e0b;
        border-radius: 26px;
        padding: 18px 22px;
        text-align: center;
        margin-top: 18px;
        animation: popHint 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes popHint {
        0% { transform: scale(0.92); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# --- ZERO-DEPENDENCY WEBAUDIO SPEECH SYNTHESIZER ---
def speak(text):
    clean_text = text.replace('"', '\\"').replace("'", "\\'")
    js = f"""
    <script>
        (function() {{
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
            utter.pitch = 1.25;
            utter.lang = 'en-US';

            const voices = synth.getVoices();
            if (voices && voices.length > 0) {{
                const pref = voices.find(v => (v.name.includes("Samantha") || v.name.includes("Victoria") || v.lang === "en-US") && !v.name.includes("Bad"));
                if (pref) utter.voice = pref;
            }}
            synth.speak(utter);
        }})();
    </script>
    """
    components.html(js, height=0)

# --- CURRICULUM QUESTION REPOSITORY (PHONICS, SIGHT WORDS, MATH) ---
QUESTIONS = [
    {
        "id": "q1",
        "domain": "Early Phonics",
        "instruction": "Look at uppercase letter A! Which baby lowercase letter matches it?",
        "prompt_visual": "🅰️",
        "options": [
            {"label": "a", "display": "a"},
            {"label": "b", "display": "b"},
            {"label": "d", "display": "d"}
        ],
        "correct": "a",
        "hint": "Letter A says 'ah' like in 🍎 apple! Look for the round circle with a short tail: 'a'."
    },
    {
        "id": "q2",
        "domain": "Object Counting",
        "instruction": "Count the yummy strawberries! How many are on the plate?",
        "prompt_visual": "🍓 🍓 🍓 🍓",
        "options": [
            {"label": "2", "display": "2"},
            {"label": "4", "display": "4"},
            {"label": "5", "display": "5"}
        ],
        "correct": "4",
        "hint": "Touch and count each berry slowly: 1... 2... 3... 4!"
    },
    {
        "id": "q3",
        "domain": "Sight Words",
        "instruction": "Which word says 'THE'?",
        "prompt_visual": "📖 T - H - E",
        "options": [
            {"label": "the", "display": "the"},
            {"label": "and", "display": "and"},
            {"label": "was", "display": "was"}
        ],
        "correct": "the",
        "hint": "Look for the letters that start with tall letter T and H: 'the'!"
    },
    {
        "id": "q4",
        "domain": "Kindergarten Math",
        "instruction": "What is 2 apples plus 1 apple?",
        "prompt_visual": "🍎 🍎 + 🍏",
        "options": [
            {"label": "2", "display": "2"},
            {"label": "3", "display": "3"},
            {"label": "4", "display": "4"}
        ],
        "correct": "3",
        "hint": "Count all the apples together: 1, 2, and 1 more makes 3!"
    }
]

# --- GAME STATE MANAGEMENT ---
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "stars_earned" not in st.session_state:
    st.session_state.stars_earned = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "show_hint" not in st.session_state:
    st.session_state.show_hint = False
if "telemetry_log" not in st.session_state:
    st.session_state.telemetry_log = []
if "last_spoken_id" not in st.session_state:
    st.session_state.last_spoken_id = None

current_idx = st.session_state.current_question_index % len(QUESTIONS)
current_q = QUESTIONS[current_idx]

# Auto-speak question on transition
if st.session_state.last_spoken_id != f"{current_q['id']}_{st.session_state.show_hint}":
    if st.session_state.show_hint:
        speak(f"Let's look at the clue: {current_q['hint']}")
    else:
        speak(current_q["instruction"])
    st.session_state.last_spoken_id = f"{current_q['id']}_{st.session_state.show_hint}"

# --- TOP HUD DISPLAY ---
st.markdown(f"""
<div class="hud-banner">
    <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:2.2rem;">🚀</span>
        <b style="font-size:1.5rem; color:#0f172a;">Level {st.session_state.current_question_index + 1}</b>
    </div>
    <div style="display:flex; gap:12px;">
        <div class="hud-stat">⭐ {st.session_state.stars_earned} Stars</div>
        <div class="hud-stat" style="background:#fee2e2; color:#b91c1c; border-color:#f87171;">🔥 {st.session_state.streak} Streak</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- MASCOT GUIDE BANNER ---
st.markdown(f"""
<div class="mascot-card">
    <div class="mascot-avatar">🐥</div>
    <div class="mascot-prompt">
        <span style="color:#0284c7; font-size:1.1rem; text-transform:uppercase; letter-spacing:1px;">{current_q['domain']}</span><br>
        {current_q['instruction']}
    </div>
</div>
""", unsafe_allow_html=True)

# --- PLAY ARENA ---
st.markdown(f"""
<div class="play-card">
    <div style="font-size: 5rem; letter-spacing: 8px; margin: 10px 0;">{current_q['prompt_visual']}</div>
</div>
""", unsafe_allow_html=True)

# --- ANSWER CHECKER FUNCTION ---
def handle_choice(selected_value):
    is_correct = (selected_value == current_q["correct"])
    now_str = datetime.now().strftime("%I:%M:%S %p")

    if is_correct:
        st.session_state.stars_earned += 1
        st.session_state.streak += 1
        st.session_state.show_hint = False
        st.session_state.current_question_index += 1
        st.session_state.telemetry_log.append({
            "time": now_str,
            "question": current_q["id"],
            "domain": current_q["domain"],
            "result": "Correct (+1 ⭐)",
            "streak": st.session_state.streak
        })
        st.balloons()
        st.rerun()
    else:
        # Non-punitive: Never deduct stars or drop level
        st.session_state.streak = 0
        st.session_state.show_hint = True
        st.session_state.telemetry_log.append({
            "time": now_str,
            "question": current_q["id"],
            "domain": current_q["domain"],
            "result": "Hint Triggered (No Penalty)",
            "streak": 0
        })
        st.rerun()

# --- INTERACTIVE TACTILE BUTTON TARGETS ---
cols = st.columns(len(current_q["options"]))
for i, opt in enumerate(current_q["options"]):
    with cols[i]:
        if st.button(f"👉  {opt['display']}", key=f"btn_{current_q['id']}_{opt['label']}", use_container_width=True):
            handle_choice(opt["label"])

# --- GENTLE VISUAL CLUE BOX (ON MISS) ---
if st.session_state.show_hint:
    st.markdown(f"""
    <div class="hint-box">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">💡 Gentle Clue:</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #78350f;">{current_q['hint']}</div>
    </div>
    """, unsafe_allow_html=True)

# --- EDUCATOR & PARENT TELEMETRY DASHBOARD ---
st.markdown("---")
with st.expander("📊 Parent & Teacher Live Dashboard", expanded=False):
    m1, m2, m3 = st.columns(3)
    total_answered = len(st.session_state.telemetry_log)
    correct_count = sum(1 for entry in st.session_state.telemetry_log if "Correct" in entry["result"])
    accuracy = int((correct_count / total_answered) * 100) if total_answered > 0 else 100

    m1.metric("Questions Practiced", total_answered)
    m2.metric("Total Stars", f"⭐ {st.session_state.stars_earned}")
    m3.metric("First-Try Accuracy", f"{accuracy}%")

    st.markdown("#### 📝 Live Session Activity Stream:")
    if st.session_state.telemetry_log:
        for item in reversed(st.session_state.telemetry_log):
            st.write(f"• **{item['time']}** — [{item['domain']}] Question `{item['question']}`: **{item['result']}**")
    else:
        st.info("No answers logged yet. Tap an answer choice to record real-time telemetry!")
