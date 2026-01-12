# simple_ocr.py
from PIL import Image
import pytesseract

# Path to your image file (png, jpg, jpeg)
image_path = "C:/Users/karen/Downloads/téléchargement.png"

# Open the image
image = Image.open(image_path)

# Extract text using pytesseract
extracted_text = pytesseract.image_to_string(image)

# Print the result
print("Extracted Text:\n")
print(extracted_text)
