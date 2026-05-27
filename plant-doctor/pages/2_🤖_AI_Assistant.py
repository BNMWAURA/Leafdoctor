import streamlit as st
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import inject_css
from utils.disease_db import get_chat_response

st.set_page_config(page_title="AI Assistant · AI Crop Doctor", page_icon="🤖", layout="wide")
inject_css()

st.markdown(
    '<div class="hero-banner" style="padding:1.5rem 2rem;">'
    '<h1 style="font-size:1.8rem">🤖 AI Farming Assistant</h1>'
    '<p>Your personal crop expert — ask anything about farming, pests, disease, and more</p>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Sidebar quick-start prompts ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💡 Quick Questions")
    quick = [
        "How do I fertilise tomatoes?",
        "What causes maize rust?",
        "How to manage irrigation in dry season?",
        "How to prevent potato late blight?",
        "Best practices for pest control?",
        "When should I harvest beans?",
        "How to improve soil pH?",
        "Tell me about coffee leaf rust",
    ]
    for q in quick:
        if st.button(q, use_container_width=True, key=f"quick_{q}"):
            st.session_state.setdefault("chat_history", [])
            st.session_state.chat_history.append({"role": "user", "content": q})
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": get_chat_response(q),
            })
            st.rerun()

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ── Init chat ─────────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "👋 **Habari! Hello! Welcome to AI Crop Doctor Assistant!**\n\n"
                "I'm your personal farming expert. I can help you with:\n\n"
                "🌱 **Fertiliser & nutrition** · 💧 **Irrigation management** · "
                "🐛 **Pest control** · 🛡️ **Disease prevention** · "
                "🌾 **Harvest timing** · 🏔️ **Soil management** · 🌤️ **Weather planning**\n\n"
                "**Just type your question below** — or pick a quick question from the sidebar!"
            ),
        }
    ]

# ── Render chat history ───────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user">👤 {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-bot">🌿 {msg["content"]}</div>',
                unsafe_allow_html=True,
            )

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([5, 1])
    user_input = col_input.text_input(
        "Ask your farming question…",
        placeholder="e.g. How do I treat tomato early blight?",
        label_visibility="collapsed",
    )
    send = col_btn.form_submit_button("Send 📨", use_container_width=True)

if send and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
    response = get_chat_response(user_input.strip())
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()

# ── Language note ─────────────────────────────────────────────────────────────
st.caption("🌍 Supports English & Swahili questions · More languages coming soon")
