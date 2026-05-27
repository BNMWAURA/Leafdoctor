"""Smart risk engine — spread risk, urgency, crop loss analysis."""

# Disease-specific spread + risk data
_RISK_DB: dict[str, dict] = {
    # Tomato
    "Early Blight":          {"spread": "Medium",    "days": "7–14",   "vector": "Wind & rain splash",       "loss": "15–40%"},
    "Late Blight":           {"spread": "Very High", "days": "2–5",    "vector": "Cool wet wind",            "loss": "40–100%"},
    "Septoria Leaf Spot":    {"spread": "High",      "days": "5–10",   "vector": "Rain splash",              "loss": "20–50%"},
    "Leaf Mold":             {"spread": "Medium",    "days": "8–15",   "vector": "High humidity air",        "loss": "10–30%"},
    "Spider Mites":          {"spread": "High",      "days": "4–8",    "vector": "Wind, contact",            "loss": "15–35%"},
    "Target Spot":           {"spread": "Medium",    "days": "7–12",   "vector": "Rain splash & wind",       "loss": "10–25%"},
    "Yellow Leaf Curl Virus":{"spread": "Very High", "days": "1–3",    "vector": "Whitefly insects",         "loss": "30–80%"},
    "Mosaic Virus":          {"spread": "High",      "days": "3–7",    "vector": "Aphids & tools",           "loss": "20–60%"},
    # Maize
    "Gray Leaf Spot":        {"spread": "High",      "days": "5–10",   "vector": "Wind & rain",              "loss": "20–50%"},
    "Common Rust":           {"spread": "Very High", "days": "3–6",    "vector": "Wind (long distance)",     "loss": "20–70%"},
    "Northern Leaf Blight":  {"spread": "High",      "days": "5–9",    "vector": "Wind & rain splash",       "loss": "25–60%"},
    # Potato
    "Early Blight Potato":   {"spread": "Medium",    "days": "7–14",   "vector": "Rain splash",              "loss": "15–35%"},
    "Late Blight Potato":    {"spread": "Very High", "days": "2–4",    "vector": "Cool wind & fog",          "loss": "50–100%"},
    # Rice
    "Leaf Blast":            {"spread": "Very High", "days": "3–7",    "vector": "Wind",                     "loss": "30–70%"},
    "Brown Spot":            {"spread": "Medium",    "days": "6–12",   "vector": "Wind & rain",              "loss": "10–40%"},
    # Coffee
    "Leaf Rust":             {"spread": "High",      "days": "5–14",   "vector": "Wind & rain",              "loss": "20–50%"},
    "Healthy":               {"spread": "None",      "days": "N/A",    "vector": "N/A",                      "loss": "0%"},
}

_URGENCY = {
    "Very High": ("🔴 URGENT — Act within 24 hours",    "#f85149"),
    "High":      ("🟠 HIGH — Treat within 2–3 days",    "#f97316"),
    "Medium":    ("🟡 MODERATE — Treat within a week",  "#fbbf24"),
    "Low":       ("🟢 LOW — Monitor closely",           "#22c55e"),
    "None":      ("✅ HEALTHY — Keep monitoring",        "#22c55e"),
}

