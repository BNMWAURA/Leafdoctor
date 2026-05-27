import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import inject_css
from utils.history import load_history, clear_history

st.set_page_config(page_title="Analytics · AI Crop Doctor", page_icon="📊", layout="wide")
inject_css()

st.markdown(
    '<div class="hero-banner" style="padding:1.5rem 2rem;">'
    '<h1 style="font-size:1.8rem">📊 Farm Analytics Dashboard</h1>'
    '<p>Track disease trends, scan history, and crop health insights</p>'
    '</div>',
    unsafe_allow_html=True,
)

history = load_history()

if not history:
    st.info(
        "No scan history yet. Run your first crop analysis on the **🔬 Crop Doctor** page!",
        icon="📈",
    )
    st.stop()

df = pd.DataFrame(history)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"]      = df["timestamp"].dt.date
df["hour"]      = df["timestamp"].dt.hour

# ── KPI row ───────────────────────────────────────────────────────────────────
total       = len(df)
healthy_ct  = df["is_healthy"].sum()
disease_ct  = total - healthy_ct
health_rate = healthy_ct / total * 100
avg_conf    = df["confidence"].mean()

k1, k2, k3, k4 = st.columns(4)
for col, val, label in [
    (k1, total,                    "Total Scans"),
    (k2, f"{health_rate:.0f}%",    "Healthy Rate"),
    (k3, disease_ct,               "Disease Cases"),
    (k4, f"{avg_conf:.1f}%",       "Avg Confidence"),
]:
    col.markdown(
        f"""<div class="stat-card">
            <div class="stat-value">{val}</div>
            <div class="stat-label">{label}</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Scan trend + Healthy vs Disease pie ────────────────────────────────
col_line, col_pie = st.columns([2, 1], gap="large")

with col_line:
    st.markdown('<div class="section-header">📅 Daily Scan Activity</div>', unsafe_allow_html=True)
    daily = df.groupby("date").size().reset_index(name="scans")
    fig_line = px.area(
        daily, x="date", y="scans",
        color_discrete_sequence=["#4caf50"],
        labels={"date": "Date", "scans": "Scans"},
    )
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0), height=250,
    )
    fig_line.update_xaxes(showgrid=False)
    fig_line.update_yaxes(gridcolor="#e8f5e9")
    st.plotly_chart(fig_line, use_container_width=True)

with col_pie:
    st.markdown('<div class="section-header">🏥 Health Overview</div>', unsafe_allow_html=True)
    pie_df = pd.DataFrame({
        "Status": ["Healthy", "Disease Detected"],
        "Count":  [int(healthy_ct), int(disease_ct)],
    })
    fig_pie = px.pie(
        pie_df, names="Status", values="Count",
        color_discrete_sequence=["#4caf50", "#ff9800"],
        hole=0.45,
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0), height=250,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 2: Top diseases + Crop breakdown ─────────────────────────────────────
col_bar, col_crop = st.columns([1, 1], gap="large")

with col_bar:
    st.markdown('<div class="section-header">🦠 Top Detected Diseases</div>', unsafe_allow_html=True)
    diseased = df[~df["is_healthy"]]
    if not diseased.empty:
        top_dis = diseased["disease"].value_counts().head(10).reset_index()
        top_dis.columns = ["Disease", "Count"]
        fig_bar = px.bar(
            top_dis, x="Count", y="Disease", orientation="h",
            color="Count",
            color_continuous_scale=["#a5d6a7", "#2e7d32"],
            labels={"Count": "Cases", "Disease": ""},
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), height=300,
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending"),
        )
        fig_bar.update_xaxes(gridcolor="#e8f5e9")
        fig_bar.update_yaxes(showgrid=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No disease cases recorded yet.")

with col_crop:
    st.markdown('<div class="section-header">🌾 Scans by Crop</div>', unsafe_allow_html=True)
    if "crop" in df.columns:
        crop_counts = df["crop"].value_counts().reset_index()
        crop_counts.columns = ["Crop", "Scans"]
        fig_crop = px.bar(
            crop_counts, x="Crop", y="Scans",
            color="Scans",
            color_continuous_scale=["#c8e6c9", "#1b5e20"],
        )
        fig_crop.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), height=300,
            coloraxis_showscale=False,
        )
        fig_crop.update_xaxes(showgrid=False, tickangle=-30)
        fig_crop.update_yaxes(gridcolor="#e8f5e9")
        st.plotly_chart(fig_crop, use_container_width=True)

# ── Confidence distribution ───────────────────────────────────────────────────
st.markdown('<div class="section-header">📐 Confidence Score Distribution</div>', unsafe_allow_html=True)
fig_hist = px.histogram(
    df, x="confidence", nbins=20,
    color_discrete_sequence=["#388e3c"],
    labels={"confidence": "Confidence (%)", "count": "Scans"},
)
fig_hist.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=10, b=0), height=200,
    bargap=0.05,
)
fig_hist.update_xaxes(showgrid=False)
fig_hist.update_yaxes(gridcolor="#e8f5e9")
st.plotly_chart(fig_hist, use_container_width=True)

# ── Scan log table ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📋 Scan History Log</div>', unsafe_allow_html=True)
display_df = df[["timestamp", "crop", "disease", "confidence", "is_healthy"]].copy()
display_df.columns = ["Timestamp", "Crop", "Disease", "Confidence (%)", "Healthy"]
display_df["Timestamp"] = display_df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M")
display_df["Healthy"]   = display_df["Healthy"].map({True: "✅", False: "🦠"})
st.dataframe(
    display_df.sort_values("Timestamp", ascending=False).head(50),
    use_container_width=True,
    hide_index=True,
)

# ── Clear history ─────────────────────────────────────────────────────────────
st.divider()
if st.button("🗑️ Clear All History", type="secondary"):
    clear_history()
    st.success("History cleared.")
    st.rerun()
