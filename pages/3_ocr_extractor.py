import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

st.title("🔎 OCR Text Extractor")
st.write("Upload scanned PDFs or images, extract the text, and download it as a clean PDF.")

uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf", "jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

def ocr_image(img):
    """Extract text from a Pillow image using Tesseract."""
    return pytesseract.image_to_string(img)

def ocr_pdf(pdf_bytes):
    """Convert each page of a PDF to an image, then OCR."""
    pages = convert_from_bytes(pdf_bytes)
    extracted_text = ""
    for page in pages:
        extracted_text += pytesseract.image_to_string(page) + "\n\n"
    return extracted_text

def create_pdf(text):
    """Generate a PDF with the extracted text."""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    text_object = pdf.beginText(40, 750)
    text_object.setLeading(14)

    # Write line by line
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

if uploaded_files:
    if st.button("📝 Extract Text"):
        all_text = ""

        with st.spinner("Processing... This may take a few seconds."):
            for f in uploaded_files:
                if f.type == "application/pdf":
                    all_text += ocr_pdf(f.read())
                else:
                    img = Image.open(f)
                    all_text += ocr_image(img) + "\n\n"

        st.subheader("🧾 Extracted Text")
        st.write(all_text)

        # Create downloadable PDF
        pdf_buffer = create_pdf(all_text)

        st.download_button(
            label="📥 Download Extracted Text as PDF",
            data=pdf_buffer,
            file_name="extracted_text.pdf",
            mime="application/pdf"
        )
