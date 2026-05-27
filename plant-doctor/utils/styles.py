import streamlit as st


def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Complete reset for mobile-app feel ──────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* Hide all Streamlit chrome */
header[data-testid="stHeader"],
section[data-testid="stSidebar"],
[data-testid="collapsedControl"],
#MainMenu, footer, .stDeployButton { display: none !important; }

/* Main container — mobile first, centered */
.block-container {
    max-width: 480px !important;
    padding: 0 0 88px 0 !important;
    margin: 0 auto !important;
}
section.main { background: #080f09 !important; }

/* ── Scrollbar ─────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #22c55e33; border-radius: 2px; }

/* ── Bottom navigation (activated by JS adding .nav-fixed class) ──────── */
.nav-fixed {
    position: fixed !important;
    bottom: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 480px !important;
    background: rgba(8,15,9,0.97) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border-top: 1px solid rgba(34,197,94,0.18) !important;
    z-index: 9999 !important;
    padding: 4px 4px 22px !important;
    box-shadow: 0 -4px 30px rgba(0,0,0,0.6) !important;
    gap: 0 !important;
}
.nav-fixed > div[data-testid="column"] {
    padding: 0 !important;
    min-width: 0 !important;
}
.nav-fixed button {
    background: transparent !important;
    border: none !important;
    color: #4b6050 !important;
    font-size: 0.62rem !important;
    font-weight: 500 !important;
    padding: 6px 2px 4px !important;
    border-radius: 12px !important;
    transition: all 0.2s !important;
    white-space: pre-line !important;
    line-height: 1.4 !important;
    min-height: 56px !important;
    letter-spacing: 0.2px !important;
}
.nav-fixed button:hover {
    background: rgba(34,197,94,0.08) !important;
    color: #22c55e !important;
}
.nav-fixed button.nav-active {
    color: #22c55e !important;
    background: rgba(34,197,94,0.1) !important;
}

/* ── Card / glass ──────────────────────────────────────────────────────── */
.card {
    background: #0e1a0f;
    border: 1px solid #1a2e1c;
    border-radius: 16px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 0.7rem;
}
.card-alt {
    background: #0a120b;
    border: 1px solid rgba(34,197,94,0.12);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.6rem;
}
.glass {
    background: rgba(14,26,15,0.7);
    border: 1px solid rgba(34,197,94,0.15);
    border-radius: 16px;
    padding: 1.2rem;
    backdrop-filter: blur(10px);
}

/* ── Stat row ──────────────────────────────────────────────────────────── */
.stat-chip {
    background: #0e1a0f;
    border: 1px solid #1a2e1c;
    border-radius: 12px;
    padding: 0.8rem 0.7rem;
    text-align: center;
}
.stat-chip .val { font-size: 1.5rem; font-weight: 800; color: #22c55e; line-height: 1; }
.stat-chip .lbl { font-size: 0.7rem; color: #4b6050; margin-top: 3px; }

/* ── Section header ────────────────────────────────────────────────────── */
.sec-head {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #4b6050;
    margin: 1.2rem 0 0.6rem;
    padding: 0 12px;
}

/* ── Tip card ──────────────────────────────────────────────────────────── */
.tip-card {
    background: linear-gradient(135deg, #0b1e0d, #0e2510);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    border-left: 3px solid #22c55e;
}
.tip-card .tip-icon { font-size: 1.4rem; margin-bottom: 5px; }
.tip-card .tip-title { color: #a3e635; font-weight: 700; font-size: 0.88rem; margin-bottom: 3px; }
.tip-card .tip-body  { color: #6e8a72; font-size: 0.82rem; line-height: 1.5; }

/* ── FAB (floating action button) ─────────────────────────────────────── */
div[data-testid="stButton"] > button.fab-btn {
    background: linear-gradient(135deg,#16a34a,#22c55e) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 50px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 1rem 2rem !important;
    box-shadow: 0 6px 30px rgba(34,197,94,0.45) !important;
    width: 100% !important;
}

/* ── Primary button ────────────────────────────────────────────────────── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg,#16a34a,#22c55e) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 20px rgba(34,197,94,0.35) !important;
    transition: all .2s !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(34,197,94,0.5) !important;
}

/* ── Image preview with scan ───────────────────────────────────────────── */
@keyframes scan-sweep {
    0%   { top: 0; opacity: 1; }
    100% { top: 100%; opacity: 0.2; }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-glow {
    0%,100% { box-shadow: 0 0 0 0 rgba(34,197,94,.3); }
    50%      { box-shadow: 0 0 0 10px rgba(34,197,94,0); }
}

.img-preview-wrap {
    position: relative;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #1a2e1c;
}
.img-scan-line {
    position: absolute; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg,transparent,#22c55e,#4ade80,#22c55e,transparent);
    box-shadow: 0 0 10px #22c55e;
    animation: scan-sweep 1.8s ease-in-out infinite;
    z-index: 5;
}

/* ── Result card ───────────────────────────────────────────────────────── */
.res-healthy {
    background: linear-gradient(135deg,#031a08,#052e12);
    border: 1px solid #22c55e44;
    border-radius: 18px;
    padding: 1.4rem;
    animation: fadeUp .4s ease;
    box-shadow: 0 0 40px rgba(34,197,94,.07);
}
.res-disease {
    background: linear-gradient(135deg,#1c0800,#2d1200);
    border: 1px solid #f9731655;
    border-radius: 18px;
    padding: 1.4rem;
    animation: fadeUp .4s ease;
    box-shadow: 0 0 40px rgba(249,115,22,.07);
}
.res-badge {
    display: inline-block;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: .7rem;
}
.res-name { font-size: 1.5rem; font-weight: 800; color: #f0f6fc; margin-bottom: 2px; }
.res-crop { font-size: .85rem; color: #6e7681; margin-bottom: 1rem; }

/* ── Info grid 2-col ───────────────────────────────────────────────────── */
.info-grid2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: .7rem;
    margin-top: .8rem;
}
.info-cell2 {
    background: rgba(0,0,0,.35);
    border: 1px solid #1a2e1c;
    border-radius: 10px;
    padding: .8rem .9rem;
}
.info-cell2 .lbl { font-size:.67rem;color:#4b6050;letter-spacing:1px;text-transform:uppercase;font-weight:600;margin-bottom:3px; }
.info-cell2 .val { font-size:.83rem;color:#c9d1d9;line-height:1.35; }

/* ── Info block list ───────────────────────────────────────────────────── */
.info-blk {
    background: rgba(0,0,0,.25);
    border: 1px solid #1a2e1c;
    border-radius: 10px;
    padding: .9rem 1rem;
    margin-top: .6rem;
}
.info-blk .blk-lbl {
    font-size:.67rem;color:#4b6050;letter-spacing:1px;
    text-transform:uppercase;font-weight:600;margin-bottom:7px;
}
.info-blk ul { margin:0;padding-left:1.2rem;color:#8c9a8e;font-size:.84rem;line-height:1.8; }

/* ── Confidence ring ───────────────────────────────────────────────────── */
.conf-wrap {
    display: flex; align-items: center; gap: 1rem;
    background: rgba(0,0,0,.3);
    border: 1px solid #1a2e1c;
    border-radius: 12px;
    padding: .9rem 1.1rem;
}
.conf-ring { position:relative;width:72px;height:72px;flex-shrink:0; }
.conf-ring svg { transform: rotate(-90deg); }
.conf-info { flex:1; }
.conf-lbl { font-size:.68rem;color:#4b6050;text-transform:uppercase;letter-spacing:1px;font-weight:600;margin-bottom:5px; }
.conf-bar-t { background:#0d1117;border-radius:5px;height:7px;overflow:hidden; }
.conf-bar-f { height:100%;border-radius:5px;transition:width 1s; }

/* ── Chat bubbles ──────────────────────────────────────────────────────── */
.bubble-user {
    background: #1a3a20;
    border-radius: 18px 18px 4px 18px;
    padding: .75rem 1rem;
    margin: .5rem 0 .5rem 15%;
    font-size: .88rem;
    color: #d4fde4;
    border: 1px solid rgba(34,197,94,.2);
    word-break: break-word;
}
.bubble-bot {
    background: #0e1a0f;
    border-radius: 18px 18px 18px 4px;
    padding: .75rem 1rem;
    margin: .5rem 15% .5rem 0;
    font-size: .88rem;
    color: #c9d1d9;
    border: 1px solid #1a2e1c;
    border-left: 3px solid #22c55e;
    word-break: break-word;
}

/* ── History item ──────────────────────────────────────────────────────── */
.hist-item {
    display: flex;
    align-items: center;
    gap: .8rem;
    background: #0e1a0f;
    border: 1px solid #1a2e1c;
    border-radius: 14px;
    padding: .85rem 1rem;
    margin-bottom: .5rem;
}
.hist-dot-h { width:10px;height:10px;border-radius:50%;background:#22c55e;flex-shrink:0; }
.hist-dot-d { width:10px;height:10px;border-radius:50%;background:#f97316;flex-shrink:0; }
.hist-body { flex:1;min-width:0; }
.hist-name { font-size:.88rem;font-weight:600;color:#e6edf3;
             white-space:nowrap;overflow:hidden;text-overflow:ellipsis; }
.hist-meta { font-size:.74rem;color:#4b6050;margin-top:2px; }
.hist-conf { font-size:.82rem;font-weight:700;flex-shrink:0; }

/* ── Toggle (profile) ──────────────────────────────────────────────────── */
.profile-item {
    display: flex;
    align-items: center;
    gap: .9rem;
    background: #0e1a0f;
    border: 1px solid #1a2e1c;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: .5rem;
}
.profile-icon { font-size: 1.4rem; flex-shrink:0; }
.profile-label { flex:1; color:#e6edf3; font-size:.9rem; font-weight:500; }
.profile-sub { color:#4b6050; font-size:.76rem; margin-top:2px; }

/* ── Upload zone ───────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] section {
    background: #0e1a0f !important;
    border: 2px dashed #1a2e1c !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #22c55e !important;
}

/* ── Camera input ──────────────────────────────────────────────────────── */
[data-testid="stCameraInput"] {
    border-radius: 14px !important;
    overflow: hidden !important;
}
[data-testid="stCameraInput"] > div {
    border-radius: 14px !important;
    border: 2px solid #1a2e1c !important;
    background: #0e1a0f !important;
}

/* ── Input / text area ─────────────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #0e1a0f !important;
    border: 1px solid #1a2e1c !important;
    color: #e6edf3 !important;
    border-radius: 12px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 2px rgba(34,197,94,.15) !important;
}

/* ── Expander ──────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #0e1a0f !important;
    border: 1px solid #1a2e1c !important;
    border-radius: 12px !important;
}

/* ── Progress ──────────────────────────────────────────────────────────── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg,#16a34a,#22c55e) !important;
}

/* ── Mobile safe area ──────────────────────────────────────────────────── */
@media (max-width: 480px) {
    .block-container { padding: 0 0 96px 0 !important; }
}
</style>
""", unsafe_allow_html=True)
