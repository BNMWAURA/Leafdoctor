"""TensorFlow model loading and inference utilities."""
import os
import numpy as np
from PIL import Image


def preprocess_image(image: Image.Image, target_size: tuple[int, int] = (224, 224)) -> np.ndarray:
    img = image.convert("RGB").resize(target_size)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def get_input_size(model) -> tuple[int, int]:
    try:
        _, h, w, _ = model.input_shape
        return (int(w or 224), int(h or 224))
    except Exception:
        return (224, 224)


def run_inference(model, image: Image.Image) -> tuple[int, float, list[float]]:
    """Returns (top_class_index, confidence_0_to_100, all_probs_list)."""
    size = get_input_size(model)
    arr = preprocess_image(image, size)
    preds = model.predict(arr, verbose=0)[0]
    top_idx = int(np.argmax(preds))
    confidence = float(preds[top_idx]) * 100
    return top_idx, confidence, preds.tolist()


def invert_class_indices(class_indices: dict) -> dict:
    """Convert {class_name: idx} → {str(idx): class_name}."""
    return {str(v): k for k, v in class_indices.items()}


def format_label(raw: str) -> tuple[str, str]:
    """
    Turn 'Tomato___Leaf_Miner' → ('Tomato', 'Leaf Miner')
    Returns (crop, disease).
    """
    if "___" in raw:
        crop, disease = raw.split("___", 1)
    else:
        crop, disease = "Unknown", raw
    disease = disease.replace("_", " ").strip().title()
    crop = crop.replace("_", " ").strip().title()
    return crop, disease
