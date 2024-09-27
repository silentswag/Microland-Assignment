import pytesseract
from PIL import Image

# If necessary, set the path to Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try:
    print("Tesseract version:", pytesseract.get_tesseract_version())
except Exception as e:
    print(f"Error: {str(e)}")
