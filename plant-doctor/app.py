"""
AI Crop Doctor — Main app with animated splash screen.
Splash shows once on first visit, then auto-transitions to detection UI.
"""
import streamlit as st
import numpy as np
import json, os, sys, base64

sys.path.insert(0, os.path.dirname(__file__))
from utils.styles import inject_css
from utils.model_utils import predict, invert_labels, parse_label
from utils.history import save_prediction
from utils.disease_db import DISEASE_DB, SEVERITY_COLOR_HEX, SEVERITY_BAR_PCT

st.set_page_config(
    page_title="AI Crop Doctor",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_css()

# ── Encode school image to base64 ─────────────────────────────────────────────
_IMG_PATH = os.path.join(os.path.dirname(__file__), "..", "attached_assets", "image_1779873760068.png")
_img_b64 = ""
if os.path.exists(_IMG_PATH):
    with open(_IMG_PATH, "rb") as _f:
        _img_b64 = base64.b64encode(_f.read()).decode()
_img_src = f"data:image/png;base64,{_img_b64}" if _img_b64 else ""

# ── Splash screen (shown once per session) ────────────────────────────────────
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if not st.session_state.splash_done:
    st.session_state.splash_done = True   # mark done before render so rerenders skip it

    logo_html = (
        f'<img class="splash-logo" src="{_img_src}" alt="AI Crop Doctor"/>'
        if _img_src else
        '<div class="splash-logo-placeholder">🌿</div>'
    )

    st.markdown(f"""
<div class="splash-overlay" id="splash">
  <!-- ── Particle canvas ── -->
  <canvas id="splash-canvas"></canvas>

  <!-- ── Grid overlay ── -->
  <div class="splash-grid"></div>

  <!-- ── Center content ── -->
  <div class="splash-center">

    <!-- Scan rings -->
    <div class="splash-rings">
      <div class="splash-ring splash-ring-3"></div>
      <div class="splash-ring splash-ring-2"></div>
      <div class="splash-ring splash-ring-1"></div>
    </div>

    <!-- Logo -->
    <div class="splash-logo-wrap">
      {logo_html}
      <div class="splash-scan-line"></div>
      <div class="splash-logo-glow"></div>
    </div>

    <!-- Brand text -->
    <div class="splash-title-wrap">
      <div class="splash-badge">● AI POWERED</div>
      <h1 class="splash-title">AI DOCTOR FOR CROPS</h1>
      <p class="splash-subtitle">Smart AI Disease Detection for Farmers</p>
    </div>

    <!-- Progress bar -->
    <div class="splash-progress-wrap">
      <div class="splash-progress-track">
        <div class="splash-progress-fill"></div>
      </div>
      <div class="splash-progress-label" id="splash-status">Initializing AI model…</div>
    </div>

    <!-- Bottom tagline -->
    <div class="splash-footer">
      Powered by TensorFlow · Computer Vision · Deep Learning
    </div>
  </div>
</div>

<style>
/* ═══════════════════════════════════════════════════════════════════
   SPLASH SCREEN
═══════════════════════════════════════════════════════════════════ */

/* Full-screen overlay */
.splash-overlay {{
  position: fixed;
  inset: 0;
  z-index: 99999;
  background: radial-gradient(ellipse at 50% 40%, #031a08 0%, #010d04 60%, #000300 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  animation: splash-exit 0.8s ease 4.2s forwards;
}}

@keyframes splash-exit {{
  0%   {{ opacity: 1; pointer-events: all; }}
  100% {{ opacity: 0; pointer-events: none; visibility: hidden; }}
}}

/* Canvas particles */
#splash-canvas {{
  position: absolute;
  inset: 0;
  pointer-events: none;
}}

/* Subtle grid */
.splash-grid {{
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(34,197,94,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(34,197,94,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}}

/* Center layout */
.splash-center {{
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
  animation: splash-content-in 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
}}

@keyframes splash-content-in {{
  from {{ opacity: 0; transform: translateY(30px) scale(0.95); }}
  to   {{ opacity: 1; transform: translateY(0) scale(1); }}
}}

/* ── Pulsing rings ─────────────────────────────────────────────── */
.splash-rings {{
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -72%);
  pointer-events: none;
}}
.splash-ring {{
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(34,197,94,0.3);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  animation: ring-pulse 2.5s ease-in-out infinite;
}}
.splash-ring-1 {{ width: 200px; height: 200px; animation-delay: 0s; border-color: rgba(34,197,94,0.4); }}
.splash-ring-2 {{ width: 290px; height: 290px; animation-delay: 0.5s; border-color: rgba(34,197,94,0.2); }}
.splash-ring-3 {{ width: 390px; height: 390px; animation-delay: 1s; border-color: rgba(34,197,94,0.08); }}

@keyframes ring-pulse {{
  0%, 100% {{ transform: translate(-50%,-50%) scale(1);   opacity: 1; }}
  50%       {{ transform: translate(-50%,-50%) scale(1.06); opacity: 0.6; }}
}}

/* ── Logo wrapper ─────────────────────────────────────────────── */
.splash-logo-wrap {{
  position: relative;
  width: 160px; height: 160px;
  border-radius: 20px;
  overflow: hidden;
  border: 2px solid rgba(34,197,94,0.5);
  box-shadow:
    0 0 0 4px rgba(34,197,94,0.1),
    0 0 40px rgba(34,197,94,0.4),
    0 0 80px rgba(34,197,94,0.15);
  animation: logo-zoom-in 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s both;
  margin-bottom: 20px;
}}
.splash-logo {{
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
}}
.splash-logo-placeholder {{
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  font-size: 5rem;
  background: linear-gradient(135deg, #031a08, #052e10);
}}
.splash-logo-glow {{
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at center, transparent 50%, rgba(34,197,94,0.15) 100%);
  pointer-events: none;
}}

@keyframes logo-zoom-in {{
  from {{ opacity: 0; transform: scale(0.5) rotate(-8deg); }}
  to   {{ opacity: 1; transform: scale(1)   rotate(0deg); }}
}}

/* Scan line sweeping over logo */
.splash-scan-line {{
  position: absolute;
  left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, #22c55e, #4ade80, #22c55e, transparent);
  box-shadow: 0 0 12px #22c55e, 0 0 24px rgba(34,197,94,0.5);
  animation: logo-scan 2s ease-in-out 1s infinite;
  z-index: 5;
}}
@keyframes logo-scan {{
  0%   {{ top: 0%; opacity: 0.9; }}
  100% {{ top: 100%; opacity: 0.2; }}
}}

/* ── Brand text ─────────────────────────────────────────────────── */
.splash-title-wrap {{
  text-align: center;
  margin-bottom: 28px;
  animation: text-fade-in 0.8s ease 0.7s both;
}}
@keyframes text-fade-in {{
  from {{ opacity: 0; transform: translateY(16px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}

.splash-badge {{
  display: inline-block;
  border: 1px solid rgba(34,197,94,0.4);
  color: #22c55e;
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 3px;
  margin-bottom: 14px;
  background: rgba(34,197,94,0.07);
}}

.splash-title {{
  font-size: clamp(1.8rem, 5vw, 3.2rem);
  font-weight: 900;
  letter-spacing: -1px;
  line-height: 1.05;
  margin: 0 0 10px;
  background: linear-gradient(135deg, #ffffff 0%, #a3e635 40%, #22c55e 70%, #16a34a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: none;
  filter: drop-shadow(0 0 20px rgba(34,197,94,0.3));
}}

.splash-subtitle {{
  font-size: clamp(0.85rem, 2.5vw, 1.05rem);
  color: #6ee7b7;
  font-weight: 400;
  letter-spacing: 0.3px;
  margin: 0;
  opacity: 0.85;
}}

/* ── Progress bar ─────────────────────────────────────────────── */
.splash-progress-wrap {{
  width: clamp(240px, 60vw, 380px);
  animation: text-fade-in 0.8s ease 1s both;
}}
.splash-progress-track {{
  background: rgba(34,197,94,0.1);
  border: 1px solid rgba(34,197,94,0.2);
  border-radius: 20px;
  height: 6px;
  overflow: hidden;
}}
.splash-progress-fill {{
  height: 100%;
  border-radius: 20px;
  background: linear-gradient(90deg, #16a34a, #22c55e, #4ade80);
  box-shadow: 0 0 12px rgba(34,197,94,0.6);
  animation: progress-fill 3.8s cubic-bezier(0.4, 0, 0.2, 1) 0.4s both;
  width: 0%;
}}
@keyframes progress-fill {{
  0%   {{ width: 0%; }}
  20%  {{ width: 25%; }}
  50%  {{ width: 55%; }}
  80%  {{ width: 80%; }}
  100% {{ width: 100%; }}
}}

.splash-progress-label {{
  text-align: center;
  color: #4ade80;
  font-size: 0.72rem;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-top: 10px;
  font-weight: 600;
}}

/* ── Footer ─────────────────────────────────────────────────────── */
.splash-footer {{
  color: rgba(255,255,255,0.2);
  font-size: 0.7rem;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-top: 20px;
  animation: text-fade-in 0.8s ease 1.5s both;
}}

/* Mobile */
@media (max-width: 480px) {{
  .splash-logo-wrap {{ width: 130px; height: 130px; }}
  .splash-ring-1 {{ width: 160px; height: 160px; }}
  .splash-ring-2 {{ width: 240px; height: 240px; }}
  .splash-ring-3 {{ width: 320px; height: 320px; }}
}}
</style>

<script>
/* ── Floating particles ───────────────────────────────────────── */
(function() {{
  const canvas = document.getElementById('splash-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, dots = [];

  function resize() {{
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }}
  window.addEventListener('resize', resize);
  resize();

  for (let i = 0; i < 80; i++) {{
    dots.push({{
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 2 + 0.5,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      a: Math.random() * 0.6 + 0.1,
    }});
  }}

  function draw() {{
    ctx.clearRect(0, 0, W, H);
    dots.forEach(d => {{
      d.x += d.vx; d.y += d.vy;
      if (d.x < 0) d.x = W; if (d.x > W) d.x = 0;
      if (d.y < 0) d.y = H; if (d.y > H) d.y = 0;
      ctx.beginPath();
      ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(34, 197, 94, ${{d.a}})`;
      ctx.fill();
    }});
    // Connection lines
    for (let i = 0; i < dots.length; i++) {{
      for (let j = i + 1; j < dots.length; j++) {{
        const dx = dots[i].x - dots[j].x;
        const dy = dots[i].y - dots[j].y;
        const dist = Math.sqrt(dx*dx + dy*dy);
        if (dist < 100) {{
          ctx.beginPath();
          ctx.moveTo(dots[i].x, dots[i].y);
          ctx.lineTo(dots[j].x, dots[j].y);
          ctx.strokeStyle = `rgba(34, 197, 94, ${{0.12 * (1 - dist/100)}})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }}
      }}
    }}
    requestAnimationFrame(draw);
  }}
  draw();

  /* Status text cycling */
  const statuses = [
    'Initializing AI model…',
    'Loading TensorFlow engine…',
    'Calibrating disease classifier…',
    'Scanning crop database…',
    'System ready ✓',
  ];
  let si = 0;
  const el = document.getElementById('splash-status');
  setInterval(() => {{
    si = (si + 1) % statuses.length;
    if (el) el.textContent = statuses[si];
  }}, 800);
}})();
</script>
""", unsafe_allow_html=True)

# ── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌿 AI Crop Doctor")
    st.divider()
    st.page_link("app.py",                       label="🔬 Detect Disease")
    st.page_link("pages/1_📊_Dashboard.py",       label="📊 Analytics")
    st.page_link("pages/2_🤖_AI_Assistant.py",    label="🤖 AI Assistant")
    st.page_link("pages/3_📚_Disease_Library.py", label="📚 Disease Library")
    st.divider()
    st.markdown("**⚙️ Load AI Model**")
    model_file  = st.file_uploader("Model (.keras / .h5)",         type=["keras","h5"])
    labels_file = st.file_uploader("Labels (class_indices.json)",  type=["json"])
    if model_file:
        st.success("✅ Model loaded")
    if labels_file:
        st.success("✅ Labels loaded")

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:1.5rem 0 1rem">
  <div style="
    font-size:clamp(1.6rem,4vw,2.4rem);
    font-weight:900;
    letter-spacing:-0.5px;
    background:linear-gradient(135deg,#ffffff 0%,#a3e635 40%,#22c55e 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;
    line-height:1.1;margin-bottom:6px">
    AI Crop Doctor
  </div>
  <div style="color:#6e7681;font-size:0.92rem">
    AI-powered plant disease detection system
  </div>
</div>
""", unsafe_allow_html=True)


# ── Model loader (cached) ─────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading AI model…")
def _load_model(data: bytes, name: str):
    import tensorflow as tf, tempfile
    sfx = ".keras" if name.endswith(".keras") else ".h5"
    with tempfile.NamedTemporaryFile(delete=False, suffix=sfx) as f:
        f.write(data); p = f.name
    m = tf.keras.models.load_model(p)
    os.unlink(p)
    return m


# ── Upload section ────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Upload plant leaf image",
    type=["jpg","jpeg","png","webp"],
    label_visibility="collapsed",
)

if not uploaded:
    st.markdown("""
    <div style="
      border:2px dashed #1e3a2a;
      border-radius:16px;padding:3.5rem 2rem;
      text-align:center;
      background:linear-gradient(135deg,#0a1a0e,#0d1f10);
      cursor:pointer;transition:all .3s;
      box-shadow:inset 0 0 60px rgba(34,197,94,0.03)">
      <div style="font-size:3rem;margin-bottom:0.8rem">🍃</div>
      <div style="color:#e6edf3;font-size:1rem;font-weight:500">
        Drop your crop leaf image here
      </div>
      <div style="color:#4b6458;font-size:0.82rem;margin-top:6px">
        JPG · PNG · WEBP · Drag & drop or click to browse
      </div>
    </div>
    <div style="text-align:center;margin-top:1.5rem;color:#3a5244;font-size:0.78rem;letter-spacing:1px">
      SUPPORTS 13 CROPS · 30+ DISEASE CLASSES · TENSORFLOW AI
    </div>
    """, unsafe_allow_html=True)

else:
    from PIL import Image
    img = Image.open(uploaded)

    col_img, col_act = st.columns([3, 2], gap="large")

    with col_img:
        st.markdown('<div class="image-preview-wrapper">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown("""
        <div class="scan-overlay"></div>
        <div class="scanning-text">● READY TO ANALYSE</div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_act:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-card">
          <div style="color:#4b6458;font-size:.72rem;letter-spacing:1px;text-transform:uppercase">
            Image loaded
          </div>
          <div style="color:#e6edf3;font-weight:600;margin-top:4px;
               white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
            {uploaded.name}
          </div>
          <div style="color:#4b6458;font-size:.82rem;margin-top:2px">
            {img.size[0]}×{img.size[1]} px · {img.mode}
          </div>
        </div>
        """, unsafe_allow_html=True)

        analyse = st.button("🔬  Analyse Crop", type="primary", use_container_width=True)
        st.markdown("""
        <div style="color:#4b6458;font-size:.75rem;text-align:center;margin-top:.6rem">
          Upload model &amp; labels via sidebar
        </div>""", unsafe_allow_html=True)

    # ── Run prediction ────────────────────────────────────────────────────────
    if analyse:
        if not model_file:
            st.error("No model loaded — upload a `.keras` or `.h5` file in the sidebar.", icon="⚠️")
        elif not labels_file:
            st.error("No class labels — upload `class_indices.json` in the sidebar.", icon="⚠️")
        else:
            status_box = st.empty()
            status_box.markdown("""
            <div style="text-align:center;padding:2.5rem 1rem">
              <div style="font-size:2.5rem;animation:pulse-ring 1.5s infinite">🧬</div>
              <div style="color:#22c55e;font-weight:700;letter-spacing:3px;
                   font-size:.9rem;text-transform:uppercase;margin-top:.7rem">
                Analysing crop image…
              </div>
              <div style="color:#4b6458;font-size:.78rem;margin-top:5px">
                AI model processing · please wait
              </div>
            </div>""", unsafe_allow_html=True)

            try:
                model  = _load_model(model_file.read(), model_file.name)
                labels = invert_labels(json.loads(labels_file.read()))
                img_f  = Image.open(uploaded)
                top_idx, conf, all_probs = predict(model, img_f)

                raw = labels.get(str(top_idx), f"Class {top_idx}")
                crop, disease = parse_label(raw)
                is_healthy    = "healthy" in raw.lower()
                save_prediction(crop, disease, conf, is_healthy)
                status_box.empty()

                # Colours
                sev = "None" if is_healthy else (
                    DISEASE_DB.get(crop,{}).get("diseases",{}).get(disease,{}).get("severity","Unknown"))
                ring_col  = "#22c55e" if is_healthy else SEVERITY_COLOR_HEX.get(sev,"#f97316")
                card_grad = (
                    "linear-gradient(135deg,#031a0a,#052e12)" if is_healthy
                    else "linear-gradient(135deg,#1c0a03,#2d1500)"
                )
                card_border = "#22c55e44" if is_healthy else "#f9731666"

                # SVG ring maths
                circ  = 213.63
                dash  = circ - (conf/100)*circ
                status_txt = "✅ HEALTHY PLANT" if is_healthy else "⚠️  DISEASE DETECTED"
                badge_bg  = "rgba(34,197,94,.12)"  if is_healthy else "rgba(249,115,22,.12)"
                badge_col = "#22c55e"              if is_healthy else "#f97316"
                name_disp = "Healthy"              if is_healthy else disease

                # Treatment data
                dis_info  = DISEASE_DB.get(crop,{}).get("diseases",{}).get(disease,{})
                pathogen  = dis_info.get("pathogen","—") if not is_healthy else "None — plant is healthy"
                recovery  = dis_info.get("recovery","N/A")
                sev_pct   = SEVERITY_BAR_PCT.get(sev,0)

                st.markdown(f"""
<div style="animation:fadeSlideUp .5s ease both">
<div style="background:{card_grad};border:1px solid {card_border};
     border-radius:18px;padding:1.8rem;
     box-shadow:0 0 50px rgba(34,197,94,.07)">

  <!-- Status badge + title -->
  <div style="display:inline-block;background:{badge_bg};color:{badge_col};
       border:1px solid {badge_col}44;border-radius:20px;padding:4px 16px;
       font-size:.72rem;font-weight:700;letter-spacing:1.5px;margin-bottom:.8rem">
    {status_txt}
  </div>
  <div style="font-size:1.7rem;font-weight:800;color:#f0f6fc;
       margin-bottom:2px;line-height:1.1">{name_disp}</div>
  <div style="color:#6e7681;font-size:.88rem;margin-bottom:1.2rem">Crop: {crop}</div>

  <!-- Confidence ring + bar -->
  <div style="display:flex;align-items:center;gap:1.2rem;
       background:rgba(0,0,0,.3);border:1px solid #21262d;
       border-radius:12px;padding:1rem 1.2rem">
    <div style="position:relative;width:80px;height:80px;flex-shrink:0">
      <svg viewBox="0 0 80 80" width="80" height="80"
           style="transform:rotate(-90deg)">
        <circle cx="40" cy="40" r="34" fill="none"
                stroke="#1a2a1a" stroke-width="7"/>
        <circle cx="40" cy="40" r="34" fill="none"
                stroke="{ring_col}" stroke-width="7"
                stroke-linecap="round"
                stroke-dasharray="{circ:.2f}"
                stroke-dashoffset="{dash:.2f}"
                style="filter:drop-shadow(0 0 6px {ring_col})"/>
      </svg>
      <div style="position:absolute;inset:0;display:flex;flex-direction:column;
           align-items:center;justify-content:center">
        <span style="font-size:1.05rem;font-weight:800;color:#f0f6fc">{conf:.0f}%</span>
        <span style="font-size:.52rem;color:#6e7681;letter-spacing:1px;text-transform:uppercase">AI conf</span>
      </div>
    </div>
    <div style="flex:1">
      <div style="font-size:.72rem;color:#6e7681;margin-bottom:6px;font-weight:600;
           text-transform:uppercase;letter-spacing:1px">AI Confidence Score</div>
      <div style="background:#0d1117;border-radius:6px;height:8px;overflow:hidden">
        <div style="height:100%;border-radius:6px;width:{conf:.1f}%;
             background:linear-gradient(90deg,{ring_col}99,{ring_col});
             box-shadow:0 0 8px {ring_col}88;transition:width 1s ease"></div>
      </div>
      <div style="display:flex;justify-content:space-between;
           margin-top:4px;font-size:.72rem;color:#4b6458">
        <span>0%</span><span>50%</span><span>100%</span>
      </div>
    </div>
  </div>

  <!-- Info grid -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin-top:1rem">
    <div style="background:rgba(0,0,0,.3);border:1px solid #21262d;
         border-radius:10px;padding:.9rem 1rem">
      <div style="font-size:.7rem;color:#4b6458;letter-spacing:1px;
           text-transform:uppercase;font-weight:600;margin-bottom:4px">🦠 Pathogen</div>
      <div style="font-size:.85rem;color:#c9d1d9;line-height:1.4">{pathogen}</div>
    </div>
    <div style="background:rgba(0,0,0,.3);border:1px solid #21262d;
         border-radius:10px;padding:.9rem 1rem">
      <div style="font-size:.7rem;color:#4b6458;letter-spacing:1px;
           text-transform:uppercase;font-weight:600;margin-bottom:4px">⚡ Severity</div>
      <div style="font-size:.85rem;font-weight:700;color:{ring_col}">{sev}</div>
      <div style="background:#1a1a1a;border-radius:4px;height:5px;margin-top:6px;overflow:hidden">
        <div style="height:100%;width:{sev_pct}%;background:{ring_col};border-radius:4px"></div>
      </div>
    </div>
    <div style="background:rgba(0,0,0,.3);border:1px solid #21262d;
         border-radius:10px;padding:.9rem 1rem">
      <div style="font-size:.7rem;color:#4b6458;letter-spacing:1px;
           text-transform:uppercase;font-weight:600;margin-bottom:4px">⏱ Recovery</div>
      <div style="font-size:.85rem;color:#c9d1d9">{recovery}</div>
    </div>
    <div style="background:rgba(0,0,0,.3);border:1px solid #21262d;
         border-radius:10px;padding:.9rem 1rem">
      <div style="font-size:.7rem;color:#4b6458;letter-spacing:1px;
           text-transform:uppercase;font-weight:600;margin-bottom:4px">🌾 Crop</div>
      <div style="font-size:.85rem;color:#c9d1d9">{crop}</div>
    </div>
  </div>
</div>
</div>
""", unsafe_allow_html=True)

                # Symptoms / Treatment / Prevention
                if not is_healthy and dis_info:
                    sym_items = "".join(f"<li>{s}</li>" for s in dis_info.get("symptoms",[]))
                    trt_items = "".join(f"<li>{t}</li>" for t in dis_info.get("treatment",[]))
                    prv_items = "".join(f"<li>{p}</li>" for p in dis_info.get("prevention",[]))

                    for icon, label, items in [
                        ("🩺","Symptoms",sym_items),
                        ("💊","Treatment Protocol",trt_items),
                        ("🛡️","Prevention Measures",prv_items),
                    ]:
                        st.markdown(f"""
<div class="info-block" style="margin-top:.7rem">
  <div class="info-block-label">{icon} {label}</div>
  <ul style="margin:0;padding-left:1.3rem;color:#9ca3af;font-size:.87rem;line-height:1.8">
    {items}
  </ul>
</div>""", unsafe_allow_html=True)

                elif is_healthy:
                    st.markdown("""
<div class="info-block" style="margin-top:.7rem;border-color:#22c55e22">
  <div class="info-block-label">✅ Recommendations</div>
  <ul style="margin:0;padding-left:1.3rem;color:#9ca3af;font-size:.87rem;line-height:1.8">
    <li>No disease detected — plant appears healthy</li>
    <li>Continue regular crop monitoring and scouting</li>
    <li>Apply preventive fungicide at start of rainy season</li>
    <li>Maintain proper plant spacing and irrigation</li>
  </ul>
</div>""", unsafe_allow_html=True)

                # Top-5
                with st.expander("📈 Full probability breakdown", expanded=False):
                    top5 = sorted(enumerate(all_probs), key=lambda x:x[1], reverse=True)[:5]
                    rows = ""
                    for rank, (idx, prob) in enumerate(top5, 1):
                        lbl = labels.get(str(idx), f"Class {idx}")
                        _, d = parse_label(lbl)
                        pct = prob*100
                        rows += f"""
<div class="top5-item">
  <span class="top5-rank">{rank}</span>
  <span class="top5-name">{d}</span>
  <div class="top5-bar-wrap">
    <div class="top5-bar-track">
      <div class="top5-bar-fill" style="width:{min(100,pct):.1f}%"></div>
    </div>
  </div>
  <span class="top5-pct">{pct:.1f}%</span>
</div>"""
                    st.markdown(f'<div style="padding:.3rem 0">{rows}</div>',
                                unsafe_allow_html=True)

            except Exception as e:
                status_box.empty()
                st.error(f"**Analysis failed:** {e}", icon="❌")
                st.caption("Ensure the model and class_indices.json are compatible, and the model accepts RGB image input.")

# ── Supported crops strip ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
from utils.disease_db import DISEASE_DB as _DB
icons = "".join(
    f'<span title="{c}" style="margin:0 5px;font-size:1.3rem">{v["icon"]}</span>'
    for c, v in _DB.items()
)
st.markdown(
    f'<div style="text-align:center;padding:.8rem 0;'
    f'border-top:1px solid #21262d;color:#3a5244;font-size:.76rem;'
    f'letter-spacing:.8px;text-transform:uppercase">'
    f'Supported crops &nbsp;{icons}</div>',
    unsafe_allow_html=True,
)
