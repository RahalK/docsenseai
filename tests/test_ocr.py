from PyPDF2 import PdfReader


def extract_text_with_pyPDF(PDF_File):
    pdf_reader = PdfReader(PDF_File)

    raw_text = ''

    for i, page in enumerate(pdf_reader.pages):

        text = page.extract_text()
        if text:
            raw_text += text

    return raw_text

text_with_pyPDF = extract_text_with_pyPDF("C:/Users/karen/Downloads/téléchargement.pdf")
print(text_with_pyPDF)

for i, page in enumerate(pdf_reader.pages):
    text = page.extract_text()
    print(f"Page {i+1} text length:", len(text) if text else 0)
    if text:
        raw_text += text



"""
import pypdfium2 as pdfium
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

def convert_pdf_to_images(file_path, scale=300 / 72):
    pdf_file = pdfium.PdfDocument(file_path)
    page_indices = [i for i in range(len(pdf_file))]

    renderer = pdf_file.render(
        pdfium.PdfBitmap.to_pil,
        page_indices=page_indices,
        scale=scale,
    )

    list_final_images = []

    for i, image in zip(page_indices, renderer):
        image_byte_array = BytesIO()
        image.save(image_byte_array, format='jpeg', optimize=True)
        list_final_images.append({i: image_byte_array.getvalue()})

    return list_final_images


def display_images(list_dict_final_images):
    all_images = [list(data.values())[0] for data in list_dict_final_images]

    for index, image_bytes in enumerate(all_images):
        image = Image.open(BytesIO(image_bytes))
        figure = plt.figure(figsize=(image.width / 100, image.height / 100))

        plt.title(f"----- Page Number {index + 1} -----")
        plt.imshow(image)
        plt.axis("off")
        plt.show()

# ✅ Provide a PDF file path, not a PNG
pdf_images = convert_pdf_to_images("C:/Users/karen/Downloads/téléchargement.pdf")
display_images(pdf_images)




***

import pypdfium2 as pdfium
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO


def convert_pdf_to_images(file_path, scale=300 / 72):
    pdf_file = pdfium.PdfDocument(file_path)
    page_indices = [i for i in range(len(pdf_file))]

    renderer = pdf_file.render(
        pdfium.PdfBitmap.to_pil,
        page_indices=page_indices,
        scale=scale,
    )

    list_final_images = []

    for i, image in zip(page_indices, renderer):
        image_byte_array = BytesIO()
        image.save(image_byte_array, format='jpeg', optimize=True)
        image_byte_array = image_byte_array.getvalue()
        list_final_images.append(dict({i: image_byte_array}))

    return list_final_images


def display_images(list_dict_final_images):
    all_images = [list(data.values())[0] for data in list_dict_final_images]

    for index, image_bytes in enumerate(all_images):
        image = Image.open(BytesIO(image_bytes))
        figure = plt.figure(figsize=(image.width / 100, image.height / 100))

        plt.title(f"----- Page Number {index + 1} -----")
        plt.imshow(image)
        plt.axis("off")
        plt.show()

convert_pdf_to_images = convert_pdf_to_images("C:/Users/karen/Downloads/téléchargement.pdf")

#convert_pdf_to_images
display_images(convert_pdf_to_images)
"""