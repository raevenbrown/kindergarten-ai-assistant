import streamlit as st
import random
from supabase import create_client, Client

st.set_page_config(page_title="Kindergarten Learning Studio", page_icon="⭐", layout="wide")

# --- SUPABASE CONFIGURATION ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.sidebar.warning("Supabase connection pending valid credentials.")

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

# --- ADAPTIVE LEVEL PROGRESSION ---
if st.session_state.stars >= 5 and st.session_state.level == 1:
    st.session_state.level = 2
    log_milestone(st.session_state.student_name, "Level Promotion", "Reached Level 2")
    st.balloons()
elif st.session_state.stars >= 12 and st.session_state.level == 2:
    st.session_state.level = 3
    log_milestone(st.session_state.student_name, "Level Promotion", "Reached Level 3")
    st.balloons()

# --- SIDEBAR PROFILE ---
st.sidebar.title("🎒 Student Profile")
st.session_state.student_name = st.sidebar.text_input("Student Name:", value=st.session_state.student_name)

if st.sidebar.button("🔄 Reset Progress"):
    st.session_state.xp = 0
    st.session_state.streak = 0
    st.session_state.level = 1
    st.session_state.stars = 0
    st.rerun()

# --- TOP SCOREBOARD ---
st.markdown(f"""
<div style="background: rgba(245, 158, 11, 0.08); border: 2px solid #f59e0b; padding: 18px; border-radius: 12px; display: flex; justify-content: space-around; align-items: center; margin-bottom: 24px;">
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">STUDENT LEVEL</span><br><b style="font-size: 1.4rem; color: #f59e0b;">Level {st.session_state.level} {'🌱 (Emergent)' if st.session_state.level==1 else '🌟 (On-Level)' if st.session_state.level==2 else '🚀 (Advanced)'}</b></div>
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">STARS COLLECTED</span><br><b style="font-size: 1.4rem; color: #fbbf24;">⭐ {st.session_state.stars}</b></div>
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">CURRENT STREAK</span><br><b style="font-size: 1.4rem; color: #34d399;">🔥 {st.session_state.streak}</b></div>
    <div style="text-align: center;"><span style="font-size: 0.8rem; color: #aaa;">TOTAL XP</span><br><b style="font-size: 1.4rem; color: #38bdf8;">💎 {st.session_state.xp}</b></div>
</div>
""", unsafe_allow_html=True)

# --- ADAPTIVE DATASETS ---
LEVEL_WORDS = {
    1: {"target": "CAT", "rhymes": ["hat", "bat", "mat"], "wrong": ["dog", "sun"], "math_max": 5},
    2: {"target": "HOP", "rhymes": ["mop", "top", "stop"], "wrong": ["bed", "fish", "cup", "pen"], "math_max": 10},
    3: {"target": "TRUCK", "rhymes": ["duck", "stuck", "cluck"], "wrong": ["shoe", "star", "tree", "milk"], "math_max": 20}
}
current_data = LEVEL_WORDS[st.session_state.level]

tab1, tab2, tab3 = st.tabs(["🎵 Rhyme Quest", "🔢 Ten-Frame Math Challenge", "🔤 Letter Partner Match"])

# TAB 1: RHYME QUEST
with tab1:
    st.subheader(f"Level {st.session_state.level} Rhyme Challenge")
    st.write(f"Find the word that rhymes with **{current_data['target']}**:")
    
    options = [random.choice(current_data["rhymes"])] + current_data["wrong"][:(2 if st.session_state.level==1 else 3)]
    random.shuffle(options)
    
    choice = st.radio("Select rhyming partner:", options, horizontal=True, key=f"rhyme_{st.session_state.stars}")
    
    if st.button("Submit Rhyme 🎯"):
        if choice in current_data["rhymes"]:
            st.session_state.stars += 1
            st.session_state.streak += 1
            st.session_state.xp += 50
            log_milestone(st.session_state.student_name, "Rhyme Quest", f"Correct: {choice}")
            st.success(f"🎉 Correct! {current_data['target']} rhymes with {choice}! (+50 XP, +1 ⭐)")
            st.rerun()
        else:
            st.session_state.streak = 0
            log_milestone(st.session_state.student_name, "Rhyme Quest", f"Incorrect: {choice}")
            st.error("Not quite! Listen closely to the ending sound.")

# TAB 2: TEN-FRAME COUNT
with tab2:
    st.subheader(f"Level {st.session_state.level} Ten-Frame Count")
    target_count = random.randint(1, current_data["math_max"])
    st.write("Count the yellow dots in the frame:")
    
    cells = ["🟡" if i < min(target_count, 10) else "⬜" for i in range(10)]
    r1 = "".join([f"<div style='border:2px solid #f59e0b; width:45px; height:45px; display:inline-flex; align-items:center; justify-content:center; margin:2px; font-size:1.4rem;'>{c}</div>" for c in cells[:5]])
    r2 = "".join([f"<div style='border:2px solid #f59e0b; width:45px; height:45px; display:inline-flex; align-items:center; justify-content:center; margin:2px; font-size:1.4rem;'>{c}</div>" for c in cells[5:]])
    st.markdown(f"<div>{r1}<br>{r2}</div>", unsafe_allow_html=True)
    
    math_ans = st.number_input("How many counters do you see?", min_value=0, max_value=20, step=1, key=f"math_{st.session_state.stars}")
    if st.button("Check Count ✅"):
        if math_ans == target_count:
            st.session_state.stars += 1
            st.session_state.streak += 1
            st.session_state.xp += 50
            log_milestone(st.session_state.student_name, "Ten-Frame Math", f"Counted: {target_count}")
            st.success("🎉 Spot on! Great counting! (+50 XP, +1 ⭐)")
            st.rerun()
        else:
            st.session_state.streak = 0
            log_milestone(st.session_state.student_name, "Ten-Frame Math", "Incorrect Count")
            st.error("Recount the top and bottom rows carefully!")

# TAB 3: LETTER MATCH
with tab3:
    st.subheader(f"Level {st.session_state.level} Uppercase to Lowercase Match")
    alphabet = [("B", "b"), ("D", "d"), ("G", "g"), ("M", "m"), ("R", "r"), ("Q", "q")]
    pair = random.choice(alphabet)
    
    st.markdown(f"<div style='font-size:3rem; font-weight:800; color:#f59e0b;'>{pair[0]}</div>", unsafe_allow_html=True)
    letter_guess = st.text_input("Type the matching lowercase letter:", key=f"let_{st.session_state.stars}")
    
    if st.button("Check Letter 🔤"):
        if letter_guess.strip().lower() == pair[1]:
            st.session_state.stars += 1
            st.session_state.streak += 1
            st.session_state.xp += 50
            log_milestone(st.session_state.student_name, "Letter Match", f"Matched: {pair[0]}->{pair[1]}")
            st.success(f"🎉 Perfect match! {pair[0]} -> {pair[1]} (+50 XP, +1 ⭐)")
            st.rerun()
        else:
            log_milestone(st.session_state.student_name, "Letter Match", f"Missed: {pair[0]}")
            st.error(f"Look at the shape of {pair[0]} and try again.")
