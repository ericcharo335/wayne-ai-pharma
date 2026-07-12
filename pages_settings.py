"""
Wayne AI Pharma - Account Settings Page
"""
import streamlit as st
from auth import require_auth, logout_user
from database import (
    get_user_by_id, update_user_settings, delete_user_data, log_audit,
    get_user_analyses, get_user_uploads
)
from ui_components import show_brand_header, show_disclaimer, inject_css


def render_settings():
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
        if st.button("📋 My Past Analyses", use_container_width=True):
            st.session_state.page = "history"
            st.rerun()
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            log_audit(user_id, "LOGOUT", f"User {user_email} logged out")
            logout_user()
            st.rerun()

    # ---- Main ----
    show_brand_header("Account Settings")

    user = get_user_by_id(user_id)
    if user is None:
        st.error("User not found.")
        return

    # ---- Profile Section ----
    st.markdown("### 👤 Profile")
    st.markdown(f"""
    <div class="card">
        <strong>Email:</strong> {user['email']}<br>
        <strong>Member since:</strong> {user['created_at'][:10]}<br>
        <strong>Account ID:</strong> #{user['id']}
    </div>
    """, unsafe_allow_html=True)

    # ---- Data Retention Settings ----
    st.markdown("---")
    st.markdown("### 🗂️ Data Retention")

    current_auto_delete = bool(user["auto_delete_enabled"])
    current_days = user["auto_delete_days"] or 90

    auto_delete = st.checkbox(
        "Auto-delete my data after retention period",
        value=current_auto_delete,
        help="When enabled, your uploads and analyses older than the retention period will be automatically deleted."
    )

    retention_days = st.slider(
        "Retention period (days)",
        min_value=7,
        max_value=365,
        value=current_days,
        step=1,
        help="Data older than this will be automatically deleted."
    )

    if auto_delete != current_auto_delete or retention_days != current_days:
        if st.button("💾 Save Retention Settings", use_container_width=True):
            update_user_settings(user_id, auto_delete, retention_days)
            log_audit(user_id, "SETTINGS_UPDATE",
                      f"Auto-delete: {auto_delete}, Days: {retention_days}")
            st.success("✅ Settings saved!")
            st.rerun()

    # Display retention info
    if auto_delete:
        st.info(f"🕐 Your data will be automatically deleted after {retention_days} days.")
    else:
        st.info("🕐 Auto-delete is currently disabled. Your data will be kept indefinitely.")

    # ---- Data Stats ----
    st.markdown("---")
    st.markdown("### 📊 Your Data")

    analyses = get_user_analyses(user_id)
    uploads = get_user_uploads(user_id)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:2rem;font-weight:800;color:#2563eb;">{len(analyses)}</div>
            <div style="color:#6b7280;">Total Analyses</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:2rem;font-weight:800;color:#2563eb;">{len(uploads)}</div>
            <div style="color:#6b7280;">Total Uploads</div>
        </div>
        """, unsafe_allow_html=True)

    # ---- Delete My Data ----
    st.markdown("---")
    st.markdown("### ⚠️ Danger Zone")

    st.markdown("""
    <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:12px;padding:20px;margin-bottom:16px;">
        <strong style="color:#dc2626;">Delete All My Data</strong>
        <p style="color:#7f1d1d;margin-top:8px;">
            This will permanently delete all your uploads and analysis results.
            This action cannot be undone.
        </p>
    </div>
    """, unsafe_allow_html=True)

    confirm_delete = st.text_input(
        "Type 'DELETE' to confirm:",
        placeholder="DELETE",
        key="confirm_delete_input"
    )

    col_del, col_empty = st.columns([1, 2])
    with col_del:
        if st.button("🗑️ Delete My Data", type="secondary", key="delete_data_btn",
                     disabled=(confirm_delete != "DELETE"), use_container_width=True):
            if confirm_delete == "DELETE":
                delete_user_data(user_id)
                log_audit(user_id, "DATA_DELETION", "User deleted all data")
                st.success("✅ All your data has been permanently deleted.")
                st.info("Your account remains active. You can upload new documents anytime.")
                st.rerun()

    # ---- Security Info ----
    st.markdown("---")
    st.markdown("### 🔒 Security & Privacy")

    st.markdown("""
    <div class="card">
        <strong>✅ Encryption:</strong> All uploaded files are encrypted with AES-128-CBC before storage.<br>
        <strong>✅ PHI Redaction:</strong> Patient names, emails, and phone numbers are automatically stripped before AI analysis.<br>
        <strong>✅ Data Isolation:</strong> Your data is isolated to your account. No other user can see it.<br>
        <strong>✅ No AI Training:</strong> We do not train AI models on your clinical trial data.<br>
        <strong>✅ HIPAA/PPB Aligned:</strong> Our data handling follows HIPAA and African regulatory guidelines.<br>
        <strong>✅ Password Security:</strong> Passwords are hashed with bcrypt (never stored in plain text).<br>
        <strong>✅ HTTPS:</strong> All data in transit is encrypted via TLS.
    </div>
    """, unsafe_allow_html=True)

    show_disclaimer()
