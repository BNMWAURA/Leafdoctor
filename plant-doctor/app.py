"""
AI Crop Doctor — Production-grade mobile app.
Single-file, all five tabs, WhatsApp-style bottom navigation.
"""
import streamlit as st
import numpy as np
import json, os, sys, base64, time
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from utils.styles       import inject_css
from utils.model_utils  import predict, invert_labels, parse_label
from utils.history      import load_history, save_prediction, clear_history
from utils.disease_db   import DISEASE_DB, SEVERITY_COLOR_HEX, SEVERITY_BAR_PCT, get_bot_response
from utils.image_quality import check_quality, quality_bar_html
from utils.risk_engine  import get_risk
from utils.translations import t

# ─────────────────────────────────────────────────────────────────────────────
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
_DEFAULTS = {
    "tab":           "home",
    "splash_done":   False,
    "chat":          [],
    "model_bytes":   None,
    "model_name":    None,
    "labels_str":    None,
    "last_result":   None,
    "scan_mode":     "upload",
    "lang":          "en",          # "en" | "sw"
    "quality":       None,          # last quality-check dict
    "force_analyse": False,         # bypass quality warning
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

L = st.session_state.lang           # shorthand

# ─────────────────────────────────────────────────────────────────────────────
# School logo (base64)
# ─────────────────────────────────────────────────────────────────────────────
_IMG = os.path.join(os.path.dirname(__file__), "..", "attached_assets", "image_1779873760068.png")
_b64 = ""
if os.path.exists(_IMG):
    with open(_IMG, "rb") as _f:
        _b64 = base64.b64encode(_f.read()).decode()
_img_src = f"data:image/png;base64,{_b64}" if _b64 else ""

# ─────────────────────────────────────────────────────────────────────────────
# Splash screen (once per session)
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.splash_done:
    st.session_state.splash_done = True
    logo_html = (f'<img class="sp-logo" src="{_img_src}" alt="logo"/>'
                 if _img_src else '<div class="sp-logo-ph">🌿</div>')
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
    <div class="sp-logo-wrap">{logo_html}<div class="sp-scan"></div></div>
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
  box-shadow:0 0 0 4px rgba(34,197,94,.1),0 0 40px rgba(34,197,94,.4);
  animation:sp-zoom .8s cubic-bezier(.34,1.56,.64,1) .3s both;}}
