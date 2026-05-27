import streamlit as st
import numpy as np
import json
import os
from PIL import Image

st.set_page_config(
    page_title="AI Crop Doctor",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="auto",
)

# ── Header ──────────────────────────────────────────────────────────────────
st.title("🌿 AI Crop Doctor")
st.caption("Upload a plant leaf image to instantly detect diseases using AI.")
st.divider()

# ── Sidebar: Model & Labels ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("Upload your trained model and class labels below.")

    model_file = st.file_uploader(
        "Upload Model (.keras)",
        type=["keras", "h5"],
        help="Keras model file (.keras or .h5)",
    )

    labels_file = st.file_uploader(
        "Upload Class Labels (class_indices.json)",
        type=["json"],
        help="JSON file mapping class indices to disease names",
    )

    st.divider()
    st.markdown("**Supported formats**")
    st.markdown("- Images: JPG, JPEG, PNG, WEBP")
    st.markdown("- Model: `.keras` / `.h5`")
    st.markdown("- Labels: `class_indices.json`")

    st.divider()
    st.info(
        "💡 **Tip:** Load your model once and it will be cached for faster "
        "predictions on subsequent uploads.",
        icon="💡",
    )

# ── Load model (cached) ───────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading model into memory…")
def load_model_from_bytes(file_bytes: bytes, file_name: str):
    import tensorflow as tf
    import tempfile

    suffix = ".keras" if file_name.endswith(".keras") else ".h5"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    model = tf.keras.models.load_model(tmp_path)
    os.unlink(tmp_path)
    return model


def load_labels(file_bytes: bytes) -> dict:
    data = json.loads(file_bytes.decode("utf-8"))
    # class_indices.json is {class_name: index} — invert to {index: class_name}
    return {str(v): k for k, v in data.items()}


def preprocess_image(image: Image.Image, target_size=(224, 224)) -> np.ndarray:
    img = image.convert("RGB").resize(target_size)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def format_label(raw: str) -> str:
    """Turn 'Tomato___Leaf_Miner' → 'Tomato — Leaf Miner'."""
    parts = raw.replace("___", " — ").replace("_", " ").split(" — ")
    return " — ".join(p.strip().title() for p in parts)


# ── Main content ──────────────────────────────────────────────────────────────
col_upload, col_preview = st.columns([1, 1], gap="large")

with col_upload:
    st.subheader("📸 Upload Leaf Image")
    uploaded_image = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )

with col_preview:
    if uploaded_image:
        st.subheader("🔍 Preview")
        image = Image.open(uploaded_image)
        st.image(image, use_container_width=True)
    else:
        st.subheader("🔍 Preview")
        st.markdown(
            """
            <div style="
                border: 2px dashed #81c784;
                border-radius: 12px;
                padding: 48px 16px;
                text-align: center;
                color: #558b2f;
                background: #f1f8e9;
            ">
                <p style="font-size: 2rem; margin:0;">🍃</p>
                <p style="margin-top: 8px;">Your image will appear here</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ── Prediction ────────────────────────────────────────────────────────────────
if uploaded_image:
    run_col, _ = st.columns([1, 2])
    with run_col:
        predict_btn = st.button(
            "🔬 Analyse Crop",
            use_container_width=True,
            type="primary",
        )

    if predict_btn:
        if model_file is None:
            st.warning(
                "⚠️ No model loaded. Please upload a `.keras` or `.h5` model file "
                "in the sidebar first.",
                icon="⚠️",
            )
        elif labels_file is None:
            st.warning(
                "⚠️ No class labels loaded. Please upload a `class_indices.json` "
                "file in the sidebar first.",
                icon="⚠️",
            )
        else:
            with st.spinner("Running AI analysis…"):
                try:
                    model = load_model_from_bytes(
                        model_file.read(), model_file.name
                    )
                    labels = load_labels(labels_file.read())

                    # Re-open since the uploader stream may be exhausted
                    image = Image.open(uploaded_image)

                    # Try to infer input size from model
                    try:
                        _, h, w, _ = model.input_shape
                        target_size = (w or 224, h or 224)
                    except Exception:
                        target_size = (224, 224)

                    input_arr = preprocess_image(image, target_size)
                    preds = model.predict(input_arr, verbose=0)[0]

                    top_idx = int(np.argmax(preds))
                    confidence = float(preds[top_idx]) * 100
                    raw_label = labels.get(str(top_idx), f"Class {top_idx}")
                    friendly_label = format_label(raw_label)

                    is_healthy = "healthy" in raw_label.lower()

                    st.divider()
                    st.subheader("📊 Diagnosis Results")

                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        if is_healthy:
                            st.success(f"✅ {friendly_label}", icon="✅")
                        else:
                            st.error(f"🦠 {friendly_label}", icon="🦠")

                    with res_col2:
                        bar_color = "normal" if is_healthy else "inverse"
                        st.metric(
                            label="Confidence",
                            value=f"{confidence:.1f}%",
                        )

                    st.progress(confidence / 100)

                    # Top-5 predictions
                    with st.expander("📈 Top-5 Predictions", expanded=False):
                        top5_idx = np.argsort(preds)[::-1][:5]
                        for rank, idx in enumerate(top5_idx, 1):
                            lbl = format_label(
                                labels.get(str(idx), f"Class {idx}")
                            )
                            prob = float(preds[idx]) * 100
                            cols = st.columns([3, 7])
                            cols[0].markdown(f"**{rank}. {lbl}**")
                            cols[1].progress(prob / 100, text=f"{prob:.1f}%")

                    # Treatment hint
                    if not is_healthy:
                        st.divider()
                        st.subheader("💊 General Recommendations")
                        st.info(
                            "• Isolate affected plants to prevent disease spread.\n"
                            "• Remove and destroy visibly infected leaves.\n"
                            "• Consult a local agronomist for targeted treatment.\n"
                            "• Improve air circulation and avoid overhead watering.",
                            icon="🌱",
                        )

                except Exception as exc:
                    st.error(
                        f"❌ Prediction failed: {exc}\n\n"
                        "Ensure the model and labels match the uploaded image.",
                        icon="❌",
                    )
else:
    st.info(
        "Upload a plant leaf image above to get started.",
        icon="👆",
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:#81c784; font-size:0.85rem;'>"
    "AI Crop Doctor · Powered by TensorFlow & Streamlit"
    "</p>",
    unsafe_allow_html=True,
)
