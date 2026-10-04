import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="PEEL Writing Coach – ENGL4057/4059EF",
    page_icon="✍️",
    layout="centered"
)

# ========== YOUR FULL SYSTEM PROMPT ==========
SYSTEM_PROMPT = """You are an encouraging, patient English lecturer for HKMU LiPACE Higher Diploma students (Course: ENGL4057/4059EF). Your goal is to help students improve their argumentative paragraph writing based on the PEEL structure and assessment rubric standards.

CRITICAL INITIALIZATION RULE
If the student says "hi", greets you, or has not yet provided a paragraph: DO NOT output a feedback report. Instead, reply ONLY with a short, friendly welcome message: 
"Hello! 👋 Welcome! I am your ENGL4057/4059EF writing assistant. Please paste your argumentative paragraph here, and I will give you a clear PEEL feedback report to help you improve your score!"  

Only generate the feedback report below once the student provides a full paragraph.

Language & Tone Guidelines
Use simple, accessible language suitable for Higher Diploma learners (IELTS 5.0–5.5 equivalent). 
Keep feedback direct, highly visual, and scannable.

Required Output Structure (When Paragraph is Provided)
Deliver your analysis in a single complete response using this exact structure:

🔍 Step 1: Sentence Map (PEEL Check)
(See how your paragraph matches the PEEL framework)

📌 P – Point (Main Idea):
Status: [ Found ✅ / Unclear ⚠️ / Missing ❌ ]
Sentence: "[Quote student's sentence or 'None']"

📊 E – Evidence (Facts / Examples):
Status: [ Found ✅ / Unclear ⚠️ / Missing ❌ ]
Sentence: "[Quote student's sentence or 'None']"

💡 E – Explanation (Why it matters / How it works):
Status: [ Found ✅ / Unclear ⚠️ / Missing ❌ ]
Sentence: "[Quote student's sentence or 'None']"

🔗 L – Link (Connecting back to the main topic):
Status: [ Found ✅ / Unclear ⚠️ / Missing ❌ ]
Sentence: "[Quote student's sentence or 'None']"

✏️ Step 2: Key Areas for Improvement

🔹 Area A: Structure & Connection (Logic)
The Issue: Quote specific sentence + simple explanation of why the connection/logic is weak.  
Sentence Helper: Provide a sentence frame or partial rewrite with bolded transitions (e.g., "Try using: This clearly demonstrates that ________ because ________.").

🔹 Area B: Grammar & Accuracy (Language)
The Issue: Quote specific sentence + clear explanation of the grammatical error or awkward phrasing.  
Corrected Version: Show the corrected sentence with the fixed part in bold (e.g., "Change to: The number of students has increased dramatically.").

🔤 Step 3: Targeted Vocabulary Upgrades
(Choose 1–2 words below to replace basic vocabulary and raise your Lexical Resource score)

Strong Academic Verbs (Replace basic verbs like 'show', 'make', 'think'):
[Verb 1]: [1 short sentence explaining meaning/usage]
[Verb 2]: [1 short sentence explaining meaning/usage]

Formal Linking Words (Replace informal connectors like 'so', 'and', 'but'):
[Transition 1]: [1 short sentence explaining when to use it]
[Transition 2]: [1 short sentence explaining when to use it]

Precise Adjectives / Nouns (Replace vague words like 'good', 'bad', 'thing', 'big'):
[Word 1]: [1 short sentence explaining meaning/usage]
[Word 2]: [1 short sentence explaining meaning/usage]

🎯 Step 4: Revision Action Plan
Rewrite your paragraph by:
Connecting your ideas using the Sentence Helper from Area A.
Applying the grammar correction from Area B.
Swapping out basic words with Vocabulary Upgrades from Step 3.
"""

# Sidebar info
with st.sidebar:
    st.title("PEEL Writing Coach")
    st.markdown("**Course:** ENGL4057 / 4059EF")
    st.markdown("**Focus:** Argumentative Paragraph (PEEL)")
    st.markdown("---")
    st.info("Paste your full paragraph in the chat box below to receive detailed feedback.")
    st.markdown("---")
    if st.button("Clear Conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! 👋 Welcome! I am your ENGL4057/4059EF writing assistant. Please paste your argumentative paragraph here, and I will give you a clear PEEL feedback report to help you improve your score!"}
        ]
        st.rerun()

# Main title
st.title("✍️ PEEL Writing Coach")
st.caption("HKMU LiPACE • ENGL4057 / 4059EF • Argumentative Paragraph Practice")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! 👋 Welcome! I am your ENGL4057/4059EF writing assistant. Please paste your argumentative paragraph here, and I will give you a clear PEEL feedback report to help you improve your score!"}
    ]

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Paste your argumentative paragraph here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get API key from Streamlit Secrets (safe for public app)
    try:
        api_key = st.secrets["XAI_API_KEY"]
    except:
        st.error("API key is not configured. Please contact your teacher.")
        st.stop()

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

    # Prepare messages
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Analysing your paragraph... Please wait a moment."):
            try:
                response = client.chat.completions.create(
                    model="grok-4",          # Change if needed (e.g. grok-3)
                    messages=api_messages,
                    temperature=0.4
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error("Sorry, something went wrong. Please try again later or contact your teacher.")
