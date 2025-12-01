import streamlit as st
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Image Description", layout="wide")
st.header("🖼️ Image Description")

uploaded_images = st.file_uploader(
    "Upload image(s) (jpg, png, gif, webp)",
    type=["jpg", "jpeg", "png", "gif", "webp"],
    accept_multiple_files=True
)

def describe_image(img_file):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type":"input_text","text":"Describe this image in detail."},
                {"type":"input_file","file":img_file}
            ]
        }]
    )
    return response.output_text

if uploaded_images:
    for img_file in uploaded_images:
        col1, col2 = st.columns([1,2])
        img = Image.open(img_file)
        with col1: 
            st.image(img, caption=img_file.name, use_column_width=True)
        with col2:
            with st.spinner(f"Describing {img_file.name}..."):
                description = describe_image(img_file)
            st.markdown(
                f"<div style='background-color:#FFF4E5; padding:15px; border-radius:10px;'>{description}</div>",
                unsafe_allow_html=True
            )
