import streamlit as st
from pypdf import PdfReader
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv
import os

# ==========================
# Load API key
# ==========================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==========================
# Page config
# ==========================
st.set_page_config(
    page_title="AI Document & Image Analyzer",
    # page_icon="✨",
    layout="wide"
)

# ==========================
# Sidebar
# ==========================
st.sidebar.title("Instructions")
st.sidebar.info("""
1. **PDF Summarizer:** Upload one or more PDFs and click "Summarize PDFs".  
2. **Image Description:** Upload images (`jpg`, `png`, `gif`, `webp`) to get detailed AI-generated descriptions.  
                """)
# 3. Make sure your **OpenAI API key** is set in `.env`.


# ==========================
# Main title
# ==========================
st.markdown("<h1 style='text-align: center; color: #4B0082;'>AI Document & Image Analyzer</h1>", unsafe_allow_html=True)

# ==========================
# Tabs
# ==========================
tab1, tab2 = st.tabs(["📄 Summarize PDFs", "🖼️ Describe Images"])

# ============================================
# TAB 1 — PDF SUMMARIZER
# ============================================
with tab1:
    st.header("📚 Summarize PDF Documents")
    uploaded_pdfs = st.file_uploader(
        "Upload your PDF file(s)",
        type=["pdf"],
        accept_multiple_files=True
    )

    def extract_text_from_pdf(file):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text

    def summarize_text(text):
        prompt = f"""
        Summarize the following document(s) into clear bullet points.
        Focus on the main ideas and avoid unnecessary details.

        TEXT:
        {text[:120000]}
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content

    if uploaded_pdfs:
        if st.button("Summarize PDFs"):
            with st.spinner("Extracting text and generating summary..."):
                combined_text = ""
                for pdf in uploaded_pdfs:
                    combined_text += extract_text_from_pdf(pdf) + "\n\n"
                summary = summarize_text(combined_text)

            # Display summary in an expander
            with st.expander("📝 Summary", expanded=True):
                st.markdown(f"<div style='background-color:#F3E8FF; padding:15px; border-radius:10px;'>{summary}</div>", unsafe_allow_html=True)

# ============================================
# TAB 2 — IMAGE DESCRIPTION
# ============================================
with tab2:
    st.header("🖼️ Describe Uploaded Images")
    uploaded_images = st.file_uploader(
        "Upload your image(s)",
        type=["jpg", "jpeg", "png", "gif", "webp"],
        accept_multiple_files=True
    )

    def describe_image(img_file):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Describe this image in detail."},
                        {"type": "input_file", "file": img_file}
                    ]
                }
            ]
        )
        return response.output_text

    if uploaded_images:
        for img_file in uploaded_images:
            # Use columns for image and description side by side
            col1, col2 = st.columns([1, 2])
            img = Image.open(img_file)
            with col1:
                st.image(img, caption=img_file.name, use_column_width=True)
            with col2:
                with st.spinner(f"Describing {img_file.name}..."):
                    description = describe_image(img_file)
                st.markdown(f"<div style='background-color:#FFF4E5; padding:15px; border-radius:10px;'>{description}</div>", unsafe_allow_html=True)
