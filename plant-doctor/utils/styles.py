import streamlit as st


def inject_css():
    st.markdown("""
<style>
/* ── Reset & base ──────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* hide default Streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* ── Scrollbar ─────────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #22c55e44; border-radius: 3px; }

/* ── Sidebar ───────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #21262d;
}
section[data-testid="stSidebar"] * { color: #e6edf3 !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: #161b22 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 0.7rem !important;
    margin: 2px 0 !important;
    text-align: left !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #1f2937 !important;
    border-color: #22c55e !important;
    color: #22c55e !important;
}

/* ── Page wrapper ──────────────────────────────────────────────────────────── */
.main-container {
    max-width: 780px;
    margin: 0 auto;
}

/* ── App header ────────────────────────────────────────────────────────────── */
.app-header {
    text-align: center;
    margin-bottom: 2rem;
}
.app-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #22c55e 0%, #4ade80 50%, #86efac 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    line-height: 1.1;
    margin: 0;
}
.app-subtitle {
    color: #8b949e;
    font-size: 1rem;
    margin-top: 6px;
    font-weight: 400;
}

/* ── Upload zone ───────────────────────────────────────────────────────────── */
.upload-zone {
    border: 2px dashed #30363d;
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    background: #161b22;
    transition: all 0.3s;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.upload-zone:hover {
    border-color: #22c55e;
    background: #161b2299;
    box-shadow: 0 0 30px rgba(34,197,94,0.1);
}
.upload-zone::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center, rgba(34,197,94,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.upload-icon { font-size: 3rem; margin-bottom: 0.8rem; display: block; }
.upload-text { color: #e6edf3; font-size: 1.05rem; font-weight: 500; }
.upload-hint { color: #6e7681; font-size: 0.82rem; margin-top: 6px; }

/* ── Image preview with scan animation ────────────────────────────────────── */
@keyframes scan-line {
    0%   { top: 0; opacity: 1; }
    100% { top: 100%; opacity: 0.3; }
}
@keyframes pulse-ring {
    0%   { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34,197,94,0.4); }
    70%  { transform: scale(1);    box-shadow: 0 0 0 14px rgba(34,197,94,0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0  rgba(34,197,94,0); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
    0%   { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

.image-preview-wrapper {
    position: relative;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #30363d;
    background: #161b22;
}
.scan-overlay {
    position: absolute;
    left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent 0%, #22c55e 50%, transparent 100%);
    animation: scan-line 2s ease-in-out infinite;
    z-index: 10;
    box-shadow: 0 0 12px rgba(34,197,94,0.8);
}
.scanning-text {
    position: absolute;
    bottom: 12px; left: 0; right: 0;
    text-align: center;
    color: #22c55e;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    animation: fadeSlideUp 0.5s ease;
    z-index: 10;
}

/* ── Analyze button ────────────────────────────────────────────────────────── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 20px rgba(34,197,94,0.35) !important;
    animation: pulse-ring 2.5s infinite !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(34,197,94,0.5) !important;
}

/* ── Result cards ──────────────────────────────────────────────────────────── */
.result-wrapper { animation: fadeSlideUp 0.5s ease forwards; }

.result-card-healthy {
    background: linear-gradient(135deg, #052e16, #14532d);
    border: 1px solid #22c55e44;
    border-radius: 16px;
    padding: 1.8rem;
    box-shadow: 0 0 40px rgba(34,197,94,0.12), inset 0 1px 0 rgba(34,197,94,0.15);
}
.result-card-disease {
    background: linear-gradient(135deg, #1c1007, #2d1b06);
    border: 1px solid #f97316aa;
    border-radius: 16px;
    padding: 1.8rem;
    box-shadow: 0 0 40px rgba(249,115,22,0.12), inset 0 1px 0 rgba(249,115,22,0.15);
}
.result-status-badge-healthy {
    display: inline-block;
    background: #22c55e22;
    color: #22c55e;
    border: 1px solid #22c55e44;
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.result-status-badge-disease {
    display: inline-block;
    background: #f9731622;
    color: #f97316;
    border: 1px solid #f9731644;
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.result-disease-name {
    font-size: 1.7rem;
    font-weight: 700;
    color: #e6edf3;
    margin: 0 0 0.2rem;
    line-height: 1.2;
}
.result-crop-name {
    font-size: 0.9rem;
    color: #8b949e;
    margin-bottom: 1.2rem;
}

/* ── Confidence ring ───────────────────────────────────────────────────────── */
.conf-ring-wrapper {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    background: #0d111788;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
    border: 1px solid #21262d;
}
.conf-ring {
    position: relative;
    width: 80px; height: 80px;
    flex-shrink: 0;
}
.conf-ring svg { transform: rotate(-90deg); }
.conf-ring-bg  { fill: none; stroke: #21262d; stroke-width: 6; }
.conf-ring-fg  { fill: none; stroke-width: 6; stroke-linecap: round;
                 transition: stroke-dashoffset 1s ease; }
.conf-ring-text {
    position: absolute; inset: 0;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.conf-pct  { font-size: 1.1rem; font-weight: 700; color: #e6edf3; line-height: 1; }
.conf-label{ font-size: 0.55rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }
.conf-detail { flex: 1; }
.conf-detail-label { font-size: 0.78rem; color: #8b949e; margin-bottom: 6px; font-weight: 500; }
.conf-bar-track {
    background: #21262d;
    border-radius: 6px;
    height: 8px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 1s ease;
}

/* ── Info grid ─────────────────────────────────────────────────────────────── */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    margin-top: 1.2rem;
}
.info-cell {
    background: #0d111788;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 0.9rem 1rem;
}
.info-cell-label {
    font-size: 0.72rem;
    color: #6e7681;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 4px;
}
.info-cell-value {
    font-size: 0.88rem;
    color: #e6edf3;
    font-weight: 500;
    line-height: 1.4;
}
.severity-critical { color: #f85149 !important; }
.severity-high     { color: #f97316 !important; }
.severity-medium   { color: #fbbf24 !important; }
.severity-low      { color: #22c55e !important; }

/* ── Full-width info blocks ────────────────────────────────────────────────── */
.info-block {
    background: #0d111788;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
}
.info-block-label {
    font-size: 0.72rem;
    color: #6e7681;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 8px;
}
.info-block ul {
    margin: 0;
    padding-left: 1.2rem;
    color: #c9d1d9;
    font-size: 0.88rem;
    line-height: 1.8;
}

/* ── Top-5 breakdown ───────────────────────────────────────────────────────── */
.top5-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #21262d;
}
.top5-item:last-child { border-bottom: none; }
.top5-rank { color: #6e7681; font-size: 0.78rem; width: 20px; flex-shrink: 0; }
.top5-name { color: #c9d1d9; font-size: 0.85rem; flex: 1; min-width: 0;
             white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.top5-bar-wrap { width: 120px; flex-shrink: 0; }
.top5-bar-track { background: #21262d; border-radius: 4px; height: 5px; overflow: hidden; }
.top5-bar-fill  { height: 100%; border-radius: 4px; background: #22c55e; }
.top5-pct { color: #8b949e; font-size: 0.78rem; width: 42px; text-align: right; flex-shrink: 0; }

/* ── Stat cards (dashboard) ────────────────────────────────────────────────── */
.stat-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.stat-value { font-size: 2rem; font-weight: 700; color: #22c55e; line-height: 1.1; }
.stat-label { font-size: 0.8rem; color: #6e7681; margin-top: 4px; }

/* ── Chat bubbles ──────────────────────────────────────────────────────────── */
.chat-msg-user {
    background: #1f2937;
    border-radius: 18px 18px 4px 18px;
    padding: 0.85rem 1.1rem;
    margin: 0.6rem 0 0.6rem 20%;
    font-size: 0.9rem;
    color: #e6edf3;
    border: 1px solid #30363d;
}
.chat-msg-bot {
    background: #161b22;
    border-radius: 18px 18px 18px 4px;
    padding: 0.85rem 1.1rem;
    margin: 0.6rem 20% 0.6rem 0;
    font-size: 0.9rem;
    color: #c9d1d9;
    border: 1px solid #22c55e22;
    border-left: 3px solid #22c55e;
}

/* ── Glass card ────────────────────────────────────────────────────────────── */
.glass-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.6rem;
}

/* ── Section title ─────────────────────────────────────────────────────────── */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e6edf3;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #22c55e33, transparent);
    margin-left: 8px;
}

/* ── Disease library cards ─────────────────────────────────────────────────── */
.disease-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: #e6edf3;
}
.sev-pill {
    display: inline-block;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.sev-vhigh  { background: #2d0a0a; color: #f85149; border: 1px solid #f8514944; }
.sev-high   { background: #2d1200; color: #f97316; border: 1px solid #f9731644; }
.sev-medium { background: #2d2000; color: #fbbf24; border: 1px solid #fbbf2444; }
.sev-low    { background: #0a2d0a; color: #22c55e; border: 1px solid #22c55e44; }
.sev-none   { background: #0a1a0a; color: #4ade80; border: 1px solid #4ade8044; }

/* ── File uploader overrides ────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #161b22 !important;
    border: 2px dashed #30363d !important;
    border-radius: 14px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #22c55e !important;
}

/* ── Mobile ────────────────────────────────────────────────────────────────── */
@media (max-width: 640px) {
    .app-title { font-size: 1.8rem; }
    .info-grid { grid-template-columns: 1fr; }
    .conf-ring-wrapper { flex-direction: column; text-align: center; }
    .top5-bar-wrap { width: 80px; }
}
</style>
""", unsafe_allow_html=True)
