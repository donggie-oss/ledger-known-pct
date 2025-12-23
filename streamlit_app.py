import streamlit as st

st.set_page_config(
    page_title="GigaSphere Execution Viewers",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔑 FORCE SIDEBAR INITIALIZATION
st.sidebar.markdown("")

st.title("GigaSphere Execution Viewers")
st.caption("Canon-safe. Viewer-only. No execution.")

st.markdown("""
Use the sidebar to switch between:

• **Module One — Execution Viewer**  
• **Module Two — Decision Viewer**
""")