@keyframes sp-zoom{{from{{opacity:0;transform:scale(.45) rotate(-8deg)}}to{{opacity:1;transform:none}}}}
.sp-logo{{width:100%;height:100%;object-fit:cover;display:block;}}
.sp-logo-ph{{width:100%;height:100%;display:flex;align-items:center;justify-content:center;
  font-size:4.5rem;background:linear-gradient(135deg,#031a08,#052e10);}}
.sp-scan{{position:absolute;left:0;right:0;height:3px;
  background:linear-gradient(90deg,transparent,#22c55e,#4ade80,#22c55e,transparent);
  box-shadow:0 0 12px #22c55e;animation:sp-scan-a 2s ease-in-out 1s infinite;z-index:5;}}
@keyframes sp-scan-a{{0%{{top:0;opacity:.9}}100%{{top:100%;opacity:.15}}}}
.sp-badge{{border:1px solid rgba(34,197,94,.4);color:#22c55e;border-radius:20px;
  padding:4px 14px;font-size:.65rem;font-weight:700;letter-spacing:3px;
  background:rgba(34,197,94,.07);margin-bottom:12px;animation:sp-txt .8s ease .7s both;}}
.sp-title{{font-size:clamp(1.7rem,5.5vw,3rem);font-weight:900;letter-spacing:-0.5px;
  margin:0 0 9px;background:linear-gradient(135deg,#fff 0%,#a3e635 40%,#22c55e 70%,#16a34a 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 18px rgba(34,197,94,.3));animation:sp-txt .8s ease .8s both;}}
.sp-sub{{font-size:clamp(.82rem,2.5vw,1rem);color:#6ee7b7;margin:0 0 22px;animation:sp-txt .8s ease .9s both;}}
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
  const c=document.getElementById('sp-canvas');if(!c)return;
  const x=c.getContext('2d');let W,H,dots=[];
  function resize(){{W=c.width=window.innerWidth;H=c.height=window.innerHeight;}}
  window.addEventListener('resize',resize);resize();
  for(let i=0;i<75;i++)dots.push({{x:Math.random()*W,y:Math.random()*H,
    r:Math.random()*2+.4,vx:(Math.random()-.5)*.38,vy:(Math.random()-.5)*.38,
    a:Math.random()*.55+.1}});
  function draw(){{x.clearRect(0,0,W,H);
    dots.forEach(d=>{{d.x+=d.vx;d.y+=d.vy;
      if(d.x<0)d.x=W;if(d.x>W)d.x=0;if(d.y<0)d.y=H;if(d.y>H)d.y=0;
      x.beginPath();x.arc(d.x,d.y,d.r,0,Math.PI*2);
      x.fillStyle=`rgba(34,197,94,${{d.a}})`;x.fill();}});
    for(let i=0;i<dots.length;i++)for(let j=i+1;j<dots.length;j++){{
      const dx=dots[i].x-dots[j].x,dy=dots[i].y-dots[j].y,dist=Math.sqrt(dx*dx+dy*dy);
      if(dist<90){{x.beginPath();x.moveTo(dots[i].x,dots[i].y);x.lineTo(dots[j].x,dots[j].y);
        x.strokeStyle=`rgba(34,197,94,${{.1*(1-dist/90)}})`;x.lineWidth=.5;x.stroke();}}
    }}requestAnimationFrame(draw);}}
  draw();
  const msgs=['Initializing AI model…','Loading TensorFlow engine…','Calibrating disease classifier…',
    'Scanning crop database…','System ready ✓'];
  let si=0;const el=document.getElementById('sp-status');
  setInterval(()=>{{si=(si+1)%msgs.length;if(el)el.textContent=msgs[si];}},820);
}})();
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Model loader (cached by bytes hash)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading AI model…")
def _load_model(data: bytes, name: str):
    import tensorflow as tf, tempfile
    sfx = ".keras" if name.endswith(".keras") else ".h5"
    with tempfile.NamedTemporaryFile(delete=False, suffix=sfx) as f:
        f.write(data); p = f.name
    m = tf.keras.models.load_model(p); os.unlink(p)
    return m


# ─────────────────────────────────────────────────────────────────────────────
# TTS helper — injects browser Web Speech API
# ─────────────────────────────────────────────────────────────────────────────
def tts_button(text: str, lang: str = "en", label: str = "🔊 Listen"):
    """Render a small 'Listen' button that speaks `text` via the browser."""
    lang_code = "sw-KE" if lang == "sw" else "en-US"
    safe = text.replace('"', "'").replace("\n", " ").replace("<", "").replace(">", "")[:400]
    st.markdown(f"""
<button onclick="(function(){{
  if('speechSynthesis' in window){{
    window.speechSynthesis.cancel();
    var u=new SpeechSynthesisUtterance('{safe}');
    u.lang='{lang_code}';u.rate=0.88;u.pitch=1;
    window.speechSynthesis.speak(u);
  }}
}})()" style="background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.3);
  color:#22c55e;border-radius:20px;padding:5px 14px;font-size:.75rem;
  font-weight:600;cursor:pointer;letter-spacing:.5px;margin:.4rem 0;
  display:inline-flex;align-items:center;gap:5px">
  {label}
</button>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Shared: run prediction + build full result dict
# ─────────────────────────────────────────────────────────────────────────────
def _run_prediction(img_pil) -> dict | str:
    """Returns result dict or error string ("no_model" | "no_labels" | "error:…")."""
    if not st.session_state.model_bytes:   return "no_model"
    if not st.session_state.labels_str:    return "no_labels"
    try:
        model  = _load_model(st.session_state.model_bytes, st.session_state.model_name or "model.keras")
        labels = invert_labels(json.loads(st.session_state.labels_str))
        top_idx, conf, all_probs = predict(model, img_pil)
        raw    = labels.get(str(top_idx), f"Class {top_idx}")
        crop, disease = parse_label(raw)
        is_healthy    = "healthy" in raw.lower()
        sev = "None" if is_healthy else (
            DISEASE_DB.get(crop,{}).get("diseases",{}).get(disease,{}).get("severity","Unknown"))
        dis_info = DISEASE_DB.get(crop,{}).get("diseases",{}).get(disease,{})
        risk     = get_risk(disease, conf, is_healthy)
        save_prediction(crop, disease, conf, is_healthy)
        return dict(crop=crop, disease=disease, conf=conf, is_healthy=is_healthy,
                    sev=sev, all_probs=all_probs, labels=labels, dis_info=dis_info,
                    risk=risk, raw=raw, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"))
    except Exception as e:
        return f"error:{e}"


def _render_result(res: dict, lang: str = "en"):
    """Full result card: diagnosis + AI reasoning + risk + treatment + TTS."""
    is_h     = res["is_healthy"]
    conf     = res["conf"]
    sev      = res["sev"]
    risk     = res["risk"]
    ring_col = "#22c55e" if is_h else SEVERITY_COLOR_HEX.get(sev, "#f97316")
    sev_pct  = SEVERITY_BAR_PCT.get(sev, 0)
    card_cls = "res-healthy" if is_h else "res-disease"
    badge_bg = "rgba(34,197,94,.12)" if is_h else "rgba(249,115,22,.12)"
    badge_col= "#22c55e" if is_h else "#f97316"
    status_tx= t("result_healthy", lang) if is_h else t("result_disease", lang)
    name_disp= "Healthy" if is_h else res["disease"]
    pathogen = res["dis_info"].get("pathogen","—") if not is_h else "None — plant is healthy"
    recovery = res["dis_info"].get("recovery","N/A")
    urg_col  = risk["urgency_color"]

    # ── Main card ────────────────────────────────────────────────────────────
    st.markdown(f"""
<div class="{card_cls}" style="animation:fadeUp .4s ease">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:.5rem">
    <div>
      <div class="res-badge"
           style="background:{badge_bg};color:{badge_col};border:1px solid {badge_col}44">
        {status_tx}
      </div>
      <div class="res-name">{name_disp}</div>
      <div class="res-crop">{res["crop"]} · {res["timestamp"]}</div>
    </div>
  </div>

  <!-- Confidence ring -->
  <div class="conf-wrap">
    <div class="conf-ring">
      <svg viewBox="0 0 72 72" width="72" height="72">
        <circle cx="36" cy="36" r="30" fill="none" stroke="#1a2e1c" stroke-width="6"/>
        <circle cx="36" cy="36" r="30" fill="none" stroke="{ring_col}"
          stroke-width="6" stroke-linecap="round"
          stroke-dasharray="188.5"
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
      <div style="font-size:.72rem;color:#4b6050;margin-top:5px;line-height:1.4">
        {risk["confidence_explain"]}
      </div>
    </div>
  </div>

  <!-- Info grid -->
  <div class="info-grid2">
    <div class="info-cell2"><div class="lbl">🦠 Pathogen</div>
      <div class="val">{pathogen[:50]}{"…" if len(pathogen)>50 else ""}</div></div>
    <div class="info-cell2"><div class="lbl">⚡ Severity</div>
      <div class="val" style="color:{ring_col};font-weight:700">{sev}</div>
      <div style="background:#0d1117;border-radius:4px;height:4px;margin-top:5px;overflow:hidden">
        <div style="height:100%;width:{sev_pct}%;background:{ring_col};border-radius:4px"></div></div>
    </div>
    <div class="info-cell2"><div class="lbl">⏱ Recovery</div><div class="val">{recovery}</div></div>
    <div class="info-cell2"><div class="lbl">🌾 Crop</div><div class="val">{res["crop"]}</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── TTS Listen button ─────────────────────────────────────────────────────
    speak_text = (f"{'Healthy plant detected' if is_h else 'Disease detected: ' + res['disease']}. "
                  f"Confidence: {conf:.0f} percent. {risk['advice']}")
    tts_button(speak_text, lang, t("listen_btn", lang))

    # ── Urgency alert ─────────────────────────────────────────────────────────
    if not is_h:
        st.markdown(f"""
<div style="background:rgba(0,0,0,.3);border:1px solid {urg_col}44;border-left:4px solid {urg_col};
     border-radius:10px;padding:.9rem 1rem;margin:.6rem 0;animation:fadeUp .5s ease .1s both">
  <div style="font-size:.68rem;color:{urg_col};font-weight:700;letter-spacing:1px;
       text-transform:uppercase;margin-bottom:4px">{t("urgency", lang)}</div>
  <div style="font-size:.9rem;font-weight:700;color:{urg_col}">{risk["urgency_label"]}</div>
  <div style="font-size:.8rem;color:#9ca3af;margin-top:4px">{risk["advice"]}</div>
</div>""", unsafe_allow_html=True)

    # ── AI Reasoning card ─────────────────────────────────────────────────────
    reasoning_items = "".join(
        f'<div style="display:flex;align-items:center;gap:6px;padding:4px 0;'
        f'border-bottom:1px solid rgba(34,197,94,.08)">'
        f'<span style="color:#22c55e;font-size:.8rem">◉</span>'
        f'<span style="color:#c9d1d9;font-size:.83rem">{r}</span></div>'
        for r in risk["reasoning"]
    )
    st.markdown(f"""
<div class="info-blk" style="border-color:rgba(34,197,94,.2);animation:fadeUp .5s ease .15s both">
  <div class="blk-lbl" style="color:#22c55e">🧠 {t("ai_reasoning", lang)}</div>
  {reasoning_items}
</div>""", unsafe_allow_html=True)

    # ── Spread risk card ──────────────────────────────────────────────────────
    if not is_h:
        spread_cols = {"Very High":"#f85149","High":"#f97316","Medium":"#fbbf24",
                       "Low":"#22c55e","None":"#22c55e"}
        sc = spread_cols.get(risk["spread"], "#6e7681")
        st.markdown(f"""
<div class="info-grid2" style="animation:fadeUp .5s ease .2s both">
  <div class="info-cell2">
    <div class="lbl">{t("spread_risk", lang)}</div>
    <div class="val" style="color:{sc};font-weight:700">{risk["spread"]}</div>
    <div style="font-size:.72rem;color:#4b6050;margin-top:2px">Spreads every {risk["days"]} days</div>
  </div>
  <div class="info-cell2">
    <div class="lbl">{t("vector", lang)}</div>
    <div class="val">{risk["vector"]}</div>
  </div>
  <div class="info-cell2">
    <div class="lbl">{t("crop_loss", lang)}</div>
    <div class="val" style="color:{sc};font-weight:700">{risk["crop_loss_risk"]}</div>
  </div>
  <div class="info-cell2">
    <div class="lbl">⏱ SPREAD SPEED</div>
    <div class="val">{risk["days"]} days</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Symptoms / Treatment / Prevention ────────────────────────────────────
    if not is_h and res["dis_info"]:
        for icon, lbl_key, db_key in [
            ("🩺", "symptoms",  "symptoms"),
            ("💊", "treatment", "treatment"),
            ("🛡️","prevention","prevention"),
        ]:
            items = "".join(f"<li>{x}</li>" for x in res["dis_info"].get(db_key, []))
            if items:
                st.markdown(f"""
<div class="info-blk" style="animation:fadeUp .5s ease .25s both">
  <div class="blk-lbl">{icon} {t(lbl_key, lang)}</div>
  <ul>{items}</ul>
</div>""", unsafe_allow_html=True)
    elif is_h:
        st.markdown(f"""
<div class="info-blk" style="border-color:#22c55e22;animation:fadeUp .5s ease .25s both">
  <div class="blk-lbl">✅ Recommendations</div>
  <ul>
    <li>No disease detected — plant appears healthy</li>
    <li>Continue regular crop monitoring and scouting</li>
    <li>Apply preventive fungicide at start of rainy season</li>
    <li>Maintain proper plant spacing and irrigation</li>
  </ul>
</div>""", unsafe_allow_html=True)

    # ── Top-5 probabilities ───────────────────────────────────────────────────
    with st.expander("📈 Full probability breakdown"):
        top5 = sorted(enumerate(res["all_probs"]), key=lambda x: x[1], reverse=True)[:5]
        for rank, (idx, prob) in enumerate(top5, 1):
            lbl = res["labels"].get(str(idx), f"Class {idx}")
            _, d = parse_label(lbl)
            pct = prob * 100
            bar_col = ring_col if rank == 1 else "#2d4a31"
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:.6rem;padding:5px 0;
     border-bottom:1px solid #1a2e1c">
  <span style="font-size:.72rem;color:#4b6050;width:16px;text-align:right">{rank}</span>
  <span style="flex:1;font-size:.82rem;color:#c9d1d9;
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{d}</span>
  <div style="width:90px;background:#1a2e1c;border-radius:4px;height:5px">
    <div style="height:100%;width:{min(100,pct):.1f}%;background:{bar_col};border-radius:4px"></div>
  </div>
  <span style="font-size:.78rem;font-weight:700;color:{bar_col};width:38px;text-align:right">
    {pct:.1f}%</span>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# AI analysis animation
# ─────────────────────────────────────────────────────────────────────────────
def _animate_analysis(lang: str):
    """Show step-by-step AI processing animation, return when done."""
    steps = [
        (t("ai_step_1", lang), 12),
        (t("ai_step_2", lang), 18),
        (t("ai_step_3", lang), 8),
        (t("ai_step_4", lang), 8),
        (t("ai_step_5", lang), 8),
        (t("ai_step_6", lang), 6),
    ]
    total = sum(w for _, w in steps)
    slot  = st.empty()
    prog  = 0
    for i, (msg, weight) in enumerate(steps):
        prog_pct = int((prog / total) * 100)
        done_items = "".join(
            f'<div style="display:flex;align-items:center;gap:8px;opacity:.5">'
            f'<span style="color:#22c55e">✓</span>'
            f'<span style="color:#4b6050;font-size:.8rem">{steps[j][0]}</span></div>'
            for j in range(i)
        )
        slot.markdown(f"""
<div style="background:linear-gradient(135deg,#0b1e0d,#0e2510);
     border:1px solid rgba(34,197,94,.25);border-radius:18px;
     padding:1.8rem 1.5rem;text-align:center">
  <div style="font-size:2rem;margin-bottom:.8rem;
       animation:pulse-glow 1s infinite">🧬</div>
  <div style="color:#22c55e;font-weight:700;font-size:.95rem;
       letter-spacing:1px;margin-bottom:1.2rem">{msg}</div>
  {done_items}
  <div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);
       border-radius:10px;height:6px;overflow:hidden;margin-top:1rem">
    <div style="height:100%;width:{prog_pct}%;
         background:linear-gradient(90deg,#16a34a,#22c55e,#4ade80);
         border-radius:10px;transition:width .4s ease;
         box-shadow:0 0 10px rgba(34,197,94,.5)"></div>
  </div>
  <div style="color:#4b6050;font-size:.7rem;margin-top:.5rem;letter-spacing:1px">
    {prog_pct}% complete
  </div>
</div>""", unsafe_allow_html=True)
        time.sleep(0.55)
        prog += weight
    slot.empty()


# ─────────────────────────────────────────────────────────────────────────────
# TAB: HOME
# ─────────────────────────────────────────────────────────────────────────────
def tab_home():
    from utils.disease_db import DISEASE_DB as DB
    history = load_history()
    total   = len(history)
    hlth_ct = sum(1 for h in history if h.get("is_healthy"))
    dis_ct  = total - hlth_ct

    # App bar
    st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
     padding:14px 16px 4px;position:sticky;top:0;background:#080f09;z-index:100">
  <div>
    <div style="font-size:.72rem;color:#4b6050;letter-spacing:1px;text-transform:uppercase">
      {t("home_greeting", L)}</div>
    <div style="font-size:1.3rem;font-weight:800;
         background:linear-gradient(90deg,#a3e635,#22c55e);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
         background-clip:text;line-height:1.1">{t("home_title", L)}</div>
  </div>
  <div style="width:40px;height:40px;border-radius:50%;
       background:linear-gradient(135deg,#16a34a,#22c55e);
       display:flex;align-items:center;justify-content:center;font-size:1.2rem">🌿</div>
</div>""", unsafe_allow_html=True)

    # Hero CTA card
    st.markdown(f"""
<div style="margin:8px 12px 0;background:linear-gradient(135deg,#0b2e10,#0e3d15);
     border:1px solid rgba(34,197,94,.25);border-radius:20px;padding:1.4rem 1.5rem;
     box-shadow:0 8px 32px rgba(34,197,94,.1)">
  <div style="font-size:.7rem;color:#4ade80;letter-spacing:2px;
       text-transform:uppercase;font-weight:600;margin-bottom:5px">● INSTANT DIAGNOSIS</div>
  <div style="font-size:1.25rem;font-weight:800;color:#f0f6fc;line-height:1.2;margin-bottom:5px">
    {t("home_cta_title", L)}</div>
  <div style="font-size:.82rem;color:#6e8a72;margin-bottom:1rem">
    {t("home_cta_sub", L)}</div>
</div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    ca, cb = st.columns(2)
    if ca.button(t("take_photo", L), use_container_width=True, type="primary"):
        st.session_state.tab = "scan"; st.session_state.scan_mode = "camera"; st.rerun()
    if cb.button(t("upload_image", L), use_container_width=True):
        st.session_state.tab = "scan"; st.session_state.scan_mode = "upload"; st.rerun()

    # Stats
    st.markdown(f'<div class="sec-head">{t("farm_stats", L)}</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, val, lbl_key in [(c1,total,"stat_scans"),(c2,hlth_ct,"stat_healthy"),(c3,dis_ct,"stat_disease")]:
        col.markdown(
            f'<div class="stat-chip"><div class="val">{val}</div>'
            f'<div class="lbl">{t(lbl_key, L)}</div></div>',
            unsafe_allow_html=True)

    # Dashboard mini-charts (Plotly) — only when there's data
    if total >= 3:
        try:
            import plotly.graph_objects as go
            st.markdown('<div class="sec-head">DISEASE ANALYTICS</div>', unsafe_allow_html=True)

            # Disease frequency
            from collections import Counter
            disease_counts = Counter(
                h.get("disease","Unknown") for h in history if not h.get("is_healthy")
            )
            if disease_counts:
                top_diseases = disease_counts.most_common(5)
                labels = [d[:20] for d, _ in top_diseases]
                values = [v for _, v in top_diseases]
                fig_bar = go.Figure(go.Bar(
                    x=values, y=labels, orientation="h",
                    marker_color="#22c55e",
                    marker_line_color="rgba(34,197,94,.3)",
                    marker_line_width=1,
                ))
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#6e7681", size=11),
                    height=max(120, len(top_diseases)*40),
                    margin=dict(l=0,r=10,t=0,b=0),
                    xaxis=dict(gridcolor="#1a2e1c", showgrid=True),
                    yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                    showlegend=False,
                )
                st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

            # Healthy vs Disease doughnut
            fig_pie = go.Figure(go.Pie(
                labels=["Healthy","Disease"], values=[hlth_ct, dis_ct],
                hole=.65,
                marker_colors=["#22c55e","#f97316"],
                textinfo="none",
            ))
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", height=180,
                margin=dict(l=0,r=0,t=0,b=0),
                showlegend=True,
                legend=dict(font=dict(color="#6e7681",size=11),
                            orientation="h",yanchor="bottom",y=-0.1,xanchor="center",x=.5),
                annotations=[dict(text=f"{int(hlth_ct/total*100) if total else 0}%<br>Healthy",
                                  font=dict(size=13,color="#22c55e"),showarrow=False)],
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        except Exception:
            pass

    # Recent scans
    if history:
        st.markdown(f'<div class="sec-head">{t("recent_scans", L)}</div>', unsafe_allow_html=True)
        for h in reversed(history[-3:]):
            is_h   = h.get("is_healthy", True)
            dot    = "hist-dot-h" if is_h else "hist-dot-d"
            conf   = h.get("confidence", 0)
            col    = "#22c55e" if is_h else "#f97316"
            ts     = h.get("timestamp","")[:16].replace("T"," ")
            label  = "✅ Healthy" if is_h else "🦠 " + h.get("disease","?")
            st.markdown(f"""
<div class="hist-item">
  <div class="{dot}"></div>
  <div class="hist-body">
    <div class="hist-name">{label}</div>
    <div class="hist-meta">{h.get("crop","?")} · {ts}</div>
  </div>
  <div class="hist-conf" style="color:{col}">{conf:.0f}%</div>
</div>""", unsafe_allow_html=True)

    # Farming tips
    tips = [
        ("💧","Water Wisely","Morning irrigation reduces fungal risk. Use drip irrigation to save 30–50% water."),
        ("🌱","Fertilise Right","Apply basal NPK at planting, top-dress with CAN at 4–6 weeks."),
        ("🐛","Scout Weekly","Walk your field twice a week. Early detection saves 80% of treatment cost."),
        ("☀️","Prevent Disease","Rotate crops every 2–3 seasons and remove crop debris after harvest."),
    ]
    st.markdown(f'<div class="sec-head">{t("farming_tips", L)}</div>', unsafe_allow_html=True)
    for icon, title, body in tips:
        st.markdown(f"""
<div class="tip-card">
  <div class="tip-icon">{icon}</div>
  <div class="tip-title">{title}</div>
  <div class="tip-body">{body}</div>
</div>""", unsafe_allow_html=True)

    icons_row = "".join(
        f'<span title="{c}" style="font-size:1.3rem;margin:0 4px">{v["icon"]}</span>'
        for c, v in DB.items())
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

    st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;padding:14px 16px 8px;
     position:sticky;top:0;background:#080f09;z-index:100">
  <div style="font-size:1.3rem;font-weight:800;color:#f0f6fc">{t("scan_title", L)}</div>
</div>""", unsafe_allow_html=True)

    # Model settings
    with st.expander(t("model_settings", L), expanded=not bool(st.session_state.model_bytes)):
        mf = st.file_uploader("Upload Model (.keras / .h5)", type=["keras","h5"], key="model_up")
        lf = st.file_uploader("Upload Labels (class_indices.json)", type=["json"], key="labels_up")
        if mf:
            st.session_state.model_bytes = mf.read()
            st.session_state.model_name  = mf.name
            st.success("✅ Model saved")
        if lf:
            st.session_state.labels_str = lf.read().decode("utf-8")
            st.success("✅ Labels saved")
        c1, c2 = st.columns(2)
        for col, flag, ok_txt, fail_txt in [
            (c1, st.session_state.model_bytes, "✅ Model Ready", "⚠️ No Model"),
            (c2, st.session_state.labels_str,  "✅ Labels Ready","⚠️ No Labels"),
        ]:
            ok = bool(flag)
            col.markdown(
                f'<div style="background:{"rgba(34,197,94,.12)" if ok else "rgba(248,81,73,.08)"};'
                f'border:1px solid {"#22c55e44" if ok else "#f8514944"};border-radius:8px;'
                f'padding:6px 10px;text-align:center;font-size:.78rem;'
                f'color:{"#22c55e" if ok else "#f85149"}">'
                f'{"" if ok else ""}{ok_txt if ok else fail_txt}</div>',
                unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Mode toggle
    cc, cu = st.columns(2)
    if cc.button("📷 Camera", use_container_width=True,
                  type="primary" if st.session_state.scan_mode=="camera" else "secondary"):
        st.session_state.scan_mode = "camera"
        st.session_state.quality   = None
        st.session_state.force_analyse = False
        st.rerun()
    if cu.button("🖼️ Upload", use_container_width=True,
                  type="primary" if st.session_state.scan_mode=="upload" else "secondary"):
        st.session_state.scan_mode = "upload"
        st.session_state.quality   = None
        st.session_state.force_analyse = False
        st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    img_pil = None

    if st.session_state.scan_mode == "camera":
        st.markdown("""
<div style="background:#0e1a0f;border:2px solid #1a2e1c;border-radius:14px;
     padding:.8rem;text-align:center;color:#4b6050;font-size:.8rem;margin-bottom:.6rem">
  📸 Your device camera will open below — point at the leaf
</div>""", unsafe_allow_html=True)
        cam = st.camera_input("Take a photo of the leaf", label_visibility="collapsed")
        if cam:
            img_pil = Image.open(cam)
    else:
        upl = st.file_uploader("Choose a leaf image", type=["jpg","jpeg","png","webp"],
                                label_visibility="collapsed")
        if upl:
            img_pil = Image.open(upl)

    if img_pil:
        # ── Quality check ─────────────────────────────────────────────────────
        qr = check_quality(img_pil)
        st.session_state.quality = qr

        # Image preview with scan line
        st.markdown('<div class="img-preview-wrap">', unsafe_allow_html=True)
        st.image(img_pil, use_container_width=True)
        st.markdown('<div class="img-scan-line"></div></div>', unsafe_allow_html=True)

        # Quality bar
        st.markdown(quality_bar_html(qr["score"]), unsafe_allow_html=True)

        # Issues list
        if qr["issues"]:
            for code, title, hint in qr["issues"]:
                icon = {"dark":"🌑","bright":"☀️","blur":"📷","size":"🔍","mono":"🖼️"}.get(code,"⚠️")
                st.markdown(f"""
<div style="display:flex;gap:.6rem;background:#1a0c0c;border:1px solid #f8514933;
     border-radius:10px;padding:.7rem .9rem;margin:.3rem 0;align-items:flex-start">
  <span style="font-size:1rem;flex-shrink:0">{icon}</span>
  <div>
    <div style="color:#f85149;font-size:.82rem;font-weight:600">{title}</div>
    <div style="color:#9ca3af;font-size:.76rem;margin-top:2px">{hint}</div>
  </div>
</div>""", unsafe_allow_html=True)

        can_go = qr["can_proceed"] or st.session_state.force_analyse

        if not qr["can_proceed"] and not st.session_state.force_analyse:
            ra, rb = st.columns(2)
            if ra.button(t("retake", L), use_container_width=True, type="primary"):
                st.session_state.quality = None
                st.rerun()
            if rb.button(t("proceed_anyway", L), use_container_width=True):
                st.session_state.force_analyse = True
                st.rerun()
        else:
            if st.button(t("analyse_btn", L), type="primary", use_container_width=True):
                st.session_state.force_analyse = False
                _animate_analysis(L)
                result = _run_prediction(img_pil)
                if result == "no_model":
                    st.error(f"⚠️ Upload a model file in **{t('model_settings', L)}** above.")
                elif result == "no_labels":
                    st.error("⚠️ Upload class_indices.json in model settings above.")
                elif isinstance(result, str) and result.startswith("error:"):
                    st.error(f"Analysis failed: {result[6:]}", icon="❌")
                else:
                    st.session_state.last_result = result
                    _render_result(result, L)

    else:
        st.markdown(f"""
<div style="border:2px dashed #1a2e1c;border-radius:16px;padding:2.5rem 1.5rem;
     text-align:center;background:#0a120b;margin-top:4px">
  <div style="font-size:2.5rem">🍃</div>
  <div style="color:#e6edf3;font-weight:600;margin-top:8px">{t("no_image", L)}</div>
  <div style="color:#4b6050;font-size:.82rem;margin-top:4px">{t("no_image_sub", L)}</div>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB: HISTORY
# ─────────────────────────────────────────────────────────────────────────────
def tab_history():
    history = load_history()

    st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
     padding:14px 16px 8px;position:sticky;top:0;background:#080f09;z-index:100">
  <div style="font-size:1.3rem;font-weight:800;color:#f0f6fc">{t("history_title", L)}</div>
</div>""", unsafe_allow_html=True)

    if not history:
        st.markdown(f"""
<div style="text-align:center;padding:3rem 1rem">
  <div style="font-size:3rem">📋</div>
  <div style="color:#e6edf3;font-weight:600;margin-top:.8rem">{t("no_scans", L)}</div>
  <div style="color:#4b6050;font-size:.85rem;margin-top:.4rem">{t("no_scans_sub", L)}</div>
</div>""", unsafe_allow_html=True)
        return

    total  = len(history)
    hlth_ct= sum(1 for h in history if h.get("is_healthy"))
    dis_ct = total - hlth_ct
    avg_c  = sum(h.get("confidence",0) for h in history)/total if total else 0

    c1,c2,c3,c4 = st.columns(4)
    for col,val,lbl in [(c1,total,"Total"),(c2,hlth_ct,"Healthy"),
                        (c3,dis_ct,"Disease"),(c4,f"{avg_c:.0f}%","Avg")]:
        col.markdown(
            f'<div class="stat-chip"><div class="val">{val}</div>'
            f'<div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

    # Confidence trend (Plotly line chart)
    if total >= 4:
        try:
            import plotly.graph_objects as go
            confs = [h.get("confidence",0) for h in history[-20:]]
            fig = go.Figure(go.Scatter(
                y=confs, mode="lines+markers",
                line=dict(color="#22c55e", width=2),
                marker=dict(color="#22c55e", size=5),
                fill="tozeroy", fillcolor="rgba(34,197,94,.08)",
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=140, margin=dict(l=0,r=0,t=8,b=0),
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(gridcolor="#1a2e1c", range=[0,105],
                           tickfont=dict(color="#4b6050",size=10)),
                showlegend=False,
            )
            st.markdown('<div class="sec-head">CONFIDENCE TREND</div>', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        except Exception:
            pass

    st.markdown(f'<div class="sec-head">{t("all_scans", L)}</div>', unsafe_allow_html=True)
    for h in reversed(history[-50:]):
        is_h = h.get("is_healthy", True)
        dot  = "hist-dot-h" if is_h else "hist-dot-d"
        conf = h.get("confidence", 0)
        col  = "#22c55e" if is_h else "#f97316"
        ts   = h.get("timestamp","")[:16].replace("T"," ")
        name = "Healthy" if is_h else h.get("disease","?")
        st.markdown(f"""
<div class="hist-item">
  <div class="{dot}"></div>
  <div class="hist-body">
    <div class="hist-name">{"✅ " if is_h else "🦠 "}{name}</div>
    <div class="hist-meta">{h.get("crop","?")} · {ts}</div>
  </div>
  <div class="hist-conf" style="color:{col}">{conf:.0f}%</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button(t("clear_history", L), use_container_width=True):
        clear_history(); st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TAB: ASSISTANT
# ─────────────────────────────────────────────────────────────────────────────
def tab_assistant():
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;padding:14px 16px 8px;
     position:sticky;top:0;background:#080f09;z-index:100">
  <div style="width:36px;height:36px;border-radius:50%;
       background:linear-gradient(135deg,#16a34a,#22c55e);
       display:flex;align-items:center;justify-content:center;font-size:1rem">🤖</div>
  <div>
    <div style="font-size:1rem;font-weight:700;color:#f0f6fc">AI Farming Assistant</div>
    <div style="font-size:.72rem;color:#22c55e">{t("chat_online", L)}</div>
  </div>
</div>""", unsafe_allow_html=True)

    if not st.session_state.chat:
        st.session_state.chat = [{"role":"bot","text":t("chat_welcome", L)}]

    # Quick question chips
    quick = ["Fertilise tomatoes","Maize rust","Late blight","Irrigation","Improve soil pH"]
    cols  = st.columns(len(quick))
    for col, q in zip(cols, quick):
        if col.button(q, use_container_width=True, key=f"qq_{q}"):
            st.session_state.chat.append({"role":"user","text":q})
            st.session_state.chat.append({"role":"bot","text":get_bot_response(q)})
            st.rerun()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Chat messages
    for msg in st.session_state.chat:
        cls = "bubble-user" if msg["role"]=="user" else "bubble-bot"
        txt = msg["text"].replace("\n","<br>")
        st.markdown(f'<div class="{cls}">{txt}</div>', unsafe_allow_html=True)
        if msg["role"] == "bot" and len(msg["text"]) > 30:
            tts_button(msg["text"][:350], L, t("listen_btn", L))

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    with st.form("chat_input", clear_on_submit=True):
        ic, bc = st.columns([5,1])
        user_txt = ic.text_input("msg", placeholder=t("chat_placeholder", L),
                                  label_visibility="collapsed")
        send = bc.form_submit_button(t("chat_send", L), use_container_width=True)
    if send and user_txt.strip():
        st.session_state.chat.append({"role":"user","text":user_txt.strip()})
        st.session_state.chat.append({"role":"bot","text":get_bot_response(user_txt.strip())})
        st.rerun()

    if len(st.session_state.chat) > 2:
        if st.button(t("clear_chat", L), use_container_width=True):
            st.session_state.chat = []; st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TAB: PROFILE
# ─────────────────────────────────────────────────────────────────────────────
def tab_profile():
    st.markdown(f"""
<div style="padding:14px 16px 8px;position:sticky;top:0;background:#080f09;z-index:100">
  <div style="font-size:1.3rem;font-weight:800;color:#f0f6fc">{t("profile_title", L)}</div>
</div>""", unsafe_allow_html=True)

    # Avatar
    st.markdown("""
<div style="text-align:center;padding:1.4rem 0 .5rem">
  <div style="width:72px;height:72px;border-radius:50%;margin:0 auto;
       background:linear-gradient(135deg,#16a34a,#22c55e);
       display:flex;align-items:center;justify-content:center;font-size:2rem;
       box-shadow:0 0 24px rgba(34,197,94,.3)">🧑‍🌾</div>
  <div style="color:#f0f6fc;font-weight:700;font-size:1rem;margin-top:.6rem">Farmer</div>
  <div style="color:#4b6050;font-size:.78rem">AI Crop Doctor User</div>
</div>""", unsafe_allow_html=True)

    # Language toggle
    st.markdown(f'<div class="sec-head">{t("language", L)}</div>', unsafe_allow_html=True)
    lc1, lc2 = st.columns(2)
    if lc1.button(f"{'✓ ' if L=='en' else ''}{t('lang_en', L)}", use_container_width=True,
                   type="primary" if L=="en" else "secondary"):
        st.session_state.lang = "en"; st.rerun()
    if lc2.button(f"{'✓ ' if L=='sw' else ''}{t('lang_sw', L)}", use_container_width=True,
                   type="primary" if L=="sw" else "secondary"):
        st.session_state.lang = "sw"; st.rerun()

    # Model status
    st.markdown(f'<div class="sec-head">{t("model_status", L)}</div>', unsafe_allow_html=True)
    for label, flag in [("🤖 Model",  st.session_state.model_bytes),
                         ("📋 Labels", st.session_state.labels_str),
                         ("📊 Scans",  str(len(load_history())))]:
        val = (t("model_ready",L) if flag else t("model_missing",L)) if not label.startswith("📊") else flag
        col = "#22c55e" if ("✅" in str(val)) else ("#f97316" if "⚠️" in str(val) else "#c9d1d9")
        st.markdown(f"""
<div class="profile-item">
  <div class="profile-icon">📌</div>
  <div><div class="profile-label">{label}</div></div>
  <div style="color:{col};font-size:.85rem;font-weight:600">{val}</div>
</div>""", unsafe_allow_html=True)

    if st.session_state.model_bytes:
        if st.button(t("remove_model", L), use_container_width=True):
            st.session_state.model_bytes = None
            st.session_state.model_name  = None
            st.session_state.labels_str  = None
            st.rerun()

    # Supported crops
    st.markdown('<div class="sec-head">SUPPORTED CROPS</div>', unsafe_allow_html=True)
    crop_cols = st.columns(4)
    for i,(crop,info) in enumerate(DISEASE_DB.items()):
        crop_cols[i%4].markdown(
            f'<div style="text-align:center;padding:8px 4px;background:#0e1a0f;'
            f'border:1px solid #1a2e1c;border-radius:10px;margin:2px 0">'
            f'<div style="font-size:1.3rem">{info["icon"]}</div>'
            f'<div style="font-size:.65rem;color:#4b6050;margin-top:2px">{crop}</div></div>',
            unsafe_allow_html=True)

    # Disease library expandable
    st.markdown('<div class="sec-head">DISEASE LIBRARY</div>', unsafe_allow_html=True)
    for crop, info in DISEASE_DB.items():
        diseases = [d for d in info["diseases"] if d != "Healthy"]
        with st.expander(f"{info['icon']} {crop} — {len(diseases)} diseases"):
            for d in diseases:
                sev = info["diseases"][d].get("severity","?")
                c = "#f85149" if "Very" in sev else "#f97316" if sev=="High" else "#fbbf24" if "Med" in sev else "#22c55e"
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;'
                    f'padding:5px 0;border-bottom:1px solid #1a2e1c">'
                    f'<span style="color:#c9d1d9;font-size:.84rem">{d}</span>'
                    f'<span style="color:{c};font-size:.76rem;font-weight:600">{sev}</span></div>',
                    unsafe_allow_html=True)

    # About
    st.markdown(f'<div class="sec-head">{t("about", L)}</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="card">
  <div style="color:#a3e635;font-weight:700;font-size:.9rem">🌿 AI Crop Doctor</div>
  <div style="color:#6e8a72;font-size:.82rem;margin-top:.4rem;line-height:1.7">
    AI-powered plant disease detection for farmers across Africa and beyond.
    Powered by TensorFlow deep learning · 13 crops · 30+ disease classes.<br><br>
    <strong style="color:#4b6050">Built for:</strong>
    <span style="color:#6e8a72"> Farmers · Agronomists · Agriculture officers · NGOs</span>
  </div>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Render active tab
# ─────────────────────────────────────────────────────────────────────────────
tab = st.session_state.tab
if   tab == "home":    tab_home()
elif tab == "scan":    tab_scan()
elif tab == "history": tab_history()
elif tab == "assist":  tab_assistant()
elif tab == "profile": tab_profile()
else:                  tab_home()

# ─────────────────────────────────────────────────────────────────────────────
# Bottom Navigation
# ─────────────────────────────────────────────────────────────────────────────
NAV = [
    ("🏠", t("nav_home",    L), "home"),
    ("🔬", t("nav_scan",    L), "scan"),
    ("📋", t("nav_history", L), "history"),
    ("🤖", t("nav_chat",    L), "assist"),
    ("👤", t("nav_profile", L), "profile"),
]

st.markdown(f'<input type="hidden" id="active-tab-val" value="{tab}">',
            unsafe_allow_html=True)

nav_cols = st.columns(5, gap="small")
for col, (icon, label, key) in zip(nav_cols, NAV):
    active  = tab == key
    display = f"{icon}\n{'**'+label+'**' if active else label}"
    if col.button(display, key=f"nav_{key}", use_container_width=True):
        st.session_state.tab = key
        st.rerun()

# JS: fix nav to bottom + highlight active tab
st.markdown(f"""
<style>
@keyframes pulse-glow {{
  0%,100%{{box-shadow:0 0 0 0 rgba(34,197,94,.3)}}
  50%{{box-shadow:0 0 0 8px rgba(34,197,94,0)}}
}}
@keyframes fadeUp {{
  from{{opacity:0;transform:translateY(14px)}}
  to{{opacity:1;transform:translateY(0)}}
}}
</style>
<script>
(function fixNav(){{
  function apply(){{
    const activeKey = (document.getElementById('active-tab-val')||{{}}).value || 'home';
    const blocks = document.querySelectorAll('div[data-testid="stHorizontalBlock"]');
    if(!blocks.length) return;
    const last = blocks[blocks.length-1];
    document.querySelectorAll('.nav-fixed').forEach(b=>b.classList.remove('nav-fixed'));
    last.classList.add('nav-fixed');
    const tabs=['home','scan','history','assist','profile'];
    const btns=last.querySelectorAll('button');
    btns.forEach((b,i)=>{{
      b.classList.remove('nav-active');
      if(tabs[i]===activeKey) b.classList.add('nav-active');
    }});
  }}
  apply();
  const obs=new MutationObserver(apply);
  obs.observe(document.body,{{childList:true,subtree:true}});
  [100,400,900,1800].forEach(d=>setTimeout(apply,d));
}})();
</script>
""", unsafe_allow_html=True)
