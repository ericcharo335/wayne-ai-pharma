"""
Wayne AI Pharma - Main Application Entry Point
Clinical Trial AI for Africa — 10x faster, 20x cheaper than McKinsey.
"""
import streamlit as st
from database import init_db
from pages_login import render_login_page
from pages_dashboard import render_dashboard
from pages_analyzer import render_analyzer
from pages_history import render_history
from pages_settings import render_settings
from ui_components import inject_css


def main():
    # ---- Page Config ----
    st.set_page_config(
        page_title="Wayne AI Pharma",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": None,
            "Report a bug": None,
            "About": "Wayne AI Pharma — Clinical trials 10x faster, 20x cheaper. Built for Africa."
        }
    )

    # ---- Initialize Database ----
    init_db()

    # ---- Initialize Session ----
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # ---- Route to correct page ----
    current_page = st.session_state.page

    if current_page == "login":
        render_login_page()
    elif current_page == "dashboard":
        render_dashboard()
    elif current_page == "analyzer":
        render_analyzer()
    elif current_page == "history":
        render_history()
    elif current_page == "settings":
        render_settings()
    else:
        render_login_page()


if __name__ == "__main__":
    main()
