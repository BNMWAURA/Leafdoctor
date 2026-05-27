"""Prediction history — stored in data/history.json."""
import json, os
from datetime import datetime

_HISTORY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "history.json")


def _init():
    os.makedirs(os.path.dirname(_HISTORY_PATH), exist_ok=True)
    if not os.path.exists(_HISTORY_PATH):
        with open(_HISTORY_PATH, "w") as f:
            json.dump([], f)


def load_history() -> list[dict]:
    _init()
    with open(_HISTORY_PATH) as f:
        return json.load(f)


def save_prediction(crop: str, disease: str, confidence: float, is_healthy: bool):
    _init()
    history = load_history()
    history.append({
        "timestamp":  datetime.now().isoformat(),
        "crop":       crop,
        "disease":    disease,
        "confidence": round(confidence, 2),
        "is_healthy": is_healthy,
    })
    with open(_HISTORY_PATH, "w") as f:
        json.dump(history[-500:], f, indent=2)


def clear_history():
    _init()
    with open(_HISTORY_PATH, "w") as f:
        json.dump([], f)
