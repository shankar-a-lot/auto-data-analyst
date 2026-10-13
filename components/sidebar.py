import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("## 📊 Auto Data Analyst")
        st.caption("A lightweight, rule-based analytics workspace")
        st.divider()
        st.markdown("### 1. Upload your data")
        uploaded_file = st.file_uploader(
            "CSV or Excel file", type=["csv", "xlsx", "xls"],
            help="Your data is analyzed by this application; no AI API is required."
        )
        st.divider()
        st.markdown("### 2. Visualization settings")
        max_charts = st.slider("Maximum charts", min_value=4, max_value=20, value=12)
        st.caption("Charts are selected from detected column roles and data characteristics.")
        st.divider()
        st.markdown("**Built for exploration**")
        st.caption("Profile → Analyze → Visualize → Report")
    return uploaded_file, max_charts
