import streamlit as st


def render_header():
    st.markdown("""
    <div class="ada-hero">
      <div class="ada-kicker">Explore · Analyze · Discover</div>
      <h1>📊 Auto Data Analyst</h1>
      <p>Turn any structured dataset into clear analysis, useful visualizations, and a shareable report.</p>
    </div>
    """, unsafe_allow_html=True)


def render_footer(text="Auto Data Analyst · Rule-based analysis · No external AI API"):
    st.markdown(f'<div class="ada-footer">{text}</div>', unsafe_allow_html=True)