_AI_REASONING: dict[str, list[str]] = {
    "Early Blight":           ["Brown concentric ring lesions detected", "Target-like spots on lower leaves", "Yellowing around lesion edges"],
    "Late Blight":            ["Dark water-soaked spots identified", "White mold edge on underside", "Rapid lesion spread pattern"],
    "Septoria Leaf Spot":     ["Small brown circular spots found", "Dark borders with light centers", "Concentrated on older leaves"],
    "Leaf Mold":              ["Yellow patches on upper surface detected", "Olive-grey mold on underside", "Moisture-associated patterns"],
    "Spider Mites":           ["Fine webbing patterns detected", "Stippled bronzing on leaf surface", "Edge feeding damage identified"],
    "Yellow Leaf Curl Virus": ["Upward leaf curling detected", "Yellowing along leaf margins", "Stunted growth pattern identified"],
    "Mosaic Virus":           ["Mosaic colour patterning found", "Light-green mottling on surface", "Distorted leaf texture detected"],
    "Gray Leaf Spot":         ["Rectangular lesions between veins", "Gray-brown coloration identified", "Long narrow spots detected"],
    "Common Rust":            ["Orange-brown pustules detected", "Powdery rust spore clusters", "Pustule pattern on leaf surface"],
    "Northern Leaf Blight":   ["Long cigar-shaped lesions found", "Gray-green early stage spots", "Expanding water-soaked edges"],
    "Late Blight Potato":     ["Dark irregular blotches detected", "Water-soaked lesion margins", "Rapid spreading edge pattern"],
    "Leaf Blast":             ["Diamond-shaped lesions found", "Gray-white center with brown border", "Blast lesion halo pattern"],
    "Brown Spot":             ["Oval brown spots with yellow halo", "Necrotic center detected", "Scattered spot distribution"],
    "Leaf Rust":              ["Rust-orange pustules identified", "Circular uredinia clusters", "Underside powder deposits"],
    "Healthy":                ["Uniform green coloration confirmed", "No lesion or spot patterns", "Healthy leaf texture detected"],
}


def get_risk(disease: str, confidence: float, is_healthy: bool) -> dict:
    """
    Returns a full risk assessment dictionary.
    disease   : parsed disease name (e.g. 'Early Blight')
    confidence: 0-100 float
    is_healthy: bool
    """
    if is_healthy:
        return {
            "spread":         "None",
            "days":           "N/A",
            "vector":         "N/A",
            "loss":           "0%",
            "urgency_label":  "✅ HEALTHY — Keep monitoring",
            "urgency_color":  "#22c55e",
            "reasoning":      _AI_REASONING.get("Healthy", ["Healthy leaf patterns detected"]),
            "crop_loss_risk": "Minimal",
            "advice":         "Your crop looks healthy! Continue regular scouting and preventive care.",
            "confidence_explain": _confidence_explain(confidence),
        }

    info = _RISK_DB.get(disease, {
        "spread": "Unknown", "days": "?", "vector": "Unknown", "loss": "?"
    })
    spread     = info["spread"]
    urg_label, urg_color = _URGENCY.get(spread, ("⚠️ Unknown risk", "#4b6050"))

    return {
        "spread":         spread,
        "days":           info["days"],
        "vector":         info["vector"],
        "loss":           info["loss"],
        "urgency_label":  urg_label,
        "urgency_color":  urg_color,
        "reasoning":      _AI_REASONING.get(disease, ["Pattern analysis complete", "Disease markers identified"]),
        "crop_loss_risk": info["loss"],
        "advice":         _advice(disease, spread),
        "confidence_explain": _confidence_explain(confidence),
    }


def _confidence_explain(c: float) -> str:
    if c >= 90:
        return f"Very high confidence ({c:.0f}%) — strong visual disease markers present."
    elif c >= 75:
        return f"High confidence ({c:.0f}%) — clear disease patterns detected."
    elif c >= 55:
        return f"Moderate confidence ({c:.0f}%) — some markers present; consider expert review."
    else:
        return f"Low confidence ({c:.0f}%) — image quality or early-stage disease may affect accuracy."


def _advice(disease: str, spread: str) -> str:
    urgency_map = {
        "Very High": "Act immediately — remove infected plants, apply fungicide today.",
        "High":      "Treat within 48 hours — isolate affected area and apply recommended fungicide.",
        "Medium":    "Schedule treatment this week — monitor daily for spread.",
        "Low":       "Monitor the field — apply preventive spray if symptoms worsen.",
    }
    return urgency_map.get(spread, "Consult your local agriculture officer for advice.")
