import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        /* ── Global ──────────────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* ── Hero banner ─────────────────────────────────────────────── */
        .hero-banner {
            background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%);
            border-radius: 16px;
            padding: 2.5rem 2rem;
            margin-bottom: 1.5rem;
            color: #fff;
            text-align: center;
            box-shadow: 0 8px 32px rgba(46,125,50,0.35);
        }
        .hero-banner h1 {
            font-size: 2.4rem;
            font-weight: 700;
            margin: 0 0 0.4rem;
            letter-spacing: -0.5px;
        }
        .hero-banner p {
            font-size: 1.05rem;
            opacity: 0.9;
            margin: 0;
        }

        /* ── Glass card ──────────────────────────────────────────────── */
        .glass-card {
            background: rgba(255,255,255,0.75);
            border: 1px solid rgba(46,125,50,0.2);
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(46,125,50,0.08);
            backdrop-filter: blur(8px);
        }

        /* ── Stat card ───────────────────────────────────────────────── */
        .stat-card {
            background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
            border: 1px solid #a5d6a7;
            border-radius: 14px;
            padding: 1.2rem 1rem;
            text-align: center;
            box-shadow: 0 2px 12px rgba(46,125,50,0.1);
        }
        .stat-card .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2e7d32;
            line-height: 1.1;
        }
        .stat-card .stat-label {
            font-size: 0.82rem;
            color: #558b2f;
            margin-top: 4px;
            font-weight: 500;
        }

        /* ── Feature card ────────────────────────────────────────────── */
        .feature-card {
            background: #fff;
            border: 1px solid #c8e6c9;
            border-radius: 14px;
            padding: 1.4rem;
            text-align: center;
            transition: box-shadow 0.2s;
            height: 100%;
        }
        .feature-card:hover { box-shadow: 0 6px 24px rgba(46,125,50,0.18); }
        .feature-card .feat-icon { font-size: 2.2rem; }
        .feature-card h4 { color: #1b5e20; margin: 0.5rem 0 0.3rem; font-size: 1rem; font-weight: 600; }
        .feature-card p  { color: #555; font-size: 0.85rem; margin: 0; }

        /* ── Disease result ──────────────────────────────────────────── */
        .result-healthy {
            background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
            border: 2px solid #4caf50;
            border-radius: 14px;
            padding: 1.5rem;
            text-align: center;
        }
        .result-disease {
            background: linear-gradient(135deg, #fff3e0, #ffe0b2);
            border: 2px solid #ff9800;
            border-radius: 14px;
            padding: 1.5rem;
            text-align: center;
        }
        .result-label {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0.3rem 0;
        }
        .result-conf {
            font-size: 0.9rem;
            opacity: 0.8;
        }

        /* ── Chat bubbles ────────────────────────────────────────────── */
        .chat-user {
            background: #e3f2fd;
            border-radius: 16px 16px 4px 16px;
            padding: 0.8rem 1rem;
            margin: 0.5rem 0 0.5rem 3rem;
            font-size: 0.92rem;
            color: #1a237e;
        }
        .chat-bot {
            background: #e8f5e9;
            border-radius: 16px 16px 16px 4px;
            padding: 0.8rem 1rem;
            margin: 0.5rem 3rem 0.5rem 0;
            font-size: 0.92rem;
            color: #1b5e20;
            border-left: 3px solid #4caf50;
        }

        /* ── Section header ──────────────────────────────────────────── */
        .section-header {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1b5e20;
            border-bottom: 3px solid #4caf50;
            padding-bottom: 6px;
            margin-bottom: 1rem;
        }

        /* ── Badge ───────────────────────────────────────────────────── */
        .badge-healthy { background:#c8e6c9; color:#1b5e20; border-radius:20px; padding:3px 12px; font-size:0.8rem; font-weight:600; }
        .badge-disease { background:#ffe0b2; color:#e65100; border-radius:20px; padding:3px 12px; font-size:0.8rem; font-weight:600; }

        /* ── Scan animation ──────────────────────────────────────────── */
        @keyframes scan {
            0%   { top: 0; opacity: 0.8; }
            50%  { opacity: 1; }
            100% { top: calc(100% - 4px); opacity: 0.8; }
        }
        .scan-wrapper {
            position: relative;
            overflow: hidden;
            border-radius: 10px;
        }
        .scan-line {
            position: absolute;
            left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, transparent, #4caf50, transparent);
            animation: scan 2s linear infinite;
        }

        /* ── Sidebar tweaks ──────────────────────────────────────────── */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #e8f5e9 0%, #f9fbe7 100%);
        }

        /* ── Responsive: mobile ──────────────────────────────────────── */
        @media (max-width: 640px) {
            .hero-banner h1 { font-size: 1.6rem; }
            .stat-card .stat-value { font-size: 1.5rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
