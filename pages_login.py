"""
Wayne AI Pharma - Login / Signup Page
"""
import streamlit as st
from auth import (
    init_session, login_user, hash_password, verify_password,
    is_valid_email, is_strong_password
)
from database import init_db, create_user, get_user_by_email, log_audit
from ui_components import show_brand_header, show_disclaimer, inject_css


def render_login_page():
    inject_css()
    init_session()

    # If already authenticated, redirect to dashboard
    if st.session_state.get("authenticated"):
        st.session_state.page = "dashboard"
        st.rerun()

    show_brand_header("Clinical trials 10x faster. 20x cheaper. Built for Africa.")

    tab_login, tab_signup = st.tabs(["🔑 Login", "✨ Create Account"])

    # ---- LOGIN TAB ----
    with tab_login:
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email", placeholder="you@hospital.org", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)

            if submitted:
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    user = get_user_by_email(email.lower().strip())
                    if user and verify_password(password, user["password_hash"]):
                        login_user(user["id"], user["email"])
                        log_audit(user["id"], "LOGIN", f"User {user['email']} logged in")
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password. Please try again.")

    # ---- SIGNUP TAB ----
    with tab_signup:
        with st.form("signup_form", clear_on_submit=False):
            email = st.text_input("Work Email", placeholder="you@hospital.org", key="signup_email")
            password = st.text_input("Password", type="password",
                                     placeholder="Min 8 chars, uppercase, lowercase, digit",
                                     key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password",
                                             placeholder="Re-enter your password",
                                             key="signup_confirm")

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.caption("✅ 8+ characters")
            with col2:
                st.caption("✅ Upper & lowercase")
            with col3:
                st.caption("✅ At least 1 digit")

            submitted = st.form_submit_button("Create Account", use_container_width=True)

            if submitted:
                email = email.lower().strip()

                # Validate email
                if not email or not password:
                    st.error("Please fill in all fields.")
                elif not is_valid_email(email):
                    st.error("Please enter a valid email address.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    valid, msg = is_strong_password(password)
                    if not valid:
                        st.error(msg)
                    else:
                        existing = get_user_by_email(email)
                        if existing:
                            st.error("An account with this email already exists. Please log in instead.")
                        else:
                            try:
                                init_db()
                                pw_hash = hash_password(password)
                                user_id = create_user(email, pw_hash)
                                log_audit(user_id, "SIGNUP", f"New user: {email}")
                                st.success("✅ Account created! Please log in.")
                                st.info("👆 Switch to the 'Login' tab to sign in.")
                            except Exception as e:
                                st.error(f"Error creating account: {str(e)}")

    # Disclaimer
    show_disclaimer()
