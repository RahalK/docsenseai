import streamlit as st

st.set_page_config(page_title="AI Doc & Image Analyzer", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4B0082;'>AI Document & Image Analyzer</h1>", unsafe_allow_html=True)

st.markdown("""
Welcome to your AI Document & Image Analyzer!

Use the sidebar or the pages below to:
- Summarize PDFs quickly and clearly.
- Generate detailed descriptions of uploaded images.
""")

st.info("""
Make sure your **OpenAI API key** is stored in a `.env` file:
OPENAI_API_KEY=your_key_here
""")

# import streamlit as st

# st.set_page_config(page_title="AI Doc & Image Analyzer", layout="wide")

# st.markdown(
#     f"<div style='background-color:#F3E8FF; color:#2C2C2C; padding:15px; border-radius:10px;'>{summary}</div>",
#     unsafe_allow_html=True
# )
# st.markdown("<h1 style='text-align: center; color: #4B0082;'>✨ AI Document & Image Analyzer</h1>", unsafe_allow_html=True)
# st.markdown("""
# Welcome to your AI Document & Image Analyzer!

# Use the sidebar or the pages below to:
# - Summarize PDFs quickly and clearly.
# - Generate detailed descriptions of uploaded images.
# """)

# st.info("""
# Make sure your **OpenAI API key** is stored in a `.env` file:
# OPENAI_API_KEY=your_key_here
#         """)