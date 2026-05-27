"""
AI Crop Doctor — Single-page mobile app with WhatsApp-style bottom navigation.
Five tabs: Home · Scan · History · Assistant · Profile
"""
import streamlit as st
import numpy as np
import json, os, sys, base64
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from utils.styles import inject_css
from utils.model_utils import predict, invert_labels, parse_label
from utils.history import load_history, save_prediction, clear_history
from utils.disease_db import DISEASE_DB, SEVERITY_COLOR_HEX, SEVERITY_BAR_PCT, get_bot_response

st.set_page_config(
    page_title="AI Crop Doctor",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_css()

# ─────────────────────────────────────────────────────────────────────────────
# Session defaults
# ─────────────────────────────────────────────────────────────────────────────
for k, v in {
    "tab":          "home",
    "splash_done":  False,
    "chat":         [],
    "model_bytes":  None,
    "model_name":   None,
    "labels_str":   None,
    "last_result":  None,
    "scan_mode":    "upload",  # "upload" | "camera"
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# Splash screen (once per session)
# ─────────────────────────────────────────────────────────────────────────────
_IMG = os.path.join(os.path.dirname(__file__), "..", "attached_assets", "image_1779873760068.png")
_b64 = ""
if os.path.exists(_IMG):
    with open(_IMG, "rb") as _f:
        _b64 = base64.b64encode(_f.read()).decode()
_img_src = f"data:image/png;base64,{_b64}" if _b64 else ""

if not st.session_state.splash_done:
    st.session_state.splash_done = True
    logo_html = (
        f'<img class="sp-logo" src="{_img_src}" alt="logo"/>'
        if _img_src else '<div class="sp-logo-ph">🌿</div>'
    )
    st.markdown(f"""
<div id="splash" class="sp-wrap">
  <canvas id="sp-canvas"></canvas>
  <div class="sp-grid"></div>
  <div class="sp-body">
    <div class="sp-rings">
      <div class="sp-ring sp-r3"></div>
      <div class="sp-ring sp-r2"></div>
      <div class="sp-ring sp-r1"></div>
    </div>
    <div class="sp-logo-wrap">
      {logo_html}
      <div class="sp-scan"></div>
    </div>
    <div class="sp-badge">● AI POWERED</div>
    <h1 class="sp-title">AI DOCTOR FOR CROPS</h1>
    <p class="sp-sub">Smart AI Disease Detection for Farmers</p>
    <div class="sp-prog-wrap">
      <div class="sp-prog-track"><div class="sp-prog-fill"></div></div>
      <div class="sp-prog-lbl" id="sp-status">Initializing AI model…</div>
    </div>
    <div class="sp-footer">Powered by TensorFlow · Computer Vision · Deep Learning</div>
  </div>
</div>
<style>
.sp-wrap{{position:fixed;inset:0;z-index:99999;
  background:radial-gradient(ellipse at 50% 35%,#031a08 0%,#010d04 60%,#000300 100%);
  display:flex;align-items:center;justify-content:center;overflow:hidden;
  animation:sp-exit .9s ease 4.2s forwards;}}
@keyframes sp-exit{{to{{opacity:0;pointer-events:none;visibility:hidden}}}}
#sp-canvas{{position:absolute;inset:0;pointer-events:none}}
.sp-grid{{position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(rgba(34,197,94,.04)1px,transparent 1px),
    linear-gradient(90deg,rgba(34,197,94,.04)1px,transparent 1px);
  background-size:40px 40px;}}
.sp-body{{position:relative;z-index:2;display:flex;flex-direction:column;
  align-items:center;gap:0;animation:sp-in .9s cubic-bezier(.16,1,.3,1) .2s both;}}
@keyframes sp-in{{from{{opacity:0;transform:translateY(28px) scale(.95)}}to{{opacity:1;transform:none}}}}
.sp-rings{{position:absolute;top:50%;left:50%;transform:translate(-50%,-72%);pointer-events:none}}
.sp-ring{{position:absolute;border-radius:50%;border:1px solid;top:50%;left:50%;
  transform:translate(-50%,-50%);animation:sp-ring 2.5s ease-in-out infinite;}}
.sp-r1{{width:195px;height:195px;border-color:rgba(34,197,94,.45);animation-delay:0s}}
.sp-r2{{width:285px;height:285px;border-color:rgba(34,197,94,.2);animation-delay:.5s}}
.sp-r3{{width:375px;height:375px;border-color:rgba(34,197,94,.08);animation-delay:1s}}
@keyframes sp-ring{{0%,100%{{transform:translate(-50%,-50%) scale(1);opacity:1}}
  50%{{transform:translate(-50%,-50%) scale(1.06);opacity:.55}}}}
.sp-logo-wrap{{position:relative;width:150px;height:150px;border-radius:20px;
  overflow:hidden;border:2px solid rgba(34,197,94,.5);margin-bottom:18px;
  box-shadow:0 0 0 4px rgba(34,197,94,.1),0 0 40px rgba(34,197,94,.4),0 0 80px rgba(34,197,94,.12);
  animation:sp-zoom .8s cubic-bezier(.34,1.56,.64,1) .3s both;}}
@keyframes sp-zoom{{from{{opacity:0;transform:scale(.45) rotate(-8deg)}}to{{opacity:1;transform:none}}}}
.sp-logo{{width:100%;height:100%;object-fit:cover;display:block;}}
.sp-logo-ph{{width:100%;height:100%;display:flex;align-items:center;justify-content:center;
  font-size:4.5rem;background:linear-gradient(135deg,#031a08,#052e10);}}
.sp-scan{{position:absolute;left:0;right:0;height:3px;
  background:linear-gradient(90deg,transparent,#22c55e,#4ade80,#22c55e,transparent);
  box-shadow:0 0 12px #22c55e,0 0 24px rgba(34,197,94,.5);
  animation:sp-scan-anim 2s ease-in-out 1s infinite;z-index:5;}}
@keyframes sp-scan-anim{{0%{{top:0;opacity:.9}}100%{{top:100%;opacity:.15}}}}
.sp-badge{{border:1px solid rgba(34,197,94,.4);color:#22c55e;border-radius:20px;
  padding:4px 14px;font-size:.65rem;font-weight:700;letter-spacing:3px;
  background:rgba(34,197,94,.07);margin-bottom:12px;
  animation:sp-txt .8s ease .7s both;}}
.sp-title{{font-size:clamp(1.7rem,5.5vw,3rem);font-weight:900;letter-spacing:-0.5px;
  margin:0 0 9px;background:linear-gradient(135deg,#fff 0%,#a3e635 40%,#22c55e 70%,#16a34a 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 18px rgba(34,197,94,.3));animation:sp-txt .8s ease .8s both;}}
.sp-sub{{font-size:clamp(.82rem,2.5vw,1rem);color:#6ee7b7;margin:0 0 22px;
  animation:sp-txt .8s ease .9s both;}}
@keyframes sp-txt{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
.sp-prog-wrap{{width:clamp(220px,58vw,360px);animation:sp-txt .8s ease 1s both;}}
.sp-prog-track{{background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);
  border-radius:20px;height:6px;overflow:hidden;}}
.sp-prog-fill{{height:100%;border-radius:20px;
  background:linear-gradient(90deg,#16a34a,#22c55e,#4ade80);
  box-shadow:0 0 12px rgba(34,197,94,.6);
  animation:sp-prog 3.8s cubic-bezier(.4,0,.2,1) .4s both;width:0;}}
@keyframes sp-prog{{0%{{width:0}}20%{{width:22%}}50%{{width:54%}}80%{{width:81%}}100%{{width:100%}}}}
.sp-prog-lbl{{text-align:center;color:#4ade80;font-size:.7rem;letter-spacing:1.5px;
  text-transform:uppercase;margin-top:9px;font-weight:600;}}
.sp-footer{{color:rgba(255,255,255,.18);font-size:.66rem;letter-spacing:1.5px;
  text-transform:uppercase;margin-top:18px;animation:sp-txt .8s ease 1.5s both;}}
</style>
<script>
(function(){{
  const c=document.getElementById('sp-canvas');
  if(!c)return;
  const x=c.getContext('2d');
  let W,H,dots=[];
  function resize(){{W=c.width=window.innerWidth;H=c.height=window.innerHeight;}}
  window.addEventListener('resize',resize);resize();
  for(let i=0;i<75;i++)dots.push({{x:Math.random()*W,y:Math.random()*H,
    r:Math.random()*2+.4,vx:(Math.random()-.5)*.38,vy:(Math.random()-.5)*.38,
    a:Math.random()*.55+.1}});
  function draw(){{
    x.clearRect(0,0,W,H);
    dots.forEach(d=>{{
      d.x+=d.vx;d.y+=d.vy;
      if(d.x<0)d.x=W;if(d.x>W)d.x=0;if(d.y<0)d.y=H;if(d.y>H)d.y=0;
      x.beginPath();x.arc(d.x,d.y,d.r,0,Math.PI*2);
      x.fillStyle=`rgba(34,197,94,${{d.a}})`;x.fill();
    }});
    for(let i=0;i<dots.length;i++)for(let j=i+1;j<dots.length;j++){{
      const dx=dots[i].x-dots[j].x,dy=dots[i].y-dots[j].y;
      const dist=Math.sqrt(dx*dx+dy*dy);
      if(dist<90){{x.beginPath();x.moveTo(dots[i].x,dots[i].y);
        x.lineTo(dots[j].x,dots[j].y);
        x.strokeStyle=`rgba(34,197,94,${{.1*(1-dist/90)}})`;
        x.lineWidth=.5;x.stroke();}}
    }}
    requestAnimationFrame(draw);
  }}
  draw();
  const msgs=['Initializing AI model…','Loading TensorFlow engine…',
    'Calibrating disease classifier…','Scanning crop database…','System ready ✓'];
  let si=0;const el=document.getElementById('sp-status');
  setInterval(()=>{{si=(si+1)%msgs.length;if(el)el.textContent=msgs[si];}},820);
}})();
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Model loader (cached)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading AI model…")
def _load_model(data: bytes, name: str):
    import tensorflow as tf, tempfile
    sfx = ".keras" if name.endswith(".keras") else ".h5"
    with tempfile.NamedTemporaryFile(delete=False, suffix=sfx) as f:
        f.write(data); p = f.name
    m = tf.keras.models.load_model(p)
    os.unlink(p)
    return m


# ─────────────────────────────────────────────────────────────────────────────
# Shared: run prediction
# ─────────────────────────────────────────────────────────────────────────────
def _run_prediction(img_pil):
    """Run AI prediction; returns result dict or error string."""
    if not st.session_state.model_bytes:
        return "no_model"
    if not st.session_state.labels_str:
        return "no_labels"
    try:
        from PIL import Image as PILImage
        model  = _load_model(st.session_state.model_bytes, st.session_state.model_name or "model.keras")
        labels = invert_labels(json.loads(st.session_state.labels_str))
        top_idx, conf, all_probs = predict(model, img_pil)
        raw = labels.get(str(top_idx), f"Class {top_idx}")
        crop, disease = parse_label(raw)
        is_healthy    = "healthy" in raw.lower()
        sev = "None" if is_healthy else (
            DISEASE_DB.get(crop,{}).get("diseases",{}).get(disease,{}).get("severity","Unknown"))
        dis_info = DISEASE_DB.get(crop,{}).get("diseases",{}).get(disease,{})
        save_prediction(crop, disease, conf, is_healthy)
        return dict(
            crop=crop, disease=disease, conf=conf,
            is_healthy=is_healthy, sev=sev, all_probs=all_probs,
            labels=labels, dis_info=dis_info,
            raw=raw, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
    except Exception as e:
        return f"error:{e}"


def _render_result(res: dict):
    """Render the prediction result card."""
    is_h = res["is_healthy"]
    sev  = res["sev"]
    conf = res["conf"]
    ring_col = "#22c55e" if is_h else SEVERITY_COLOR_HEX.get(sev, "#f97316")
    sev_pct  = SEVERITY_BAR_PCT.get(sev, 0)
    circ, dash = 213.63, 213.63 - (conf/100)*213.63
    card_cls  = "res-healthy" if is_h else "res-disease"
    badge_bg  = "rgba(34,197,94,.12)" if is_h else "rgba(249,115,22,.12)"
    badge_col = "#22c55e" if is_h else "#f97316"
    status_tx = "✅ HEALTHY PLANT" if is_h else "⚠️ DISEASE DETECTED"
    name_disp = "Healthy" if is_h else res["disease"]
    pathogen  = res["dis_info"].get("pathogen","—") if not is_h else "None — plant is healthy"
    recovery  = res["dis_info"].get("recovery","N/A")

    st.markdown(f"""
<div class="{card_cls}">
  <div class="res-badge" style="background:{badge_bg};color:{badge_col};border:1px solid {badge_col}44">
    {status_tx}
  </div>
  <div class="res-name">{name_disp}</div>
  <div class="res-crop">Crop: {res["crop"]} · {res["timestamp"]}</div>
  <div class="conf-wrap">
    <div class="conf-ring">
      <svg viewBox="0 0 72 72" width="72" height="72">
        <circle cx="36" cy="36" r="30" fill="none" stroke="#1a2e1c" stroke-width="6"/>
        <circle cx="36" cy="36" r="30" fill="none" stroke="{ring_col}"
          stroke-width="6" stroke-linecap="round"
          stroke-dasharray="{188.5:.1f}"
          stroke-dashoffset="{188.5-(conf/100)*188.5:.1f}"
          style="filter:drop-shadow(0 0 5px {ring_col})"/>
      </svg>
      <div style="position:absolute;inset:0;display:flex;flex-direction:column;
           align-items:center;justify-content:center">
        <span style="font-size:1rem;font-weight:800;color:#f0f6fc">{conf:.0f}%</span>
        <span style="font-size:.5rem;color:#4b6050;letter-spacing:1px;text-transform:uppercase">conf</span>
      </div>
    </div>
    <div class="conf-info">
      <div class="conf-lbl">AI Confidence</div>
      <div class="conf-bar-t">
        <div class="conf-bar-f" style="width:{conf:.1f}%;background:{ring_col}"></div>
      </div>
    </div>
  </div>
  <div class="info-grid2">
    <div class="info-cell2">
      <div class="lbl">🦠 Pathogen</div>
      <div class="val">{pathogen[:55]}{"…" if len(pathogen)>55 else ""}</div>
    </div>
    <div class="info-cell2">
      <div class="lbl">⚡ Severity</div>
      <div class="val" style="color:{ring_col};font-weight:700">{sev}</div>
      <div style="background:#0d1117;border-radius:4px;height:4px;margin-top:5px;overflow:hidden">
        <div style="height:100%;width:{sev_pct}%;background:{ring_col};border-radius:4px"></div>
      </div>
    </div>
    <div class="info-cell2">
      <div class="lbl">⏱ Recovery</div>
      <div class="val">{recovery}</div>
    </div>
    <div class="info-cell2">
      <div class="lbl">🌾 Crop</div>
      <div class="val">{res["crop"]}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    if not is_h and res["dis_info"]:
        for icon, lbl, key in [("🩺","Symptoms","symptoms"),
                                ("💊","Treatment","treatment"),
                                ("🛡️","Prevention","prevention")]:
            items = "".join(f"<li>{x}</li>" for x in res["dis_info"].get(key,[]))
            st.markdown(f"""
<div class="info-blk">
  <div class="blk-lbl">{icon} {lbl}</div>
  <ul>{items}</ul>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB: HOME
# ─────────────────────────────────────────────────────────────────────────────
def tab_home():
    from utils.disease_db import DISEASE_DB as DB

    # App bar
    st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;
     padding:14px 16px 4px;position:sticky;top:0;background:#080f09;z-index:100">
  <div>
    <div style="font-size:.72rem;color:#4b6050;letter-spacing:1px;text-transform:uppercase">
      Good day 🌱
    </div>
    <div style="font-size:1.3rem;font-weight:800;
         background:linear-gradient(90deg,#a3e635,#22c55e);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
         background-clip:text;line-height:1.1">
      AI Crop Doctor
    </div>
  </div>
  <div style="width:40px;height:40px;border-radius:50%;
       background:linear-gradient(135deg,#16a34a,#22c55e);
       display:flex;align-items:center;justify-content:center;font-size:1.2rem">
    🌿
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Hero CTA
    st.markdown("""
<div style="margin:0 12px;background:linear-gradient(135deg,#0b2e10,#0e3d15);
     border:1px solid rgba(34,197,94,.25);border-radius:20px;padding:1.4rem 1.5rem;
     box-shadow:0 8px 32px rgba(34,197,94,.1)">
  <div style="font-size:.72rem;color:#4ade80;letter-spacing:2px;
       text-transform:uppercase;font-weight:600;margin-bottom:6px">
    ● INSTANT DIAGNOSIS
  </div>
  <div style="font-size:1.3rem;font-weight:800;color:#f0f6fc;line-height:1.2;margin-bottom:6px">
    Detect crop diseases<br>with AI in seconds
  </div>
  <div style="font-size:.82rem;color:#6e8a72;margin-bottom:1rem">
    Upload a leaf photo or take one with your camera
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📷  Take Photo", use_container_width=True, type="primary"):
            st.session_state.tab = "scan"
            st.session_state.scan_mode = "camera"
            st.rerun()
    with col_b:
        if st.button("🖼️  Upload Image", use_container_width=True):
            st.session_state.tab = "scan"
            st.session_state.scan_mode = "upload"
            st.rerun()

    # Stats row
    history = load_history()
    total = len(history)
    healthy_ct = sum(1 for h in history if h.get("is_healthy"))
    disease_ct = total - healthy_ct

    st.markdown('<div class="sec-head">YOUR FARM STATS</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, val, lbl in [(c1,total,"Scans"),(c2,healthy_ct,"Healthy"),(c3,disease_ct,"Diseases")]:
        col.markdown(
            f'<div class="stat-chip"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>',
            unsafe_allow_html=True)

    # Recent scans
    if history:
        st.markdown('<div class="sec-head">RECENT SCANS</div>', unsafe_allow_html=True)
        for h in reversed(history[-3:]):
            is_h = h.get("is_healthy", True)
            dot  = "hist-dot-h" if is_h else "hist-dot-d"
            conf = h.get("confidence",0)
            conf_col = "#22c55e" if is_h else "#f97316"
            ts   = h.get("timestamp","")[:16].replace("T"," ")
            st.markdown(f"""
<div class="hist-item">
  <div class="{dot}"></div>
  <div class="hist-body">
    <div class="hist-name">{"✅ Healthy" if is_h else "🦠 " + h.get("disease","Unknown")}</div>
    <div class="hist-meta">{h.get("crop","?")} · {ts}</div>
  </div>
  <div class="hist-conf" style="color:{conf_col}">{conf:.0f}%</div>
</div>""", unsafe_allow_html=True)

    # Last scan result quick view
    if st.session_state.last_result and isinstance(st.session_state.last_result, dict):
        st.markdown('<div class="sec-head">LAST DIAGNOSIS</div>', unsafe_allow_html=True)
        with st.expander("View last result", expanded=False):
            _render_result(st.session_state.last_result)

    # Farming tips
    tips = [
        ("💧","Water Wisely","Morning irrigation reduces fungal risk. Use drip irrigation to save 30–50% water."),
        ("🌱","Fertilise Right","Apply basal NPK at planting, top-dress with CAN at 4–6 weeks."),
        ("🐛","Scout Weekly","Walk your field twice a week. Early detection saves 80% of treatment cost."),
        ("☀️","Prevent Disease","Rotate crops every 2–3 seasons and remove crop debris after harvest."),
    ]
    st.markdown('<div class="sec-head">FARMING TIPS</div>', unsafe_allow_html=True)
    for icon, title, body in tips:
        st.markdown(f"""
<div class="tip-card">
  <div class="tip-icon">{icon}</div>
  <div class="tip-title">{title}</div>
  <div class="tip-body">{body}</div>
</div>""", unsafe_allow_html=True)

    # Supported crops
    icons_row = "".join(
        f'<span title="{c}" style="font-size:1.3rem;margin:0 5px">{v["icon"]}</span>'
        for c, v in DB.items()
    )
    st.markdown(
        f'<div style="text-align:center;padding:.9rem 0;border-top:1px solid #1a2e1c;'
        f'margin:1rem 12px 0;color:#3a5244;font-size:.72rem;letter-spacing:.8px;'
        f'text-transform:uppercase">SUPPORTS {icons_row}</div>',
        unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB: SCAN
# ─────────────────────────────────────────────────────────────────────────────
def tab_scan():
    from PIL import Image

    # App bar
    st.markdown("""
<div style="display:flex;align-items:center;gap:10px;padding:14px 16px 8px;
     position:sticky;top:0;background:#080f09;z-index:100">
  <div style="font-size:1.3rem;font-weight:800;color:#f0f6fc">🔬 Scan Crop</div>
</div>""", unsafe_allow_html=True)

    # Model settings (collapsible)
    with st.expander("⚙️ AI Model Settings", expanded=not bool(st.session_state.model_bytes)):
        m_file = st.file_uploader("Upload Model (.keras / .h5)", type=["keras","h5"],
                                   key="model_upload")
        l_file = st.file_uploader("Upload Labels (class_indices.json)", type=["json"],
                                   key="labels_upload")
        if m_file:
            st.session_state.model_bytes = m_file.read()
            st.session_state.model_name  = m_file.name
            st.success("✅ Model saved")
        if l_file:
            st.session_state.labels_str = l_file.read().decode("utf-8")
            st.success("✅ Labels saved")

        # Status pills
        c1, c2 = st.columns(2)
        c1.markdown(
            f'<div style="background:{"rgba(34,197,94,.12)" if st.session_state.model_bytes else "rgba(255,100,100,.08)"};'
            f'border:1px solid {"#22c55e44" if st.session_state.model_bytes else "#f8514944"};'
            f'border-radius:8px;padding:6px 10px;text-align:center;font-size:.78rem;'
            f'color:{"#22c55e" if st.session_state.model_bytes else "#f85149"}'
            f'">{"✅ Model Ready" if st.session_state.model_bytes else "⚠️ No Model"}</div>',
            unsafe_allow_html=True)
        c2.markdown(
            f'<div style="background:{"rgba(34,197,94,.12)" if st.session_state.labels_str else "rgba(255,100,100,.08)"};'
            f'border:1px solid {"#22c55e44" if st.session_state.labels_str else "#f8514944"};'
            f'border-radius:8px;padding:6px 10px;text-align:center;font-size:.78rem;'
            f'color:{"#22c55e" if st.session_state.labels_str else "#f85149"}'
            f'">{"✅ Labels Ready" if st.session_state.labels_str else "⚠️ No Labels"}</div>',
            unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Input mode toggle
    col_cam, col_upl = st.columns(2)
    if col_cam.button("📷 Camera", use_container_width=True,
                       type="primary" if st.session_state.scan_mode == "camera" else "secondary"):
        st.session_state.scan_mode = "camera"; st.rerun()
    if col_upl.button("🖼️ Upload", use_container_width=True,
                       type="primary" if st.session_state.scan_mode == "upload" else "secondary"):
        st.session_state.scan_mode = "upload"; st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    img_pil = None

    if st.session_state.scan_mode == "camera":
        st.markdown("""
<div style="background:#0e1a0f;border:2px solid #1a2e1c;border-radius:14px;
     padding:.8rem;text-align:center;color:#4b6050;font-size:.8rem;margin-bottom:.6rem">
  📸 Your device camera will open below
</div>""", unsafe_allow_html=True)
        cam = st.camera_input("Take a photo of the leaf", label_visibility="collapsed")
        if cam:
            img_pil = Image.open(cam)
    else:
        upl = st.file_uploader("Choose a leaf image",
                                type=["jpg","jpeg","png","webp"],
                                label_visibility="collapsed")
        if upl:
            img_pil = Image.open(upl)

    if img_pil:
        # Preview with scan animation
        st.markdown('<div class="img-preview-wrap">', unsafe_allow_html=True)
        st.image(img_pil, use_container_width=True)
        st.markdown('<div class="img-scan-line"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("🔬  Analyse with AI", type="primary", use_container_width=True):
            with st.spinner("AI is analysing your crop…"):
                result = _run_prediction(img_pil)

            if result == "no_model":
                st.error("⚠️ Upload a model file in **AI Model Settings** above.", icon="⚠️")
            elif result == "no_labels":
                st.error("⚠️ Upload class_indices.json in **AI Model Settings** above.", icon="⚠️")
            elif isinstance(result, str) and result.startswith("error:"):
                st.error(f"Analysis failed: {result[6:]}", icon="❌")
            else:
                st.session_state.last_result = result
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                _render_result(result)

    else:
        st.markdown("""
<div style="border:2px dashed #1a2e1c;border-radius:16px;padding:2.5rem 1.5rem;
     text-align:center;background:#0a120b;margin-top:4px">
  <div style="font-size:2.5rem">🍃</div>
  <div style="color:#e6edf3;font-weight:600;margin-top:8px">No image yet</div>
  <div style="color:#4b6050;font-size:.82rem;margin-top:4px">
    Use camera or upload a leaf photo to begin analysis
  </div>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB: HISTORY
# ─────────────────────────────────────────────────────────────────────────────
def tab_history():
    history = load_history()

    st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;
     padding:14px 16px 8px;position:sticky;top:0;background:#080f09;z-index:100">
  <div style="font-size:1.3rem;font-weight:800;color:#f0f6fc">📋 History</div>
</div>""", unsafe_allow_html=True)

    if not history:
        st.markdown("""
<div style="text-align:center;padding:3rem 1rem">
  <div style="font-size:3rem">📋</div>
  <div style="color:#e6edf3;font-weight:600;margin-top:.8rem">No scans yet</div>
  <div style="color:#4b6050;font-size:.85rem;margin-top:.4rem">
    Run your first diagnosis on the Scan tab
  </div>
</div>""", unsafe_allow_html=True)
        return

    total = len(history)
    healthy_ct = sum(1 for h in history if h.get("is_healthy"))
    disease_ct = total - healthy_ct
    avg_conf   = sum(h.get("confidence",0) for h in history) / total if total else 0

    # Stats
    c1,c2,c3,c4 = st.columns(4)
    for col,val,lbl in [
        (c1,total,"Total"),(c2,healthy_ct,"Healthy"),
        (c3,disease_ct,"Disease"),(c4,f"{avg_conf:.0f}%","Avg Conf"),
    ]:
        col.markdown(
            f'<div class="stat-chip"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>',
            unsafe_allow_html=True)

    st.markdown('<div class="sec-head">ALL SCANS</div>', unsafe_allow_html=True)

    for h in reversed(history[-50:]):
        is_h = h.get("is_healthy", True)
        dot  = "hist-dot-h" if is_h else "hist-dot-d"
        conf = h.get("confidence",0)
        conf_col = "#22c55e" if is_h else "#f97316"
        name = "Healthy" if is_h else h.get("disease","Unknown")
        ts   = h.get("timestamp","")[:16].replace("T"," ")
        st.markdown(f"""
<div class="hist-item">
  <div class="{dot}"></div>
  <div class="hist-body">
    <div class="hist-name">{"✅ " if is_h else "🦠 "}{name}</div>
    <div class="hist-meta">{h.get("crop","?")} · {ts}</div>
  </div>
  <div class="hist-conf" style="color:{conf_col}">{conf:.0f}%</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Clear All History", use_container_width=True):
        clear_history()
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TAB: ASSISTANT
# ─────────────────────────────────────────────────────────────────────────────
def tab_assistant():
    st.markdown("""
<div style="display:flex;align-items:center;gap:10px;padding:14px 16px 8px;
     position:sticky;top:0;background:#080f09;z-index:100">
  <div style="width:36px;height:36px;border-radius:50%;
       background:linear-gradient(135deg,#16a34a,#22c55e);
       display:flex;align-items:center;justify-content:center;font-size:1rem">🤖</div>
  <div>
    <div style="font-size:1rem;font-weight:700;color:#f0f6fc">AI Farming Assistant</div>
    <div style="font-size:.72rem;color:#22c55e">● Online · Always ready</div>
  </div>
</div>""", unsafe_allow_html=True)

    # Init chat
    if not st.session_state.chat:
        st.session_state.chat = [{
            "role":"bot",
            "text": "**Habari! 👋 Welcome to AI Crop Doctor Assistant!**\n\n"
                    "Ask me anything about:\n\n"
                    "🌱 Fertiliser · 💧 Irrigation · 🐛 Pests · "
                    "🛡️ Disease prevention · 🌾 Harvest · 🏔️ Soil · 🌤️ Weather\n\n"
                    "Or name a crop for disease info!",
        }]

    # Quick questions
    quick = ["How to fertilise tomatoes?","Maize rust treatment",
             "Prevent late blight","Irrigation in dry season","Improve soil pH"]
    cols = st.columns(len(quick))
    for col, q in zip(cols, quick):
        if col.button(q[:12]+"…" if len(q)>12 else q, use_container_width=True, key=f"qq_{q}"):
            st.session_state.chat.append({"role":"user","text":q})
            st.session_state.chat.append({"role":"bot","text":get_bot_response(q)})
            st.rerun()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Chat messages
    for msg in st.session_state.chat:
        cls = "bubble-user" if msg["role"]=="user" else "bubble-bot"
        prefix = "" if msg["role"]=="user" else ""
        st.markdown(f'<div class="{cls}">{msg["text"]}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Input form
    with st.form("chat_input", clear_on_submit=True):
        ic, bc = st.columns([5,1])
        user_txt = ic.text_input("msg", placeholder="Ask your farming question…",
                                  label_visibility="collapsed")
        send = bc.form_submit_button("→", use_container_width=True)
    if send and user_txt.strip():
        st.session_state.chat.append({"role":"user","text":user_txt.strip()})
        st.session_state.chat.append({"role":"bot","text":get_bot_response(user_txt.strip())})
        st.rerun()

    if len(st.session_state.chat) > 2:
        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.chat = []
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TAB: PROFILE
# ─────────────────────────────────────────────────────────────────────────────
def tab_profile():
    st.markdown("""
<div style="padding:14px 16px 8px;position:sticky;top:0;background:#080f09;z-index:100">
  <div style="font-size:1.3rem;font-weight:800;color:#f0f6fc">👤 Profile & Settings</div>
</div>""", unsafe_allow_html=True)

    # Avatar
    st.markdown("""
<div style="text-align:center;padding:1.5rem 0 .5rem">
  <div style="width:72px;height:72px;border-radius:50%;margin:0 auto;
       background:linear-gradient(135deg,#16a34a,#22c55e);
       display:flex;align-items:center;justify-content:center;font-size:2rem;
       box-shadow:0 0 24px rgba(34,197,94,.3)">🧑‍🌾</div>
  <div style="color:#f0f6fc;font-weight:700;font-size:1rem;margin-top:.6rem">Farmer</div>
  <div style="color:#4b6050;font-size:.78rem">AI Crop Doctor User</div>
</div>""", unsafe_allow_html=True)

    # Model status
    st.markdown('<div class="sec-head">AI MODEL STATUS</div>', unsafe_allow_html=True)
    for label, val in [
        ("🤖 Model", "Loaded ✅" if st.session_state.model_bytes else "Not loaded ⚠️"),
        ("📋 Labels", "Loaded ✅" if st.session_state.labels_str else "Not loaded ⚠️"),
        ("📊 Total Scans", str(len(load_history()))),
    ]:
        col = "#22c55e" if "✅" in val else ("#f97316" if "⚠️" in val else "#c9d1d9")
        st.markdown(f"""
<div class="profile-item">
  <div class="profile-icon">📌</div>
  <div><div class="profile-label">{label}</div></div>
  <div style="color:{col};font-size:.85rem;font-weight:600">{val}</div>
</div>""", unsafe_allow_html=True)

    # Clear model
    if st.session_state.model_bytes:
        if st.button("🔄 Remove loaded model", use_container_width=True):
            st.session_state.model_bytes = None
            st.session_state.model_name  = None
            st.session_state.labels_str  = None
            st.success("Model removed.")
            st.rerun()

    st.markdown('<div class="sec-head">SUPPORTED CROPS</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (crop, info) in enumerate(DISEASE_DB.items()):
        cols[i % 4].markdown(
            f'<div style="text-align:center;padding:8px 4px;background:#0e1a0f;'
            f'border:1px solid #1a2e1c;border-radius:10px;margin:2px 0">'
            f'<div style="font-size:1.3rem">{info["icon"]}</div>'
            f'<div style="font-size:.65rem;color:#4b6050;margin-top:2px">{crop}</div></div>',
            unsafe_allow_html=True)

    st.markdown('<div class="sec-head">ABOUT</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="card">
  <div style="color:#a3e635;font-weight:700;font-size:.9rem">🌿 AI Crop Doctor</div>
  <div style="color:#6e8a72;font-size:.82rem;margin-top:.4rem;line-height:1.7">
    AI-powered plant disease detection for farmers across Africa and beyond.
    Powered by TensorFlow deep learning · Supports 13 crops · 30+ disease classes.<br><br>
    <strong style="color:#4b6050">Built for:</strong>
    <span style="color:#6e8a72"> Farmers · Agronomists · Agriculture officers · NGOs</span>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">DISEASE LIBRARY</div>', unsafe_allow_html=True)
    for crop, info in DISEASE_DB.items():
        diseases = [d for d in info["diseases"] if d != "Healthy"]
        with st.expander(f"{info['icon']} {crop} — {len(diseases)} diseases"):
            for d in diseases:
                sev = info["diseases"][d].get("severity","?")
                col = "#f85149" if "Very" in sev else "#f97316" if sev=="High" else "#fbbf24" if "Med" in sev else "#22c55e"
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;'
                    f'padding:5px 0;border-bottom:1px solid #1a2e1c">'
                    f'<span style="color:#c9d1d9;font-size:.84rem">{d}</span>'
                    f'<span style="color:{col};font-size:.76rem;font-weight:600">{sev}</span></div>',
                    unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Render active tab
# ─────────────────────────────────────────────────────────────────────────────
tab = st.session_state.tab

if   tab == "home":    tab_home()
elif tab == "scan":    tab_scan()
elif tab == "history": tab_history()
elif tab == "assist":  tab_assistant()
elif tab == "profile": tab_profile()

# ─────────────────────────────────────────────────────────────────────────────
# Bottom Navigation
# ─────────────────────────────────────────────────────────────────────────────
TAB_DEFS = [
    ("🏠", "Home",    "home"),
    ("🔬", "Scan",    "scan"),
    ("📋", "History", "history"),
    ("🤖", "Chat",    "assist"),
    ("👤", "Profile", "profile"),
]

# Hidden active-tab marker for JS
st.markdown(f'<input type="hidden" id="active-tab-val" value="{tab}">',
            unsafe_allow_html=True)

# Navigation buttons
nav_c = st.columns(5, gap="small")
for col, (icon, label, key) in zip(nav_c, TAB_DEFS):
    active = tab == key
    display = f"{icon}\n{'**'+label+'**' if active else label}"
    if col.button(display, key=f"nav_{key}", use_container_width=True):
        st.session_state.tab = key
        st.rerun()

# JS to add .nav-fixed class to the nav column container
st.markdown(f"""
<script>
(function fixBottomNav() {{
  function apply() {{
    const val = document.getElementById('active-tab-val');
    const activeKey = val ? val.value : 'home';
    const allBlocks = document.querySelectorAll('div[data-testid="stHorizontalBlock"]');
    if (!allBlocks.length) return;
    const lastBlock = allBlocks[allBlocks.length - 1];
    // Add fixed class
    allBlocks.forEach(b => b.classList.remove('nav-fixed'));
    lastBlock.classList.add('nav-fixed');
    // Highlight active button
    const tabs = ['home','scan','history','assist','profile'];
    const btns = lastBlock.querySelectorAll('button');
    btns.forEach((btn, i) => {{
      btn.classList.remove('nav-active');
      if (tabs[i] === activeKey) btn.classList.add('nav-active');
    }});
  }}
  // Run now and watch for DOM changes
  apply();
  const obs = new MutationObserver(apply);
  obs.observe(document.body, {{childList: true, subtree: true}});
  setTimeout(apply, 100);
  setTimeout(apply, 500);
  setTimeout(apply, 1200);
}})();
</script>
""", unsafe_allow_html=True)
