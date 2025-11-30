import streamlit as st

st.set_page_config(page_title="AI Doc & Image Analyzer", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4B0082;'>✨ AI Document & Image Analyzer</h1>", unsafe_allow_html=True)
st.markdown("""
Welcome to your AI Document & Image Analyzer!

Use the sidebar or the pages below to:
- Summarize PDFs quickly and clearly.
- Generate detailed descriptions of uploaded images.
""")

st.info("""
Make sure your **OpenAI API key** is stored in a `.env` file:
