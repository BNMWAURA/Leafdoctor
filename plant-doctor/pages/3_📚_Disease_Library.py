"""Disease Library — encyclopaedia for all 13 crops and their diseases."""
import streamlit as st
import pandas as pd
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import inject_css
from utils.disease_db import DISEASE_DB, SEVERITY_CLASS, SEVERITY_COLOR_HEX, SEVERITY_BAR_PCT

st.set_page_config(page_title="Disease Library · Thiru Mkulima AI", page_icon="📚", layout="wide")
inject_css()

with st.sidebar:
    st.markdown("### 🌿 Thiru Mkulima AI")
    st.divider()
    st.page_link("app.py",                       label="🔬 Detect Disease")
    st.page_link("pages/1_📊_Dashboard.py",       label="📊 Analytics")
    st.page_link("pages/2_🤖_AI_Assistant.py",    label="🤖 AI Assistant")
    st.page_link("pages/3_📚_Disease_Library.py", label="📚 Disease Library")

st.markdown("""
<div class="app-header" style="text-align:left">
    <div class="app-title" style="font-size:2rem">📚 Disease Library</div>
    <div class="app-subtitle">Complete encyclopaedia · 13 crops · 30+ disease classes</div>
</div>
""", unsafe_allow_html=True)

# ── Filters ───────────────────────────────────────────────────────────────────
fc, sc, tc = st.columns([2, 2, 3])
selected_crop = fc.selectbox(
    "Crop", ["All Crops"] + list(DISEASE_DB.keys()),
)
selected_sev = sc.selectbox(
    "Severity",
    ["All", "Very High", "High", "Medium-High", "Medium", "Low-Medium", "Low", "None"],
)
search = tc.text_input("🔍 Search", placeholder="e.g. rust, blight, mosaic, fungus…")

st.markdown("<br>", unsafe_allow_html=True)

# ── Render ────────────────────────────────────────────────────────────────────
any_shown = False

for crop_name, crop_data in DISEASE_DB.items():
    if selected_crop != "All Crops" and crop_name != selected_crop:
        continue

    to_show = {}
    for dname, ddata in crop_data["diseases"].items():
        if dname == "Healthy":
            continue
        if selected_sev != "All" and ddata.get("severity") != selected_sev:
            continue
        if search:
            hay = (dname + " " + ddata.get("pathogen", "") + " " +
                   " ".join(ddata.get("symptoms", [])) + " " + crop_name).lower()
            if search.lower() not in hay:
                continue
        to_show[dname] = ddata

    if not to_show:
        continue

    any_shown = True
    st.markdown(
        f'<div class="section-title">{crop_data["icon"]} {crop_name}</div>',
        unsafe_allow_html=True,
    )

    for dname, ddata in to_show.items():
        sev      = ddata.get("severity", "Unknown")
        sev_cls  = SEVERITY_CLASS.get(sev, "sev-low")
        sev_col  = SEVERITY_COLOR_HEX.get(sev, "#6e7681")
        sev_pct  = SEVERITY_BAR_PCT.get(sev, 0)
        pathogen = ddata.get("pathogen", "Unknown")

        header_html = (
            f'<div class="disease-header">'
            f'<span>{dname}</span>'
            f'<span class="sev-pill {sev_cls}">{sev}</span>'
            f'<span style="color:#6e7681;font-size:0.78rem;font-weight:400">{pathogen}</span>'
            f'</div>'
        )

        with st.expander(dname, expanded=False):
            st.markdown(f'<div style="margin-bottom:0.8rem">{header_html}</div>',
                        unsafe_allow_html=True)

            # Severity bar
            st.markdown(
                f'<div class="conf-bar-track" style="margin-bottom:1rem">'
                f'<div class="conf-bar-fill" style="width:{sev_pct}%;background:{sev_col}"></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            d1, d2, d3 = st.columns(3)

            with d1:
                st.markdown("**🩺 Symptoms**")
                for s in ddata.get("symptoms", []):
                    st.markdown(f"- {s}")
                st.markdown(f"**⏱️ Recovery:** {ddata.get('recovery', 'N/A')}")

            with d2:
                st.markdown("**💊 Treatment**")
                for t in ddata.get("treatment", []):
                    st.markdown(f"- {t}")

            with d3:
                st.markdown("**🛡️ Prevention**")
                for p in ddata.get("prevention", []):
                    st.markdown(f"- {p}")

    st.markdown("<br>", unsafe_allow_html=True)

if not any_shown:
    st.markdown("""
    <div class="glass-card" style="text-align:center;padding:2rem">
        <div style="font-size:2rem">🔍</div>
        <div style="color:#e6edf3;margin-top:0.5rem">No results match your filters</div>
        <div style="color:#6e7681;font-size:0.85rem">Try broadening the search or changing the severity filter</div>
    </div>
    """, unsafe_allow_html=True)

# ── Summary table ──────────────────────────────────────────────────────────────
with st.expander("📋 Full Disease Index Table", expanded=False):
    rows = []
    for cn, cd in DISEASE_DB.items():
        for dn, dd in cd["diseases"].items():
            if dn == "Healthy":
                continue
            rows.append({
                "Crop": cn,
                "Disease": dn,
                "Pathogen": dd.get("pathogen", ""),
                "Severity": dd.get("severity", ""),
                "Recovery": dd.get("recovery", ""),
            })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
