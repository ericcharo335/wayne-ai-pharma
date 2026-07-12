"""
Wayne AI Pharma - Trial Analyzer Page (Core Feature)
Upload PDF/DOCX → Extract → Redact → Claude Analysis → Results → PDF Report
"""
import io
import json
import streamlit as st
from auth import require_auth, logout_user
from database import (
    save_upload, save_analysis, get_analysis_pdf, log_audit,
    get_user_uploads
)
from document_processor import extract_text, redact_phi, get_text_preview
from claude_client import analyze_document
from pdf_report import get_pdf_bytes
from config import (
    MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB, SUPPORTED_TYPES,
    MCKINSEY_AVG_TIMELINE_MONTHS, MCKINSEY_AVG_COST_MILLIONS,
    REGULATORY_BODIES
)
from ui_components import (
    show_brand_header, show_disclaimer, inject_css,
    show_confidence_bar, metric_comparison
)


def render_analyzer():
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
        if st.button("📋 My Past Analyses", use_container_width=True):
            st.session_state.page = "history"
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
    show_brand_header("Trial Analyzer")

    st.markdown("""
    <div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:12px;padding:18px 24px;margin-bottom:24px;">
        <strong>📤 Upload</strong> your clinical trial protocol, investigator brochure, or trial design document (PDF or DOCX).
        <br>Wayne AI will analyze it against African regulatory frameworks and McKinsey benchmarks.
        <br><strong>🔒 All patient data is automatically redacted before analysis.</strong>
    </div>
    """, unsafe_allow_html=True)

    # ---- File Upload ----
    uploaded_file = st.file_uploader(
        "Upload Clinical Trial Document",
        type=SUPPORTED_TYPES,
        help=f"Supported: PDF, DOCX. Max size: {MAX_FILE_SIZE_MB}MB",
        key="file_uploader"
    )

    if uploaded_file is None:
        st.info("👆 Upload a PDF or DOCX file to begin analysis.")
        show_disclaimer()
        return

    # Validate file
    file_bytes = uploaded_file.read()
    file_size = len(file_bytes)
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type not in SUPPORTED_TYPES:
        st.error(f"Unsupported file type: .{file_type}. Please upload PDF or DOCX.")
        return

    if file_size > MAX_FILE_SIZE_BYTES:
        st.error(f"File too large ({file_size / 1024 / 1024:.1f}MB). Maximum: {MAX_FILE_SIZE_MB}MB.")
        return

    if file_size == 0:
        st.error("File is empty. Please upload a valid document.")
        return

    # Display file info
    st.markdown(f"""
    <div class="card">
        <strong>📄 {uploaded_file.name}</strong><br>
        <span style="color:#6b7280;">{file_size / 1024:.1f} KB  |  .{file_type.upper()}  |  Ready for analysis</span>
    </div>
    """, unsafe_allow_html=True)

    # ---- Process Step 1: Extract Text ----
    with st.spinner("🔍 Extracting text from document..."):
        try:
            extracted_text = extract_text(file_bytes, file_type)
        except Exception as e:
            st.error(f"Failed to extract text: {str(e)}")
            return

    if not extracted_text or len(extracted_text.strip()) < 10:
        st.error("Could not extract meaningful text from this document. The file may be scanned/image-based or empty.")
        return

    st.success(f"✅ Text extracted: {len(extracted_text):,} characters")

    with st.expander("👁️ Preview Extracted Text (first 500 chars)"):
        st.text(get_text_preview(extracted_text, 500))

    # ---- Process Step 2: Redact PHI ----
    with st.spinner("🛡️ Redacting protected health information..."):
        redacted_text, redaction_summary = redact_phi(extracted_text)

    st.success(f"🛡️ PHI Redacted: {redaction_summary['emails_redacted']} emails, "
               f"{redaction_summary['phones_redacted']} phones, "
               f"{redaction_summary['names_redacted']} names")

    # ---- Save Upload to DB ----
    try:
        upload_id = save_upload(user_id, uploaded_file.name, file_type, file_bytes)
        log_audit(user_id, "UPLOAD", f"Uploaded {uploaded_file.name} ({file_size} bytes)")
    except Exception as e:
        st.error(f"Failed to save file: {str(e)}")
        return

    # ---- Process Step 3: Analyze with Claude ----
    if st.button("🔬 Run AI Analysis", type="primary", use_container_width=True):
        with st.spinner("🤖 Wayne AI is analyzing your document... This may take 30-60 seconds."):
            try:
                analysis = analyze_document(redacted_text)
            except ValueError as e:
                if "API key" in str(e):
                    st.error(
                        "⚠️ Codex API key not configured.\n\n"
                        "Please add your API key to `.streamlit/secrets.toml`:\n"
                        '```toml\nCODEWX_API_KEY = "sk-cs4-..."\n```\n'
                        "Or set it in your Streamlit Cloud secrets."
                    )
                else:
                    st.error(f"Analysis error: {str(e)}")
                return
            except Exception as e:
                st.error(f"API error: {str(e)}")
                return

        # ---- Display Results ----
        st.balloons()
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")

        confidence = float(analysis.get("confidence", 85))
        show_confidence_bar(confidence)

        st.markdown("<br>", unsafe_allow_html=True)

        # 1. Timeline
        col_tl, col_blank = st.columns([1, 1])
        with col_tl:
            metric_comparison(
                analysis.get("timeline", "N/A"),
                "Predicted Timeline",
                f"{MCKINSEY_AVG_TIMELINE_MONTHS} months (McKinsey Avg)"
            )

        # 2. Cost
        col_cost, col_blank2 = st.columns([1, 1])
        with col_cost:
            metric_comparison(
                analysis.get("cost", "N/A"),
                "Predicted Cost",
                f"${MCKINSEY_AVG_COST_MILLIONS}M (McKinsey Avg)"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Top Risks
        st.markdown("### ⚠️ Top Risks in Africa & Mitigation")
        risks = analysis.get("risks", [])
        for i, risk_item in enumerate(risks[:5], 1):
            if isinstance(risk_item, dict):
                risk_text = risk_item.get("risk", "")
                mitigation = risk_item.get("mitigation", "")
            else:
                risk_text = str(risk_item)
                mitigation = "See full analysis"

            st.markdown(f"""
            <div class="risk-item">
                <div class="risk-title">🔴 Risk {i}: {risk_text}</div>
                <div class="risk-mitigation">✅ Mitigation: {mitigation}</div>
            </div>
            """, unsafe_allow_html=True)

        if not risks:
            st.info("No specific risks identified.")

        st.markdown("<br>", unsafe_allow_html=True)

        # 4. Compliance Scores
        st.markdown("### 📋 Regulatory Compliance Scores")
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

        # Compliance Checklist
        checklist = compliance.get("checklist", [])
        if checklist:
            with st.expander("📝 Compliance Checklist"):
                for item in checklist:
                    st.checkbox(item, value=False, key=f"checklist_{hash(item) % 100000}")

        st.markdown("<br>", unsafe_allow_html=True)

        # 5. Patient Recruitment
        st.markdown("### 🏥", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)  
        # 6. Why Beats McKinsey
        st.markdown("### 🚀 End", unsafe_allow_html=True)
    show_disclaimer()
