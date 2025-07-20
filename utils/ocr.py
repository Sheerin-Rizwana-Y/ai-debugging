import pytesseract
from PIL import Image
import io
import base64

def extract_text_from_image(image_data):
    """
    Extracts text from base64-encoded image data using Tesseract OCR.
    """
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text
