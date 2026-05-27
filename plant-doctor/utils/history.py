"""Manages prediction history stored in a local JSON file."""
import json
import os
from datetime import datetime

HISTORY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "history.json")


def _ensure_file():
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "w") as f:
            json.dump([], f)


def load_history() -> list[dict]:
    _ensure_file()
    with open(HISTORY_PATH) as f:
        return json.load(f)


def save_prediction(crop: str, disease: str, confidence: float, is_healthy: bool):
    _ensure_file()
    history = load_history()
    history.append({
        "timestamp": datetime.now().isoformat(),
        "crop": crop,
        "disease": disease,
        "confidence": round(confidence, 2),
        "is_healthy": is_healthy,
    })
    # Keep last 500 entries
    history = history[-500:]
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


def clear_history():
    _ensure_file()
    with open(HISTORY_PATH, "w") as f:
        json.dump([], f)
