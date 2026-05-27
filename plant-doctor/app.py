"""
Thiru Mkulima AI — Main detection page.
Opens immediately to the disease detection interface (no landing page).
"""
import streamlit as st
import numpy as np
import json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from utils.styles import inject_css
from utils.model_utils import predict, invert_labels, parse_label
from utils.history import save_prediction
from utils.disease_db import DISEASE_DB, SEVERITY_COLOR_HEX, SEVERITY_BAR_PCT

st.set_page_config(
    page_title="Thiru Mkulima AI",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_css()

# ── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌿 Thiru Mkulima AI")
    st.caption("AI-powered crop disease detection")
    st.divider()
    st.markdown("**Navigation**")
    st.page_link("app.py",                       label="🔬 Detect Disease",  icon=None)
    st.page_link("pages/1_📊_Dashboard.py",       label="📊 Analytics",       icon=None)
    st.page_link("pages/2_🤖_AI_Assistant.py",    label="🤖 AI Assistant",    icon=None)
    st.page_link("pages/3_📚_Disease_Library.py", label="📚 Disease Library", icon=None)
    st.divider()
    st.markdown("**Load AI Model**")
    model_file  = st.file_uploader("Model (.keras / .h5)", type=["keras", "h5"])
    labels_file = st.file_uploader("Labels (class_indices.json)", type=["json"])
    if model_file:
        st.success("Model ready ✓")
    if labels_file:
        st.success("Labels ready ✓")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-title">Thiru Mkulima AI</div>
    <div class="app-subtitle">AI-powered crop disease detection system</div>
</div>
""", unsafe_allow_html=True)


# ── Model loader (cached) ─────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading AI model…")
def _load_model(data: bytes, name: str):
    import tensorflow as tf, tempfile
    sfx = ".keras" if name.endswith(".keras") else ".h5"
    with tempfile.NamedTemporaryFile(delete=False, suffix=sfx) as f:
        f.write(data)
        p = f.name
    m = tf.keras.models.load_model(p)
    os.unlink(p)
    return m


# ── Upload section ────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Upload a plant leaf image",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
    help="Supports JPG, PNG, WEBP",
)

if not uploaded:
    st.markdown("""
    <div class="upload-zone">
        <span class="upload-icon">🍃</span>
        <div class="upload-text">Drop your leaf image here</div>
        <div class="upload-hint">Supports JPG · PNG · WEBP · Drag & drop or click to browse</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;margin-top:2rem;color:#6e7681;font-size:0.82rem;">
        Supports 13 crops · 30+ disease classes · Powered by TensorFlow
    </div>
    """, unsafe_allow_html=True)

else:
    from PIL import Image

    img = Image.open(uploaded)

    # ── Image preview with scan line ─────────────────────────────────────────
    col_img, col_action = st.columns([3, 2], gap="large")

    with col_img:
        st.markdown('<div class="image-preview-wrapper">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown("""
        <div class="scan-overlay"></div>
        <div class="scanning-text">● Ready to analyse</div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_action:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-card">
            <div style="color:#6e7681;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px">Image loaded</div>
            <div style="color:#e6edf3;font-weight:600;margin-top:4px">{uploaded.name}</div>
            <div style="color:#6e7681;font-size:0.82rem;margin-top:2px">{img.size[0]}×{img.size[1]} px · {img.mode}</div>
        </div>
        """, unsafe_allow_html=True)

        analyse = st.button("🔬 Analyse Crop", type="primary", use_container_width=True)

        st.markdown("""
        <div style="color:#6e7681;font-size:0.78rem;text-align:center;margin-top:0.8rem">
            Load model &amp; labels in the<br>sidebar before analysing
        </div>
        """, unsafe_allow_html=True)

    # ── Prediction ────────────────────────────────────────────────────────────
    if analyse:
        if not model_file:
            st.error("⚠️ No model loaded — upload a `.keras` or `.h5` file in the sidebar.", icon="⚠️")
        elif not labels_file:
            st.error("⚠️ No class labels — upload `class_indices.json` in the sidebar.", icon="⚠️")
        else:
            # Animated status
            status = st.empty()
            status.markdown("""
            <div style="text-align:center;padding:2rem;color:#22c55e">
                <div style="font-size:2rem;animation:pulse-ring 1.5s infinite">🧬</div>
                <div style="margin-top:0.6rem;font-size:0.9rem;letter-spacing:2px;
                     text-transform:uppercase;font-weight:600">
                     Analysing crop image…
                </div>
                <div style="color:#6e7681;font-size:0.78rem;margin-top:4px">
                     AI model processing · please wait
                </div>
            </div>
            """, unsafe_allow_html=True)

            try:
                model  = _load_model(model_file.read(), model_file.name)
                labels = invert_labels(json.loads(labels_file.read()))

                img_fresh = Image.open(uploaded)
                top_idx, conf, all_probs = predict(model, img_fresh)

                raw_label = labels.get(str(top_idx), f"Class {top_idx}")
                crop, disease = parse_label(raw_label)
                is_healthy = "healthy" in raw_label.lower()

                save_prediction(crop, disease, conf, is_healthy)
                status.empty()

                # ── Result card ───────────────────────────────────────────────
                card_cls  = "result-card-healthy"  if is_healthy else "result-card-disease"
                badge_cls = "result-status-badge-healthy" if is_healthy else "result-status-badge-disease"
                status_txt = "✅ HEALTHY PLANT" if is_healthy else "⚠️ DISEASE DETECTED"
                display_name = "Healthy" if is_healthy else disease
                sev = "None" if is_healthy else (
                    DISEASE_DB.get(crop, {}).get("diseases", {}).get(disease, {}).get("severity", "Unknown")
                )
                sev_color = SEVERITY_COLOR_HEX.get(sev, "#6e7681")
                sev_pct   = SEVERITY_BAR_PCT.get(sev, 0)

                # Ring stroke calculation (r=34, circumference≈213.6)
                circ   = 213.63
                stroke = circ - (conf / 100) * circ
                ring_color = "#22c55e" if is_healthy else sev_color

                st.markdown(f"""
                <div class="result-wrapper">
                  <div class="{card_cls}">
                    <div class="{badge_cls}">{status_txt}</div>
                    <div class="result-disease-name">{display_name}</div>
                    <div class="result-crop-name">Crop: {crop}</div>

                    <!-- Confidence ring + bar -->
                    <div class="conf-ring-wrapper">
                      <div class="conf-ring">
                        <svg viewBox="0 0 80 80" width="80" height="80">
                          <circle class="conf-ring-bg" cx="40" cy="40" r="34"/>
                          <circle class="conf-ring-fg"
                            cx="40" cy="40" r="34"
                            stroke="{ring_color}"
                            stroke-dasharray="{circ:.2f}"
                            stroke-dashoffset="{stroke:.2f}"/>
                        </svg>
                        <div class="conf-ring-text">
                          <span class="conf-pct">{conf:.0f}%</span>
                          <span class="conf-label">AI conf</span>
                        </div>
                      </div>
                      <div class="conf-detail">
                        <div class="conf-detail-label">AI Confidence Score</div>
                        <div class="conf-bar-track">
                          <div class="conf-bar-fill"
                               style="width:{conf:.1f}%;background:{ring_color}"></div>
                        </div>
                        <div style="display:flex;justify-content:space-between;
                             margin-top:4px;font-size:0.75rem;color:#6e7681;">
                          <span>0%</span><span>50%</span><span>100%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Info grid ─────────────────────────────────────────────────
                dis_info = DISEASE_DB.get(crop, {}).get("diseases", {}).get(disease, {})
                pathogen  = dis_info.get("pathogen", "—") if not is_healthy else "None — plant is healthy"
                recovery  = dis_info.get("recovery", "N/A")

                sev_display = (
                    f'<span style="color:{sev_color};font-weight:600">{sev}</span>'
                    if sev != "None"
                    else '<span style="color:#22c55e;font-weight:600">✅ None — Healthy</span>'
                )

                st.markdown(f"""
                <div class="info-grid" style="margin-top:1rem">
                  <div class="info-cell">
                    <div class="info-cell-label">🦠 Pathogen</div>
                    <div class="info-cell-value">{pathogen}</div>
                  </div>
                  <div class="info-cell">
                    <div class="info-cell-label">⚡ Severity</div>
                    <div class="info-cell-value">{sev_display}</div>
                  </div>
                  <div class="info-cell">
                    <div class="info-cell-label">🕐 Recovery</div>
                    <div class="info-cell-value">{recovery}</div>
                  </div>
                  <div class="info-cell">
                    <div class="info-cell-label">🌾 Crop</div>
                    <div class="info-cell-value">{crop}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                if not is_healthy and dis_info:
                    # Treatment block
                    treatments = "".join(f"<li>{t}</li>" for t in dis_info.get("treatment", []))
                    prevention = "".join(f"<li>{p}</li>" for p in dis_info.get("prevention", []))
                    symptoms   = "".join(f"<li>{s}</li>" for s in dis_info.get("symptoms", []))

                    st.markdown(f"""
                    <div class="info-block" style="margin-top:1rem">
                      <div class="info-block-label">🩺 Symptoms</div>
                      <ul>{symptoms}</ul>
                    </div>
                    <div class="info-block">
                      <div class="info-block-label">💊 Treatment Protocol</div>
                      <ul>{treatments}</ul>
                    </div>
                    <div class="info-block">
                      <div class="info-block-label">🛡️ Prevention Measures</div>
                      <ul>{prevention}</ul>
                    </div>
                    """, unsafe_allow_html=True)
                elif is_healthy:
                    st.markdown("""
                    <div class="info-block" style="margin-top:1rem;border-color:#22c55e22">
                      <div class="info-block-label">✅ Plant Status</div>
                      <ul>
                        <li>No disease signs detected — plant appears healthy</li>
                        <li>Continue regular crop monitoring and management</li>
                        <li>Scout twice weekly during humid periods</li>
                        <li>Apply preventive fungicide at start of rainy season</li>
                      </ul>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Top-5 predictions ─────────────────────────────────────────
                with st.expander("📈 All probability scores", expanded=False):
                    top5 = sorted(enumerate(all_probs), key=lambda x: x[1], reverse=True)[:5]
                    items_html = ""
                    for rank, (idx, prob) in enumerate(top5, 1):
                        lbl = labels.get(str(idx), f"Class {idx}")
                        _, d = parse_label(lbl)
                        pct = prob * 100
                        bar_w = min(100, pct)
                        items_html += f"""
                        <div class="top5-item">
                          <span class="top5-rank">{rank}</span>
                          <span class="top5-name">{d}</span>
                          <div class="top5-bar-wrap">
                            <div class="top5-bar-track">
                              <div class="top5-bar-fill" style="width:{bar_w:.1f}%"></div>
                            </div>
                          </div>
                          <span class="top5-pct">{pct:.1f}%</span>
                        </div>"""
                    st.markdown(f'<div style="padding:0.3rem 0">{items_html}</div>',
                                unsafe_allow_html=True)

            except Exception as exc:
                status.empty()
                st.error(f"**Analysis failed:** {exc}", icon="❌")
                st.caption("Make sure the model file and class_indices.json match each other, and that the model accepts RGB image input.")

# ── Supported crops strip ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
crop_items = [(v["icon"], k) for k, v in __import__(
    "utils.disease_db", fromlist=["DISEASE_DB"]).DISEASE_DB.items()]
icons_row = "".join(
    f'<span title="{c}" style="margin:0 6px;font-size:1.4rem;cursor:default">{i}</span>'
    for i, c in crop_items
)
st.markdown(
    f'<div style="text-align:center;padding:0.8rem 0;border-top:1px solid #21262d;'
    f'margin-top:0.5rem;color:#6e7681;font-size:0.78rem;">'
    f'Supported crops&nbsp;&nbsp;{icons_row}</div>',
    unsafe_allow_html=True,
)
