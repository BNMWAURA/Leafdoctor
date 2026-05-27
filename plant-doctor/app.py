import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.styles import inject_css
from utils.history import load_history
from utils.disease_db import DISEASE_DB

st.set_page_config(
    page_title="AI Crop Doctor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-banner">
        <h1>🌿 AI Crop Doctor</h1>
        <p>Intelligent Plant Disease Detection & Smart Farming Platform</p>
        <p style="font-size:0.85rem;margin-top:6px;opacity:0.75;">
            Serving farmers across Africa and beyond · Powered by TensorFlow AI
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Quick stats ───────────────────────────────────────────────────────────────
history = load_history()
total_scans  = len(history)
disease_hits = sum(1 for h in history if not h.get("is_healthy", True))
crops_count  = len(DISEASE_DB)
diseases_count = sum(len(v["diseases"]) - 1 for v in DISEASE_DB.values())  # exclude Healthy entries

c1, c2, c3, c4 = st.columns(4)
for col, val, label in [
    (c1, total_scans,    "Total Scans"),
    (c2, disease_hits,   "Diseases Found"),
    (c3, crops_count,    "Supported Crops"),
    (c4, diseases_count, "Disease Classes"),
]:
    col.markdown(
        f"""<div class="stat-card">
            <div class="stat-value">{val}</div>
            <div class="stat-label">{label}</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🚀 Platform Features</div>', unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)
features = [
    ("🔬", "Crop Doctor",     "Upload any leaf photo for instant AI-powered disease diagnosis with confidence scores."),
    ("🤖", "AI Assistant",    "Chat with your personal farming expert — fertiliser, pests, irrigation, weather advice."),
    ("📊", "Analytics",       "Visualise your scan history with charts showing disease trends and crop health stats."),
    ("📚", "Disease Library", "Browse the encyclopaedia of 13 crops and their diseases with treatment protocols."),
]
for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
    col.markdown(
        f"""<div class="feature-card">
            <div class="feat-icon">{icon}</div>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Supported crops ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🌾 Supported Crops</div>', unsafe_allow_html=True)

crop_cols = st.columns(7)
crop_items = [(info["icon"], crop) for crop, info in DISEASE_DB.items()]
for i, (icon, crop) in enumerate(crop_items):
    crop_cols[i % 7].markdown(
        f"""<div style="text-align:center;padding:10px 4px;background:#e8f5e9;
            border-radius:10px;margin:4px 0;border:1px solid #c8e6c9;">
            <div style="font-size:1.6rem">{icon}</div>
            <div style="font-size:0.75rem;color:#2e7d32;font-weight:600;margin-top:2px">{crop}</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Recent scans preview ──────────────────────────────────────────────────────
if history:
    st.markdown('<div class="section-header">🕑 Recent Scans</div>', unsafe_allow_html=True)
    recent = history[-5:][::-1]
    for entry in recent:
        ts    = entry["timestamp"][:16].replace("T", " ")
        crop  = entry.get("crop", "Unknown")
        dis   = entry.get("disease", "Unknown")
        conf  = entry.get("confidence", 0)
        badge = (
            '<span class="badge-healthy">✅ Healthy</span>'
            if entry.get("is_healthy")
            else '<span class="badge-disease">🦠 Disease</span>'
        )
        st.markdown(
            f"""<div class="glass-card" style="padding:0.8rem 1.2rem;">
                <span style="color:#888;font-size:0.8rem">{ts}</span>&nbsp;&nbsp;
                {badge}&nbsp;&nbsp;
                <strong>{crop}</strong> — {dis}
                &nbsp;<span style="color:#888;font-size:0.82rem">({conf:.1f}% confidence)</span>
            </div>""",
            unsafe_allow_html=True,
        )
else:
    st.info("No scans yet. Head to **🔬 Crop Doctor** in the sidebar to analyse your first plant!", icon="👈")

# ── Sidebar nav hint ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 AI Crop Doctor")
    st.markdown("Navigate using the pages above ☝️")
    st.divider()
    st.markdown("**Quick start:**")
    st.markdown("1. Open **🔬 Crop Doctor**")
    st.markdown("2. Upload your `.keras` model")
    st.markdown("3. Upload `class_indices.json`")
    st.markdown("4. Take a leaf photo and scan!")
    st.divider()
    st.caption("v1.0 · AI Crop Doctor · © 2024")
