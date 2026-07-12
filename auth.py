"""
Wayne AI Pharma - Authentication Module
Email + Password with bcrypt hashing.
"""
import re
import bcrypt
import streamlit as st
from database import (
    init_db, create_user, get_user_by_email, get_user_by_id,
    update_user_settings, delete_user_data, log_audit
)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_strong_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    return True, ""


# ---- Session State Helpers ----
def init_session():
    """Initialize session state variables."""
    defaults = {
        "authenticated": False,
        "user_id": None,
        "user_email": None,
        "page": "login",
        "analysis_result": None,
        "current_analysis_id": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def login_user(user_id: int, email: str):
    st.session_state.authenticated = True
    st.session_state.user_id = user_id
    st.session_state.user_email = email
    st.session_state.page = "dashboard"


def logout_user():
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.page = "login"
    st.session_state.analysis_result = None
    st.session_state.current_analysis_id = None


def require_auth():
    """Decorator-like gate: if not authenticated, redirect to login."""
    if not st.session_state.get("authenticated"):
        st.session_state.page = "login"
        st.rerun()
