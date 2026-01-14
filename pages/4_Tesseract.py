import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import zipfile
import os

# --- Initialize session state for OCR extracted text ---
if "extracted_texts" not in st.session_state:
    st.session_state.extracted_texts = {}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESSERACT_PATH = os.path.join(BASE_DIR, "tesseract", "tesseract.exe")

# Safety check
if not os.path.exists(TESSERACT_PATH):
    st.error("OCR engine missing. Please contact the app provider.")
    st.stop()

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# --- Set path to your Tesseract executable ---
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Dynamically point to bundled tesseract
#pytesseract.pytesseract.tesseract_cmd = os.path.join(os.getcwd(), "tesseract", "tesseract.exe")

st.title("🔎 OCR Text Extractor")
st.write("Upload scanned PDFs or images, extract the text, and download all as separate PDFs in one ZIP.")

uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf", "jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

def ocr_image(img):
    return pytesseract.image_to_string(img)

def ocr_pdf(pdf_bytes):
    pages = convert_from_bytes(pdf_bytes)
    extracted_text = ""
    for page in pages:
        extracted_text += pytesseract.image_to_string(page) + "\n\n"
    return extracted_text

def create_pdf(text):
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

# --- Extract text and save in session state ---
if uploaded_files:
    if st.button("📝 Extract Text & Download PDFs"):
        with st.spinner("Processing... This may take a few seconds."):

            # Process each uploaded file and store extracted text in session state
            for f in uploaded_files:
                if f.name not in st.session_state.extracted_texts:
                    if f.type == "application/pdf":
                        text = ocr_pdf(f.read())
                    else:
                        img = Image.open(f)
                        text = ocr_image(img)
                    st.session_state.extracted_texts[f.name] = text

            # Create ZIP with one PDF per uploaded file
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, mode="w") as zf:
                for filename, text in st.session_state.extracted_texts.items():
                    pdf_buffer = create_pdf(text)
                    pdf_name = os.path.splitext(filename)[0] + "_extracted.pdf"
                    zf.writestr(pdf_name, pdf_buffer.getvalue())

            zip_buffer.seek(0)

            # Provide one download button for all PDFs
            st.download_button(
                label="📥 Download All PDFs (ZIP)",
                data=zip_buffer,
                file_name="extracted_pdfs.zip",
                mime="application/zip"
            )

# --- Optional: show extracted text previews ---
if st.session_state.extracted_texts:
    st.subheader("🧾 Previously Extracted Texts")
    for filename, text in st.session_state.extracted_texts.items():
        st.markdown(f"**{filename}**")
        st.write(text)
