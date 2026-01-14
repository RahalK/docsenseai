import streamlit as st
from PIL import Image
import easyocr
from pdf2image import convert_from_bytes
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import numpy as np

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🔎 OCR Text Extractor")
st.write("Upload scanned documents, extract the text, and download it as a clean PDF.")

uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf", "jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

# -----------------------------
# EasyOCR Reader (cached)
# -----------------------------
@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(["en"], gpu=False)

reader = load_ocr_reader()

# -----------------------------
# Helper: format EasyOCR output
# -----------------------------
def format_easyocr_result(result, y_threshold=15):
    """
    Reconstruct text lines from EasyOCR output using vertical position.
    """
    lines = []

    for bbox, text, _ in result:
        # Average Y position of the bounding box
        y_center = sum(point[1] for point in bbox) / 4

        placed = False
        for line in lines:
            if abs(line["y"] - y_center) < y_threshold:
                line["texts"].append(text)
                placed = True
                break

        if not placed:
            lines.append({"y": y_center, "texts": [text]})

    # Sort lines top-to-bottom
    lines.sort(key=lambda x: x["y"])

    # Join words per line
    formatted_text = "\n".join(" ".join(line["texts"]) for line in lines)
    return formatted_text

# -----------------------------
# OCR functions
# -----------------------------
def ocr_image(img: Image.Image) -> str:
    """
    Extract text from a Pillow image using EasyOCR,
    preserving line breaks.
    """
    img_array = np.array(img)
    result = reader.readtext(img_array)
    return format_easyocr_result(result)

def ocr_pdf(pdf_bytes: bytes) -> str:
    """
    Convert each page of a PDF to an image, then OCR,
    preserving line breaks.
    """
    pages = convert_from_bytes(pdf_bytes)
    extracted_text = ""

    for page in pages:
        page_array = np.array(page)
        result = reader.readtext(page_array)
        extracted_text += format_easyocr_result(result) + "\n\n"

    return extracted_text

# -----------------------------
# PDF creation
# -----------------------------
def create_pdf(text: str) -> io.BytesIO:
    """
    Generate a PDF with the extracted text.
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    text_object = pdf.beginText(40, 750)
    text_object.setLeading(14)

    for line in text.split("\n"):
        if text_object.getY() < 40:
            pdf.drawText(text_object)
            pdf.showPage()
            text_object = pdf.beginText(40, 750)
            text_object.setLeading(14)

        text_object.textLine(line)

    pdf.drawText(text_object)
    pdf.save()
    buffer.seek(0)
    return buffer

# -----------------------------
# Main processing logic
# -----------------------------
if uploaded_files:
    if st.button("📝 Extract Text"):
        all_text = ""

        with st.spinner("Processing... This may take a few seconds."):
            for f in uploaded_files:
                if f.type == "application/pdf":
                    all_text += ocr_pdf(f.read())
                else:
                    img = Image.open(f).convert("RGB")
                    all_text += ocr_image(img) + "\n\n"

        st.subheader("🧾 Extracted Text")
        st.write(all_text)

        pdf_buffer = create_pdf(all_text)

        st.download_button(
            label="📥 Download Extracted Text as PDF",
            data=pdf_buffer,
            file_name="extracted_text.pdf",
            mime="application/pdf"
        )
