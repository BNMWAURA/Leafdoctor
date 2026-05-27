"""Image quality assessment — blur, brightness, resolution checks."""
import numpy as np
from PIL import Image, ImageFilter


def check_quality(img: Image.Image) -> dict:
    """
    Returns:
        score        : 0-100 overall quality score
        issues       : list of (code, title, hint) tuples
        can_proceed  : True if quality is good enough for AI analysis
        brightness   : 0.0-1.0 mean brightness
        sharpness    : Laplacian variance (higher = sharper)
        grade        : 'good' | 'acceptable' | 'poor'
    """
    img_rgb = img.convert("RGB")
    arr = np.array(img_rgb, dtype=np.float32)

    brightness = float(arr.mean()) / 255.0

    # Sharpness: variance of Laplacian edges (higher = sharper, clearer leaf detail)
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    sharpness = float(np.array(edges, dtype=np.float32).var())

    w, h = img.size
    pixels = w * h

    issues = []
    penalty = 0

    # ── Brightness checks ──────────────────────────────────────────────────
    if brightness < 0.15:
        issues.append(("dark", "Image is too dark",
                        "Take the photo in natural daylight or bright indoor light."))
        penalty += 40
    elif brightness < 0.28:
        issues.append(("dark", "Image is slightly dark",
                        "Better lighting will improve AI accuracy."))
        penalty += 18
    elif brightness > 0.88:
        issues.append(("bright", "Image is overexposed",
                        "Avoid pointing camera directly at sunlight."))
        penalty += 22

    # ── Sharpness / blur ──────────────────────────────────────────────────
    if sharpness < 60:
        issues.append(("blur", "Image is blurry",
                        "Hold the phone steady and tap the screen to focus."))
        penalty += 35
    elif sharpness < 180:
        issues.append(("blur", "Image could be sharper",
                        "Clean camera lens and retake for better results."))
        penalty += 12

    # ── Resolution ────────────────────────────────────────────────────────
    if pixels < 10_000:
        issues.append(("size", "Image resolution too low",
                        "Use a camera with at least 1 MP resolution."))
        penalty += 30
    elif pixels < 40_000:
        issues.append(("size", "Image resolution is low",
                        "Higher resolution gives better AI accuracy."))
        penalty += 10

    # ── Colour variety (all-green / all-one-color may not be a leaf) ──────
    std = float(arr.std())
    if std < 8:
        issues.append(("mono", "Image looks uniform",
                        "Ensure the leaf fills the frame clearly."))
        penalty += 20

    score = max(0, 100 - penalty)
    grade = "good" if score >= 75 else ("acceptable" if score >= 45 else "poor")

    return {
        "score":       score,
        "grade":       grade,
        "issues":      issues,
        "can_proceed": score >= 40,
        "brightness":  round(brightness, 3),
        "sharpness":   round(sharpness, 1),
        "size":        (w, h),
    }


def quality_bar_html(score: int) -> str:
    """Returns an HTML quality meter string for st.markdown."""
    if score >= 75:
        col, label = "#22c55e", "Good"
    elif score >= 45:
        col, label = "#fbbf24", "Acceptable"
    else:
        col, label = "#f85149", "Poor"

    return f"""
<div style="margin:.6rem 0">
  <div style="display:flex;justify-content:space-between;
       font-size:.72rem;color:#4b6050;margin-bottom:4px">
    <span>Image Quality</span>
    <span style="color:{col};font-weight:700">{label} · {score}/100</span>
  </div>
  <div style="background:#1a2e1c;border-radius:6px;height:6px;overflow:hidden">
    <div style="height:100%;width:{score}%;background:{col};
         border-radius:6px;transition:width .8s ease"></div>
  </div>
</div>"""
