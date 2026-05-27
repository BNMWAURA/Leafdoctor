import streamlit as st
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import inject_css
from utils.disease_db import DISEASE_DB, SEVERITY_COLOR

st.set_page_config(page_title="Disease Library · AI Crop Doctor", page_icon="📚", layout="wide")
inject_css()

st.markdown(
    '<div class="hero-banner" style="padding:1.5rem 2rem;">'
    '<h1 style="font-size:1.8rem">📚 Disease Library</h1>'
    '<p>Encyclopaedia of crop diseases, symptoms, treatments & prevention</p>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Filter controls ───────────────────────────────────────────────────────────
filter_col, sev_col, search_col = st.columns([2, 2, 3])

crop_options = ["All Crops"] + list(DISEASE_DB.keys())
selected_crop = filter_col.selectbox("Filter by Crop", crop_options)

sev_options = ["All Severities", "None", "Low", "Low-Medium", "Medium", "Medium-High", "High", "Very High"]
selected_sev = sev_col.selectbox("Filter by Severity", sev_options)

search_term = search_col.text_input("🔍 Search diseases…", placeholder="e.g. rust, blight, mosaic")

st.markdown("<br>", unsafe_allow_html=True)

# ── Display library ───────────────────────────────────────────────────────────
any_shown = False

for crop_name, crop_data in DISEASE_DB.items():
    if selected_crop != "All Crops" and crop_name != selected_crop:
        continue

    diseases_to_show = {}
    for dis_name, dis_data in crop_data["diseases"].items():
        if dis_name == "Healthy":
            continue
        if selected_sev != "All Severities" and dis_data.get("severity") != selected_sev:
            continue
        if search_term:
            haystack = (
                dis_name + " " +
                dis_data.get("pathogen", "") + " " +
                " ".join(dis_data.get("symptoms", [])) + " " +
                crop_name
            ).lower()
            if search_term.lower() not in haystack:
                continue
        diseases_to_show[dis_name] = dis_data

    if not diseases_to_show:
        continue

    any_shown = True
    icon = crop_data["icon"]

    st.markdown(
        f'<div class="section-header">{icon} {crop_name}</div>',
        unsafe_allow_html=True,
    )

    for dis_name, dis_data in diseases_to_show.items():
        severity = dis_data.get("severity", "Unknown")
        sev_icon = SEVERITY_COLOR.get(severity, "⚪")
        pathogen = dis_data.get("pathogen", "Unknown")
        recovery = dis_data.get("recovery_days", "Unknown")

        with st.expander(f"{sev_icon} **{dis_name}** — {crop_name} · Severity: {severity}"):
            d1, d2, d3 = st.columns(3)

            with d1:
                st.markdown("#### 🔬 Pathogen")
                st.markdown(f"`{pathogen}`")
                st.markdown("#### 🕐 Recovery Time")
                st.markdown(f"{recovery}")
                st.markdown("#### 🩺 Symptoms")
                for s in dis_data.get("symptoms", []):
                    st.markdown(f"- {s}")

            with d2:
                st.markdown("#### ⚠️ Causes")
                for c in dis_data.get("causes", []):
                    st.markdown(f"- {c}")
                st.markdown("#### 💊 Treatment")
                for t in dis_data.get("treatment", []):
                    st.markdown(f"- {t}")

            with d3:
                st.markdown("#### 🛡️ Prevention")
                for p in dis_data.get("prevention", []):
                    st.markdown(f"- {p}")

            # Severity gauge
            sev_map = {"None": 0, "Low": 15, "Low-Medium": 30, "Medium": 50,
                       "Medium-High": 65, "High": 80, "Very High": 100}
            sev_pct = sev_map.get(severity, 0)
            bar_color = (
                "#4caf50" if sev_pct < 30
                else "#ff9800" if sev_pct < 70
                else "#f44336"
            )
            st.markdown(
                f"""<div style="margin-top:8px">
                    <span style="font-size:0.8rem;color:#555">Severity level:</span>
                    <div style="background:#f1f1f1;border-radius:8px;height:10px;margin-top:4px;">
                        <div style="width:{sev_pct}%;background:{bar_color};
                            height:10px;border-radius:8px;transition:width 0.5s;">
                        </div>
                    </div>
                    <span style="font-size:0.78rem;color:{bar_color};font-weight:600">{severity}</span>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

if not any_shown:
    st.warning("No diseases match your current filters. Try broadening the search.", icon="🔍")

# ── Summary table ─────────────────────────────────────────────────────────────
with st.expander("📋 Full Disease Summary Table", expanded=False):
    rows = []
    for crop_name, crop_data in DISEASE_DB.items():
        for dis_name, dis_data in crop_data["diseases"].items():
            if dis_name == "Healthy":
                continue
            rows.append({
                "Crop":     crop_name,
                "Disease":  dis_name,
                "Pathogen": dis_data.get("pathogen", ""),
                "Severity": dis_data.get("severity", ""),
                "Recovery": dis_data.get("recovery_days", ""),
            })
    import pandas as pd
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
