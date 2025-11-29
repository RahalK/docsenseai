import streamlit as st
from pypdf import PdfReader
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("✨ AI Document & Image Analyzer")

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

    # Extract text
    def extract_text_from_pdf(file):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text

    # Summarize text using chat.completions
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
            with st.spinner("Extracting and summarizing..."):
                combined_text = ""
                for pdf in uploaded_pdfs:
                    combined_text += extract_text_from_pdf(pdf) + "\n\n"

                summary = summarize_text(combined_text)

            st.subheader("📝 Summary")
            st.write(summary)


# ============================================
# TAB 2 — IMAGE DESCRIPTION
# ============================================
with tab2:
    st.header("🖼️ Describe Uploaded Images")

    uploaded_images = st.file_uploader(
        "Upload your image(s)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    # New Responses API with base64 images
    def describe_image(image_bytes):
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{base64_image}"

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Describe this image in detail."},
                        {"type": "input_image", "image_url": data_url}
                    ]
                }
            ]
        )

        return response.output_text

    if uploaded_images:
        for img_file in uploaded_images:
            img = Image.open(img_file)
            st.image(img, caption=img_file.name, width=300)

            img_bytes = img_file.read()

            with st.spinner(f"Describing {img_file.name}..."):
                description = describe_image(img_bytes)

            st.subheader(f"📝 Description for {img_file.name}")
            st.write(description)
