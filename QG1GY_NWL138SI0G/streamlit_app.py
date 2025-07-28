import streamlit as st

st.set_page_config(
    page_title="Fraud Analytics Dashboard",
    page_icon="👋",
)

st.write("# Fraud Analytics Dashboard")

st.sidebar.success("Select a segmentation.")

st.markdown(
    """
    Gain insights about current and past fraud cases.

    Use the sidebar to navigate to specific insights:
    - Weekday Fraud Patterns
    - Night vs. Day Fraud Activity
    - Age Group Risk Analysis
"""
)