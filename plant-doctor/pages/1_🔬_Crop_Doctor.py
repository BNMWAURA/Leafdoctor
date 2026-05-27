import streamlit as st
import numpy as np
import json, os, sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import inject_css
from utils.model_utils import run_inference, invert_class_indices, format_label
from utils.history import save_prediction
from utils.disease_db import DISEASE_DB

st.set_page_config(page_title="Crop Doctor · AI Crop Doctor", page_icon="🔬", layout="wide")
inject_css()

st.markdown(
    '<div class="hero-banner" style="padding:1.5rem 2rem;">'
    '<h1 style="font-size:1.8rem">🔬 Crop Doctor</h1>'
    '<p>Upload a plant leaf image for instant AI disease diagnosis</p>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Sidebar: model + labels ───────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Model Settings")
    model_file  = st.file_uploader("Upload Model (.keras / .h5)", type=["keras", "h5"])
    labels_file = st.file_uploader("Upload Class Labels (class_indices.json)", type=["json"])

    if model_file:
        st.success("✅ Model ready", icon="✅")
    else:
        st.warning("No model loaded", icon="⚠️")

    if labels_file:
        st.success("✅ Labels ready", icon="✅")
    else:
        st.warning("No labels loaded", icon="⚠️")

    st.divider()
    st.markdown("**How to use**")
    st.markdown("1. Upload your `.keras` model")
    st.markdown("2. Upload `class_indices.json`")
    st.markdown("3. Upload a leaf photo")
    st.markdown("4. Click **Analyse Crop**")
    st.divider()
    st.markdown("**Supported image formats**")
    st.caption("JPG • JPEG • PNG • WEBP")


@st.cache_resource(show_spinner="Loading AI model into memory…")
def _load_model(file_bytes: bytes, fname: str):
    import tensorflow as tf
    import tempfile
    suffix = ".keras" if fname.endswith(".keras") else ".h5"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        path = tmp.name
    model = tf.keras.models.load_model(path)
    os.unlink(path)
    return model


# ── Main layout ───────────────────────────────────────────────────────────────
upload_col, result_col = st.columns([1, 1], gap="large")

with upload_col:
    st.markdown('<div class="section-header">📸 Upload Image</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Choose plant leaf image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )

    if uploaded:
        img = Image.open(uploaded)
        st.markdown('<div class="scan-wrapper">', unsafe_allow_html=True)
        st.image(img, use_container_width=True, caption="Uploaded leaf image")
        st.markdown('</div>', unsafe_allow_html=True)

        analyse = st.button("🔬 Analyse Crop", type="primary", use_container_width=True)
    else:
        st.markdown(
            """<div style="border:2px dashed #81c784;border-radius:12px;padding:60px 20px;
                text-align:center;background:#f1f8e9;">
                <p style="font-size:2.5rem;margin:0">🍃</p>
                <p style="color:#558b2f;margin-top:8px;font-weight:500">
                    Drag & drop a leaf photo here
                </p>
                <p style="color:#81c784;font-size:0.82rem">JPG, PNG, WEBP accepted</p>
            </div>""",
            unsafe_allow_html=True,
        )
        analyse = False

with result_col:
    st.markdown('<div class="section-header">📊 Diagnosis Results</div>', unsafe_allow_html=True)

    if not uploaded:
        st.markdown(
            """<div class="glass-card" style="text-align:center;padding:60px 20px;">
                <p style="font-size:2rem">🔍</p>
                <p style="color:#558b2f">Results will appear here after analysis</p>
            </div>""",
            unsafe_allow_html=True,
        )

    elif analyse:
        if not model_file:
            st.warning("Upload a model file in the sidebar first.", icon="⚠️")
        elif not labels_file:
            st.warning("Upload class_indices.json in the sidebar first.", icon="⚠️")
        else:
            with st.spinner("🔬 AI is analysing your crop…"):
                try:
                    model  = _load_model(model_file.read(), model_file.name)
                    labels = invert_class_indices(json.loads(labels_file.read()))

                    img = Image.open(uploaded)
                    top_idx, confidence, all_probs = run_inference(model, img)

                    raw_label = labels.get(str(top_idx), f"Class {top_idx}")
                    crop, disease = format_label(raw_label)
                    is_healthy = "healthy" in raw_label.lower()

                    # Save to history
                    save_prediction(crop, disease, confidence, is_healthy)

                    # ── Result card ───────────────────────────────────
                    if is_healthy:
                        st.markdown(
                            f"""<div class="result-healthy">
                                <div style="font-size:2.5rem">✅</div>
                                <div class="result-label" style="color:#2e7d32">{crop} — Healthy</div>
                                <div class="result-conf">No disease detected</div>
                            </div>""",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""<div class="result-disease">
                                <div style="font-size:2.5rem">🦠</div>
                                <div class="result-label" style="color:#e65100">{disease}</div>
                                <div class="result-conf">Crop: {crop}</div>
                            </div>""",
                            unsafe_allow_html=True,
                        )

                    # Confidence metric
                    st.markdown("<br>", unsafe_allow_html=True)
                    m1, m2 = st.columns(2)
                    m1.metric("Confidence", f"{confidence:.1f}%")
                    m2.metric("Crop", crop)
                    st.progress(confidence / 100)

                    # Top-5
                    with st.expander("📈 Top-5 Predictions", expanded=not is_healthy):
                        top5 = sorted(enumerate(all_probs), key=lambda x: x[1], reverse=True)[:5]
                        for rank, (idx, prob) in enumerate(top5, 1):
                            lbl = labels.get(str(idx), f"Class {idx}")
                            _, d = format_label(lbl)
                            pct = prob * 100
                            cols = st.columns([4, 6])
                            cols[0].markdown(f"**{rank}. {d}**")
                            cols[1].progress(pct / 100, text=f"{pct:.1f}%")

                    # Treatment info from DB
                    if not is_healthy:
                        crop_info = DISEASE_DB.get(crop, {})
                        disease_info = crop_info.get("diseases", {}).get(disease, {})
                        if disease_info:
                            st.divider()
                            st.markdown("#### 💊 Treatment Protocol")
                            t1, t2 = st.columns(2)
                            with t1:
                                st.markdown("**Symptoms**")
                                for s in disease_info.get("symptoms", []):
                                    st.markdown(f"- {s}")
                                st.markdown(f"**Pathogen:** `{disease_info.get('pathogen','Unknown')}`")
                                st.markdown(f"**Recovery:** {disease_info.get('recovery_days','Unknown')}")
                            with t2:
                                st.markdown("**Treatment**")
                                for t in disease_info.get("treatment", []):
                                    st.markdown(f"- {t}")
                                st.markdown("**Prevention**")
                                for p in disease_info.get("prevention", []):
                                    st.markdown(f"- {p}")
                        else:
                            st.info(
                                "• Isolate affected plants immediately\n"
                                "• Remove infected leaves\n"
                                "• Consult a local agronomist for treatment\n"
                                "• Improve ventilation and avoid overhead watering",
                                icon="🌱",
                            )

                except Exception as exc:
                    st.error(f"❌ Analysis failed: {exc}", icon="❌")
                    st.caption("Ensure the model and labels match. The model must accept 224×224 or similar RGB input.")
