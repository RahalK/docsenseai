import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
print("Loaded key:", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="PDF Summarizer", layout="wide")
st.header("📄 PDF Summarizer")

uploaded_pdfs = st.file_uploader(
    "Upload one or more PDF files",
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
    prompt = f"Create a beautifully formatted, elegant presentation that provides a detailed bullet-point summary of the following document(s):\n{text[:120000]}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

if uploaded_pdfs:
    if st.button("Summarize PDFs"):
        with st.spinner("Extracting text and generating summary..."):
            combined_text = "\n\n".join([extract_text_from_pdf(pdf) for pdf in uploaded_pdfs])
            summary = summarize_text(combined_text)

        with st.expander("📝 Summary", expanded=True):
            st.markdown(
                f"<div style='background-color:#D3D3D3; color:#000000; padding:15px; border-radius:10px; white-space:pre-wrap;'>{summary}</div>",
                unsafe_allow_html=True
            )




# import streamlit as st
# from pypdf import PdfReader
# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# # Load API key
# load_dotenv()
# print("Loaded key:", os.getenv("OPENAI_API_KEY"))
# # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# st.set_page_config(page_title="PDF Summarizer", layout="wide")
# st.header("📄 PDF Summarizer")

# uploaded_pdfs = st.file_uploader(
#     "Upload one or more PDF files",
#     type=["pdf"],
#     accept_multiple_files=True
# )

# def extract_text_from_pdf(file):
#     reader = PdfReader(file)
#     text = ""
#     for page in reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"
#     return text

# def summarize_text(text):
#     prompt = f"Summarize the following document(s) into bullet points:\n{text[:120000]}"
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=500
#     )
#     return response.choices[0].message.content

# if uploaded_pdfs:
#     if st.button("Summarize PDFs"):
#         with st.spinner("Extracting text and generating summary..."):
#             combined_text = "\n\n".join([extract_text_from_pdf(pdf) for pdf in uploaded_pdfs])
#             summary = summarize_text(combined_text)

#         with st.expander("📝 Summary", expanded=True):
#             st.markdown(
#                 f"<div style='background-color:#F3E8FF; padding:15px; border-radius:10px;'>{summary}</div>",
#                 unsafe_allow_html=True
#             )
