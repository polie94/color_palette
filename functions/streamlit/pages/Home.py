import streamlit as st
from colour_analysis import colour_analysis
st.set_page_config(
    page_title="Princess´ World",
    page_icon="",
    layout="wide"
)

pages = [
    st.Page(colour_analysis, title="Colour analysis"),
    st.Page("placeholder.py", title="Another page")
]

current_page = st.navigation(pages)
current_page.run()
