import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import zipfile
import os
import cv2
import numpy as np
from langdetect import detect

# -------------------------
# Session state
# -------------------------
if "current_texts" not in st.session_state:
    st.session_state.current_texts = {}

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# -------------------------
# Tesseract setup
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESSERACT_PATH = os.path.join(BASE_DIR, "tesseract", "tesseract.exe")

if not os.path.exists(TESSERACT_PATH):
    st.error("OCR engine missing.")
    st.stop()

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
OCR_LANGS = "eng+fra+spa+deu"

# -------------------------
# UI
# -------------------------
st.title("🔎 OCR Text Extractor")
st.write("Upload documents, extract text, and download OCR PDFs.")

# -------------------------
# Upload
# -------------------------
uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf", "jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}",
)

if uploaded_files:
    st.caption(f"✅ {len(uploaded_files)} file(s) ready")

    st.markdown("**Files ready for extraction:**")
    for f in uploaded_files:
        st.write(f"• {f.name}")

# -------------------------
# Clear uploaded files
# -------------------------
if uploaded_files:
    if st.button("🗑️ Clear uploaded files"):
        st.session_state.current_texts.clear()
        st.session_state.uploader_key += 1
        st.rerun()

# -------------------------
# SAFE image utilities
# -------------------------
def to_gray_cv(image):
    arr = np.array(image)
    if len(arr.shape) == 2:
        return arr
    return cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)

def is_noisy(image, threshold=12):
    gray = to_gray_cv(image)
    return cv2.Laplacian(gray, cv2.CV_64F).var() < threshold

def is_blurry(image, threshold=100):
    gray = to_gray_cv(image)
    return cv2.Laplacian(gray, cv2.CV_64F).var() < threshold

def denoise(image):
    arr = np.array(image)
    return Image.fromarray(cv2.medianBlur(arr, 5))

def sharpen(image):
    arr = np.array(image)
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return Image.fromarray(cv2.filter2D(arr, -1, kernel))

def preprocess_image(image):
    """Apply ONLY what is needed."""
    if is_noisy(image):
        image = denoise(image)
    if is_blurry(image):
        image = sharpen(image)
    return image

# -------------------------
# OCR logic
# -------------------------
def ocr_image(image):
    image = preprocess_image(image)
    data = pytesseract.image_to_data(
        image,
        lang=OCR_LANGS,
        output_type=pytesseract.Output.DICT
    )

    words = []
    confs = []

    for txt, conf in zip(data["text"], data["conf"]):
        try:
            conf = int(conf)
            if conf > 0 and txt.strip():
                words.append(txt)
                confs.append(conf)
        except:
            pass

    text = " ".join(words)
    avg_conf = sum(confs) / len(confs) if confs else 0
    return text, avg_conf

def ocr_pdf(pdf_bytes):
    pages = convert_from_bytes(pdf_bytes)
    texts = []
    confs = []

    for page in pages:
        text, conf = ocr_image(page)
        texts.append(text)
        confs.append(conf)

    return "\n\n".join(texts), sum(confs) / len(confs) if confs else 0

# -------------------------
# PDF generation
# -------------------------
def create_pdf(text):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    t = pdf.beginText(40, 750)
    t.setLeading(14)

    for line in text.split("\n"):
        if t.getY() < 40:
            pdf.drawText(t)
            pdf.showPage()
            t = pdf.beginText(40, 750)
            t.setLeading(14)
        t.textLine(line)

    pdf.drawText(t)
    pdf.save()
    buffer.seek(0)
    return buffer

# -------------------------
# Extract button
# -------------------------
if uploaded_files and st.button("📝 Extract Text"):
    st.session_state.current_texts.clear()

    for f in uploaded_files:
        with st.spinner(f"Processing {f.name}..."):
            if f.type == "application/pdf":
                text, conf = ocr_pdf(f.read())
            else:
                img = Image.open(f).convert("RGB")
                text, conf = ocr_image(img)

            st.session_state.current_texts[f.name] = text
            st.success(f"{f.name} processed (confidence: {conf:.1f}%)")

# -------------------------
# ZIP download (persistent)
# -------------------------
if st.session_state.current_texts:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for name, text in st.session_state.current_texts.items():
            pdf_buffer = create_pdf(text)
            pdf_name = os.path.splitext(name)[0] + "_extracted.pdf"
            zf.writestr(pdf_name, pdf_buffer.getvalue())

    zip_buffer.seek(0)

    st.download_button(
        "📥 Download current PDFs (ZIP)",
        zip_buffer,
        "current_extracted_pdfs.zip",
        "application/zip",
    )
