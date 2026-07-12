"""
Wayne AI Pharma - Past Analyses / History Page
"""
import json
import streamlit as st
from auth import require_auth, logout_user
from database import get_user_analyses, get_analysis, get_analysis_pdf, log_audit
from config import (
    MCKINSEY_AVG_TIMELINE_MONTHS, MCKINSEY_AVG_COST_MILLIONS
)
from ui_components import (
    show_brand_header, show_disclaimer, inject_css,
    show_confidence_bar, metric_comparison
)


def render_history():
    inject_css()
    require_auth()

    user_id = st.session_state.user_id
    user_email = st.session_state.user_email

    # ---- Sidebar ----
    with st.sidebar:
        st.markdown("### 🧬 Wayne AI Pharma")
        st.markdown(f"👤 **{user_email}**")
        st.divider()
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        if st.button("🔬 New Trial Analysis", use_container_width=True):
            st.session_state.page = "analyzer"
            st.rerun()
        if st.button("⚙️ Account Settings", use_container_width=True):
            st.session_state.page = "settings"
            st.rerun()
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            log_audit(user_id, "LOGOUT", f"User {user_email} logged out")
            logout_user()
            st.rerun()

    # ---- Main ----
    show_brand_header("Past Analyses")

    analyses = get_user_analyses(user_id)

    if not analyses:
        st.info("📭 No analyses yet. Go to **New Trial Analysis** to get started!")
        if st.button("🔬 Analyze My First Trial", use_container_width=True):
            st.session_state.page = "analyzer"
            st.rerun()
        show_disclaimer()
        return

    st.markdown(f"### 📊 {len(analyses)} Analysis Results")

    # Show a specific analysis if requested
    if st.session_state.get("current_analysis_id"):
        analysis = get_analysis(st.session_state.current_analysis_id, user_id)
        if analysis:
            _render_single_analysis(analysis)
            if st.button("← Back to All Analyses", key="back_to_list"):
                st.session_state.current_analysis_id = None
                st.rerun()
        else:
            st.error("Analysis not found.")
            st.session_state.current_analysis_id = None
        show_disclaimer()
        return

    # Show list of analyses
    for a in analyses:
        with st.expander(f"📄 {a['original_filename']} — {a['created_at'][:10]} — Confidence: {a['confidence']:.0f}% | {a['timeline']} | {a['cost']}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 View Full Report", key=f"view_{a['id']}", use_container_width=True):
                    st.session_state.current_analysis_id = a["id"]
                    st.rerun()
            with col2:
                pdf = get_analysis_pdf(a["id"], user_id)
                if pdf:
                    fn = a["original_filename"].rsplit(".", 1)[0]
                    st.download_button(
                        "📥 Download PDF",
                        data=pdf,
                        file_name=f"Wayne_Pharma_Report_{fn}.pdf",
                        mime="application/pdf",
                        key=f"dl_{a['id']}",
                        use_container_width=True
                    )

    show_disclaimer()


def _render_single_analysis(analysis_row):
    """Render a single past analysis in detail."""
    try:
        analysis = json.loads(analysis_row["analysis_json"])
    except (json.JSONDecodeError, TypeError):
        st.error("Could not parse analysis data.")
        return

    st.markdown(f"**Source:** {analysis_row.get('original_filename', 'Unknown')}")
    st.markdown(f"**Analyzed:** {analysis_row['created_at']}")
    show_confidence_bar(float(analysis.get("confidence", 85)))

    st.markdown("---")

    # 1. Timeline
    metric_comparison(
        analysis.get("timeline", "N/A"),
        "Predicted Timeline",
        f"{MCKINSEY_AVG_TIMELINE_MONTHS} months (McKinsey Avg)"
    )

    # 2. Cost
    metric_comparison(
        analysis.get("cost", "N/A"),
        "Predicted Cost",
        f"${MCKINSEY_AVG_COST_MILLIONS}M (McKinsey Avg)"
    )

    # 3. Risks
    st.markdown("### ⚠️ Top Risks in Africa")
    risks = analysis.get("risks", [])
    for i, risk_item in enumerate(risks[:5], 1):
        if isinstance(risk_item, dict):
            risk_text = risk_item.get("risk", "")
            mitigation = risk_item.get("mitigation", "")
        else:
            risk_text = str(risk_item)
            mitigation = "See analysis"
        st.markdown(f"""
        <div class="risk-item">
            <div class="risk-title">🔴 {risk_text}</div>
            <div class="risk-mitigation">✅ {mitigation}</div>
        </div>
        """, unsafe_allow_html=True)

    # 4. Compliance
    st.markdown("### 📋 Regulatory Compliance")
    compliance = analysis.get("compliance", {})
    scores = [
        ("PPB Kenya", compliance.get("kenya_score", "N/A")),
        ("NAFDAC Nigeria", compliance.get("nigeria_score", "N/A")),
        ("SAHPRA South Africa", compliance.get("sa_score", "N/A")),
        ("EDA Egypt", compliance.get("egypt_score", "N/A")),
    ]
    cols = st.columns(4)
    for i, (name, score) in enumerate(scores):
        with cols[i]:
            st.markdown(f"""
            <div class="compliance-score">
                <div class="score-label">{name}</div>
                <div class="score-num">{score}/100</div>
            </div>
            """, unsafe_allow_html=True)

    # 5. Recruitment
    st.markdown("### 🏥 Patient Recruitment")
    recruitment = analysis.get("recruitment", {})
    if recruitment:
        for country, rate in recruitment.items():
            st.markdown(f"- **{country.replace('_', ' ').title()}**: {rate}")

    # 6. Advantage
    st.markdown("### 🚀 Why This Beats McKinsey")
    st.markdown(f"""
    <div class="card" style="background:#f0f9ff;border-color:#bae6fd;">
        {analysis.get("advantage", "N/A")}
    </div>
    """, unsafe_allow_html=True)

    # Download PDF
    pdf = get_analysis_pdf(analysis_row["id"], st.session_state.user_id)
    if pdf:
        st.download_button(
            "📥 Download Encrypted PDF Report",
            data=pdf,
            file_name=f"Wayne_Pharma_Report_{analysis_row.get('original_filename', 'report')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
