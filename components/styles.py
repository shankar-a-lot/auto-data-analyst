import streamlit as st


def apply_styles():
    """Apply a consistent light theme with explicit contrast for custom HTML cards."""
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root {
  --ada-ink:#172554; --ada-muted:#64748b; --ada-line:#e2e8f0;
  --ada-primary:#4f46e5; --ada-card:#ffffff; --ada-page:#f5f7ff;
}
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:linear-gradient(180deg,#f8faff 0%,#f2f5fc 100%) !important; color:#172554; }
[data-testid="stAppViewContainer"], [data-testid="stMain"] { background:transparent !important; }
.block-container { max-width:1500px; padding-top:1.4rem; padding-bottom:3rem; }
h1,h2,h3,h4 { font-family:'Manrope',sans-serif !important; color:#172554 !important; }
h1 { letter-spacing:-1.2px; }
p, label, [data-testid="stMarkdownContainer"] { color:#263451; }
small, [data-testid="stCaptionContainer"] { color:#64748b !important; }
[data-testid="stMetric"] {
  background:linear-gradient(135deg,#ffffff,#f7f8ff) !important;
  border:1px solid #e4e9f5; padding:18px 20px; border-radius:18px;
  box-shadow:0 5px 18px rgba(30,41,90,.055);
}
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p { color:#64748b !important; font-weight:600; }
[data-testid="stMetricValue"], [data-testid="stMetricValue"] div { color:#172554 !important; font-family:'Manrope',sans-serif; }
[data-testid="stTabs"] button { font-weight:700; color:#475569 !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color:#4f46e5 !important; }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background:#4f46e5 !important; }
div[data-testid="stVerticalBlockBorderWrapper"] {
  background:#fff !important; border:1px solid #e3e9f5 !important; border-radius:18px !important;
  box-shadow:0 5px 18px rgba(30,41,90,.04);
}
.stButton > button, .stDownloadButton > button {
  border-radius:11px; font-weight:700; border:1px solid #dbe2f0;
  min-height:42px; transition:all .15s ease; color:#273451 !important;
  background:#fff;
}
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {
  background:linear-gradient(100deg,#4f46e5,#7c3aed) !important; color:#fff !important; border:0;
}
[data-testid="stFileUploader"] { background:#fff !important; border:1px dashed #a5b4fc; padding:10px; border-radius:16px; }
[data-testid="stFileUploader"] * { color:#263451 !important; }
[data-testid="stDataFrame"] { border:1px solid #e6ebf4; border-radius:12px; overflow:hidden; }
[data-testid="stSidebar"] { background:#fff !important; border-right:1px solid #e8ecf5; }
[data-testid="stSidebar"] * { color:#263451; }
.ada-hero {
  background:linear-gradient(115deg,#172554 0%,#3730a3 58%,#6d28d9 100%);
  padding:29px 32px; border-radius:22px; color:#fff !important; margin-bottom:22px;
  box-shadow:0 12px 30px rgba(55,48,163,.18); position:relative; overflow:hidden;
}
.ada-hero:after { content:''; position:absolute; width:230px; height:230px; right:-50px; top:-110px; border:1px solid rgba(255,255,255,.18); border-radius:50%; box-shadow:0 0 0 28px rgba(255,255,255,.035),0 0 0 58px rgba(255,255,255,.025); }
.ada-hero h1 { color:#fff !important; margin:0 0 7px 0; font-size:2.05rem; }
.ada-hero p { color:#e0e7ff !important; margin:0; font-size:1rem; }
.ada-kicker { text-transform:uppercase; letter-spacing:1.5px; font-size:.72rem; font-weight:700; color:#c7d2fe !important; margin-bottom:8px; }
.ada-section { padding:3px 0 4px 0; }
.ada-note { color:#64748b !important; font-size:.9rem; }
.ada-insight {
  display:block; background:#ffffff !important; color:#24324b !important;
  border:1px solid #e3e8f4; border-left:4px solid #6366f1;
  padding:15px 18px; border-radius:13px; margin:9px 0;
  box-shadow:0 4px 14px rgba(30,41,90,.045); line-height:1.55;
}
.ada-insight b, .ada-insight strong { color:#4338ca !important; font-weight:800; }
.ada-insight * { color:#24324b !important; }
.ada-footer { text-align:center; color:#64748b !important; font-size:.82rem; padding:25px 0 5px 0; }
[data-testid="stAlert"] { border-radius:13px; }
</style>
""", unsafe_allow_html=True)
