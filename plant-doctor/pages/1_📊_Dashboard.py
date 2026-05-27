"""Analytics Dashboard — scan history, disease trends, crop health stats."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import inject_css
from utils.history import load_history, clear_history

st.set_page_config(page_title="Analytics · Thiru Mkulima AI", page_icon="📊", layout="wide")
inject_css()

# Sidebar
with st.sidebar:
    st.markdown("### 🌿 Thiru Mkulima AI")
    st.divider()
    st.page_link("app.py",                       label="🔬 Detect Disease")
    st.page_link("pages/1_📊_Dashboard.py",       label="📊 Analytics")
    st.page_link("pages/2_🤖_AI_Assistant.py",    label="🤖 AI Assistant")
    st.page_link("pages/3_📚_Disease_Library.py", label="📚 Disease Library")

st.markdown("""
<div class="app-header" style="text-align:left">
    <div class="app-title" style="font-size:2rem">📊 Analytics Dashboard</div>
    <div class="app-subtitle">Scan history · Disease trends · Crop health insights</div>
</div>
""", unsafe_allow_html=True)

history = load_history()
if not history:
    st.markdown("""
    <div class="glass-card" style="text-align:center;padding:3rem">
        <div style="font-size:3rem">📊</div>
        <div style="color:#e6edf3;font-weight:600;margin-top:0.8rem">No scan data yet</div>
        <div style="color:#6e7681;font-size:0.88rem;margin-top:0.4rem">
            Run your first crop analysis on the <strong>🔬 Detect Disease</strong> page
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.DataFrame(history)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour

total       = len(df)
healthy_ct  = int(df["is_healthy"].sum())
disease_ct  = total - healthy_ct
health_rate = healthy_ct / total * 100
avg_conf    = df["confidence"].mean()

# ── KPI cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
for col, val, label in [
    (k1, total,                   "Total Scans"),
    (k2, f"{health_rate:.0f}%",   "Healthy Rate"),
    (k3, disease_ct,              "Disease Cases"),
    (k4, f"{avg_conf:.1f}%",      "Avg Confidence"),
]:
    col.markdown(
        f'<div class="stat-card"><div class="stat-value">{val}</div>'
        f'<div class="stat-label">{label}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Daily trend + health pie ───────────────────────────────────────────────────
c1, c2 = st.columns([3, 2], gap="large")

with c1:
    st.markdown('<div class="section-title">📅 Daily Scan Activity</div>', unsafe_allow_html=True)
    daily = df.groupby("date").size().reset_index(name="Scans")
    fig = px.area(
        daily, x="date", y="Scans",
        color_discrete_sequence=["#22c55e"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=8, b=0), height=230,
        font=dict(color="#8b949e"),
        xaxis=dict(showgrid=False, color="#6e7681"),
        yaxis=dict(gridcolor="#21262d", color="#6e7681"),
    )
    fig.update_traces(fillcolor="rgba(34,197,94,0.12)", line_color="#22c55e")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown('<div class="section-title">🏥 Health Overview</div>', unsafe_allow_html=True)
    fig2 = go.Figure(go.Pie(
        labels=["Healthy", "Disease"],
        values=[healthy_ct, disease_ct],
        hole=0.55,
        marker_colors=["#22c55e", "#f97316"],
        textinfo="label+percent",
        textfont_color="#e6edf3",
    ))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=8, b=0), height=230,
        font=dict(color="#8b949e"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, font_color="#8b949e"),
        showlegend=True,
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Top diseases + crop breakdown ──────────────────────────────────────────────
c3, c4 = st.columns([1, 1], gap="large")

with c3:
    st.markdown('<div class="section-title">🦠 Top Diseases Detected</div>', unsafe_allow_html=True)
    diseased = df[~df["is_healthy"]]
    if not diseased.empty:
        td = diseased["disease"].value_counts().head(10).reset_index()
        td.columns = ["Disease", "Count"]
        fig3 = px.bar(
            td, x="Count", y="Disease", orientation="h",
            color="Count", color_continuous_scale=["#1a4731", "#22c55e"],
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=8, b=0), height=280,
            font=dict(color="#8b949e"), coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending", color="#8b949e", showgrid=False),
            xaxis=dict(gridcolor="#21262d", color="#6e7681"),
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No disease cases yet — all scans healthy!")

with c4:
    st.markdown('<div class="section-title">🌾 Scans by Crop</div>', unsafe_allow_html=True)
    if "crop" in df.columns and df["crop"].notna().any():
        cc = df["crop"].value_counts().reset_index()
        cc.columns = ["Crop", "Scans"]
        fig4 = px.bar(
            cc, x="Crop", y="Scans",
            color="Scans", color_continuous_scale=["#1a4731", "#22c55e"],
        )
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=8, b=0), height=280,
            font=dict(color="#8b949e"), coloraxis_showscale=False,
            xaxis=dict(showgrid=False, color="#8b949e", tickangle=-30),
            yaxis=dict(gridcolor="#21262d", color="#6e7681"),
        )
        st.plotly_chart(fig4, use_container_width=True)

# ── Confidence histogram ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">📐 Confidence Distribution</div>', unsafe_allow_html=True)
fig5 = px.histogram(
    df, x="confidence", nbins=20,
    color_discrete_sequence=["#22c55e"],
    labels={"confidence": "Confidence (%)"},
)
fig5.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=8, b=0), height=180,
    font=dict(color="#8b949e"), bargap=0.06,
    xaxis=dict(showgrid=False, color="#6e7681"),
    yaxis=dict(gridcolor="#21262d", color="#6e7681"),
)
st.plotly_chart(fig5, use_container_width=True)

# ── History table ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Scan Log</div>', unsafe_allow_html=True)
disp = df[["timestamp", "crop", "disease", "confidence", "is_healthy"]].copy()
disp.columns = ["Timestamp", "Crop", "Disease", "Confidence (%)", "Status"]
disp["Timestamp"] = disp["Timestamp"].dt.strftime("%Y-%m-%d %H:%M")
disp["Status"]    = disp["Status"].map({True: "✅ Healthy", False: "🦠 Disease"})
st.dataframe(
    disp.sort_values("Timestamp", ascending=False).head(100),
    use_container_width=True, hide_index=True,
)

st.divider()
if st.button("🗑️ Clear All History", type="secondary"):
    clear_history()
    st.success("History cleared.")
    st.rerun()
