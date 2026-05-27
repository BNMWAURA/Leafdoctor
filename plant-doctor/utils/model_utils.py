"""TensorFlow/Keras model inference utilities."""
import numpy as np
from PIL import Image


def preprocess(image: Image.Image, size: tuple[int, int] = (224, 224)) -> np.ndarray:
    """Resize, convert RGB, normalise to [0,1], add batch dim."""
    img = image.convert("RGB").resize(size, Image.LANCZOS)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def input_size(model) -> tuple[int, int]:
    try:
        _, h, w, _ = model.input_shape
        return (int(w or 224), int(h or 224))
    except Exception:
        return (224, 224)


def predict(model, image: Image.Image) -> tuple[int, float, list[float]]:
    """Returns (top_class_idx, confidence_pct, all_probs_list)."""
    size  = input_size(model)
    arr   = preprocess(image, size)
    probs = model.predict(arr, verbose=0)[0]
    idx   = int(np.argmax(probs))
    conf  = float(probs[idx]) * 100
    return idx, conf, probs.tolist()


def invert_labels(class_indices: dict) -> dict:
    """class_indices.json: {name: idx} → {str(idx): name}."""
    return {str(v): k for k, v in class_indices.items()}


def parse_label(raw: str) -> tuple[str, str]:
    """
    'Tomato___Early_Blight' → ('Tomato', 'Early Blight')
    Returns (crop, disease).
    """
    if "___" in raw:
        crop, disease = raw.split("___", 1)
    else:
        crop, disease = "Plant", raw
    return crop.replace("_", " ").title(), disease.replace("_", " ").title()
