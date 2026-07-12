"""
Wayne AI Pharma - UI Components & Styling
"""
import streamlit as st
from config import (
    APP_NAME, APP_ICON, PRIMARY_COLOR, PRIMARY_LIGHT, PRIMARY_DARK,
    SUCCESS_COLOR, WARNING_COLOR, DANGER_COLOR
)


def inject_css():
    """Inject global CSS for styling."""
    st.markdown(f"""
    <style>
    /* ---- Global ---- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background-color: #ffffff;
    }}

    /* ---- Header / Brand ---- */
    .brand-header {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}, {PRIMARY_DARK});
        color: white;
        padding: 24px 32px;
        border-radius: 16px;
        margin-bottom: 28px;
        text-align: center;
    }}
    .brand-header h1 {{
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }}
    .brand-header p {{
        font-size: 1.05rem;
        margin: 6px 0 0 0;
        opacity: 0.9;
    }}

    /* ---- Cards ---- */
    .card {{
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s;
    }}
    .card:hover {{
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    }}

    /* ---- Metric Card ---- */
    .metric-card {{
        background: linear-gradient(135deg, #f0f5ff, #f8faff);
        border: 1.5px solid #dbe4ff;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }}
    .metric-card .metric-value {{
        font-size: 2.8rem;
        font-weight: 800;
        color: {SUCCESS_COLOR};
        line-height: 1.1;
    }}
    .metric-card .metric-label {{
        font-size: 0.95rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .metric-card .mckinsey-compare {{
        font-size: 0.82rem;
        color: #9ca3af;
        font-style: italic;
        margin-top: 4px;
    }}

    /* ---- Risk Item ---- */
    .risk-item {{
        background: #fef2f2;
        border-left: 4px solid {DANGER_COLOR};
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin-bottom: 12px;
    }}
    .risk-item .risk-title {{
        color: #dc2626;
        font-weight: 700;
        font-size: 0.95rem;
    }}
    .risk-item .risk-mitigation {{
        color: {SUCCESS_COLOR};
        font-size: 0.88rem;
        margin-top: 4px;
    }}

    /* ---- Confidence bar ---- */
    .confidence-bar {{
        background: #e5e7eb;
        border-radius: 20px;
        height: 10px;
        margin: 8px 0 4px 0;
        overflow: hidden;
    }}
    .confidence-fill {{
        background: linear-gradient(90deg, {SUCCESS_COLOR}, #34d399);
        height: 100%;
        border-radius: 20px;
        transition: width 1s ease;
    }}

    /* ---- Compliance Score ---- */
    .compliance-score {{
        display: inline-block;
        background: #f0fdf4;
        border: 2px solid #86efac;
        border-radius: 12px;
        padding: 10px 16px;
        margin: 4px;
        text-align: center;
    }}
    .compliance-score .score-num {{
        font-size: 1.5rem;
        font-weight: 800;
        color: {SUCCESS_COLOR};
    }}
    .compliance-score .score-label {{
        font-size: 0.75rem;
        color: #6b7280;
        text-transform: uppercase;
    }}

    /* ---- Recap Item ---- */
    .recap-item {{
        background: #f9fafb;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }}

    /* ---- Disclaimer ---- */
    .disclaimer-box {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 0.78rem;
        color: #94a3b8;
        text-align: center;
        margin-top: 30px;
    }}

    /* ---- Buttons ---- */
    .stButton > button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}, {PRIMARY_DARK});
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35);
        background: linear-gradient(135deg, {PRIMARY_LIGHT}, {PRIMARY_COLOR});
    }}
    .stButton > button:active {{
        transform: translateY(0);
    }}

    /* Secondary button */
    .btn-secondary > button {{
        background: white;
        color: {PRIMARY_COLOR};
        border: 2px solid {PRIMARY_COLOR};
        box-shadow: none;
    }}
    .btn-secondary > button:hover {{
        background: #f0f5ff;
        box-shadow: 0 2px 12px rgba(37, 99, 235, 0.15);
    }}

    /* Danger button */
    .btn-danger > button {{
        background: white;
        color: {DANGER_COLOR};
        border: 2px solid {DANGER_COLOR};
        box-shadow: none;
    }}
    .btn-danger > button:hover {{
        background: #fef2f2;
        box-shadow: 0 2px 12px rgba(239, 68, 68, 0.2);
    }}

    /* ---- File Uploader ---- */
    [data-testid="stFileUploader"] {{
        border: 2px dashed #cbd5e1;
        border-radius: 14px;
        padding: 20px;
    }}

    /* ---- Expander ---- */
    [data-testid="stExpander"] {{
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        box-shadow: none;
    }}

    /* ---- Mobile responsiveness ---- */
    @media (max-width: 768px) {{
        .brand-header h1 {{
            font-size: 1.6rem;
        }}
        .brand-header p {{
            font-size: 0.9rem;
        }}
        .metric-card .metric-value {{
            font-size: 2rem;
        }}
        .compliance-score {{
            display: block;
            margin: 6px 0;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)


def show_brand_header(subtitle: str = None):
    """Display the Wayne AI Pharma brand header."""
    st.markdown(f"""
    <div class="brand-header">
        <h1>{APP_ICON} {APP_NAME}</h1>
        <p>{subtitle or 'Clinical trials 10x faster. 20x cheaper. Built for Africa.'}</p>
    </div>
    """, unsafe_allow_html=True)


def show_disclaimer():
    """Display the standard disclaimer."""
    st.markdown("""
    <div class="disclaimer-box">
        🔒 All data encrypted at rest. We do NOT train AI on your data.
        HIPAA / PPB / NAFDAC / SAHPRA aligned. Data stays yours.
    </div>
    """, unsafe_allow_html=True)


def show_confidence_bar(confidence: float):
    color = SUCCESS_COLOR if confidence >= 70 else (WARNING_COLOR if confidence >= 40 else DANGER_COLOR)
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin:8px 0;">
        <span style="font-weight:700;color:#374151;">Confidence</span>
        <div class="confidence-bar" style="flex:1;">
            <div class="confidence-fill" style="width:{confidence}%;background:{color};"></div>
        </div>
        <span style="font-weight:800;color:{color};">{confidence}%</span>
    </div>
    """, unsafe_allow_html=True)


def metric_comparison(value: str, label: str, mckinsey: str):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="mckinsey-compare">vs McKinsey Average: {mckinsey}</div>
    </div>
    """, unsafe_allow_html=True)
