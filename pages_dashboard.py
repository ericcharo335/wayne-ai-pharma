"""
Wayne AI Pharma - Main Dashboard Page
"""
import streamlit as st
from auth import require_auth, logout_user
from database import get_user_analyses, run_auto_delete, log_audit
from ui_components import show_brand_header, show_disclaimer, inject_css


def render_dashboard():
    inject_css()
    require_auth()

    # Run auto-delete check
    run_auto_delete()

    user_email = st.session_state.user_email
    user_id = st.session_state.user_id

    # ---- Sidebar ----
    with st.sidebar:
        st.markdown("### 🧬 Wayne AI Pharma")
        st.markdown(f"👤 **{user_email}**")
        st.divider()

        if st.button("🏠 Dashboard", use_container_width=True, key="nav_dash"):
            st.session_state.page = "dashboard"
            st.rerun()

        if st.button("🔬 New Trial Analysis", use_container_width=True, key="nav_new"):
            st.session_state.page = "analyzer"
            st.rerun()

        if st.button("📋 My Past Analyses", use_container_width=True, key="nav_past"):
            st.session_state.page = "history"
            st.rerun()

        if st.button("⚙️ Account Settings", use_container_width=True, key="nav_settings"):
            st.session_state.page = "settings"
            st.rerun()

        st.divider()
        if st.button("🚪 Logout", use_container_width=True, key="nav_logout"):
            log_audit(user_id, "LOGOUT", f"User {user_email} logged out")
            logout_user()
            st.rerun()

    # ---- Main Content ----
    show_brand_header()

    # Welcome
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:30px;">
        <h2 style="color:#111827;font-weight:700;">Welcome back, {user_email.split('@')[0].title()} 👋</h2>
        <p style="color:#6b7280;font-size:1.05rem;">
            Your AI-powered clinical trial command center for Africa.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Stats
    analyses = get_user_analyses(user_id)
    num_analyses = len(analyses)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:#2563eb;">{num_analyses}</div>
            <div style="color:#6b7280;font-size:0.9rem;">Total Analyses</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        avg_conf = 0
        if analyses:
            avg_conf = sum(a["confidence"] or 0 for a in analyses) / len(analyses)
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:#10b981;">{avg_conf:.0f}%</div>
            <div style="color:#6b7280;font-size:0.9rem;">Avg Confidence</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:#f59e0b;">
                {'🔒' if num_analyses > 0 else '—'}
            </div>
            <div style="color:#6b7280;font-size:0.9rem;">Data Encrypted</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Action Buttons
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        if st.button("🔬 New Trial Analysis", use_container_width=True, key="dash_new"):
            st.session_state.page = "analyzer"
            st.rerun()

    with col_b:
        if st.button("📋 My Past Analyses", use_container_width=True, key="dash_past"):
            st.session_state.page = "history"
            st.rerun()

    with col_c:
        if st.button("⚙️ Account Settings", use_container_width=True, key="dash_settings"):
            st.session_state.page = "settings"
            st.rerun()

    # Recent Analyses Preview
    if analyses:
        st.markdown("---")
        st.markdown("### 📊 Recent Analyses")
        for a in analyses[:5]:
            with st.expander(f"📄 {a['original_filename']} — {a['created_at'][:10]} — Confidence: {a['confidence']:.0f}%"):
                st.markdown(f"""
                - **Timeline:** {a['timeline']}
                - **Cost:** {a['cost']}
                """)
                if st.button("📋 View Full Report", key=f"view_{a['id']}"):
                    st.session_state.current_analysis_id = a['id']
                    st.session_state.page = "history"
                    st.rerun()

    show_disclaimer()
