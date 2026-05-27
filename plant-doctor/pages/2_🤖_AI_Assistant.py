"""AI Farming Assistant — farming chatbot with knowledge base."""
import streamlit as st
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import inject_css
from utils.disease_db import get_bot_response

st.set_page_config(page_title="AI Assistant · Thiru Mkulima AI", page_icon="🤖", layout="centered")
inject_css()

with st.sidebar:
    st.markdown("### 🌿 Thiru Mkulima AI")
    st.divider()
    st.page_link("app.py",                       label="🔬 Detect Disease")
    st.page_link("pages/1_📊_Dashboard.py",       label="📊 Analytics")
    st.page_link("pages/2_🤖_AI_Assistant.py",    label="🤖 AI Assistant")
    st.page_link("pages/3_📚_Disease_Library.py", label="📚 Disease Library")
    st.divider()
    st.markdown("**💡 Quick Questions**")
    quick_qs = [
        "How do I fertilise tomatoes?",
        "What causes maize rust?",
        "Irrigation tips for dry season",
        "How to prevent potato late blight?",
        "Best practices for pest control?",
        "When should I harvest beans?",
        "How to improve soil pH?",
        "Tell me about coffee leaf rust",
        "How to manage banana black sigatoka?",
        "Cassava mosaic disease treatment",
    ]
    for q in quick_qs:
        if st.button(q, use_container_width=True, key=f"q_{q}"):
            st.session_state.setdefault("chat", [])
            st.session_state.chat.append({"role": "user", "text": q})
            st.session_state.chat.append({"role": "bot",  "text": get_bot_response(q)})
            st.rerun()
    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.chat = []
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-title" style="font-size:2rem">🤖 AI Farming Assistant</div>
    <div class="app-subtitle">Your intelligent crop advisor — ask anything</div>
</div>
""", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = [{
        "role": "bot",
        "text": (
            "**Habari! 👋 Welcome to Thiru Mkulima AI Assistant!**\n\n"
            "I'm your AI farming expert. Ask me about:\n\n"
            "🌱 **Fertiliser** · 💧 **Irrigation** · 🐛 **Pests** · "
            "🛡️ **Disease prevention** · 🌾 **Harvest** · 🏔️ **Soil** · "
            "🌤️ **Weather** · specific **crop diseases**\n\n"
            "Type your question below or pick one from the sidebar ☝️"
        ),
    }]

for msg in st.session_state.chat:
    cls = "chat-msg-user" if msg["role"] == "user" else "chat-msg-bot"
    prefix = "👤" if msg["role"] == "user" else "🌿"
    st.markdown(
        f'<div class="{cls}">{prefix}&nbsp; {msg["text"]}</div>',
        unsafe_allow_html=True,
    )

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    ic, bc = st.columns([5, 1])
    user_input = ic.text_input(
        "message",
        placeholder="Ask your farming question… (e.g. 'How do I treat tomato early blight?')",
        label_visibility="collapsed",
    )
    send = bc.form_submit_button("Send →", use_container_width=True)

if send and user_input.strip():
    st.session_state.chat.append({"role": "user", "text": user_input.strip()})
    st.session_state.chat.append({"role": "bot",  "text": get_bot_response(user_input.strip())})
    st.rerun()

st.markdown(
    '<div style="text-align:center;color:#6e7681;font-size:0.78rem;margin-top:1rem">'
    '🌍 Supports English & Swahili · More languages coming soon</div>',
    unsafe_allow_html=True,
)
