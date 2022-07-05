# Import libraries
import pytesseract

class OCR_Model:
    def recognise(self, image):
        return pytesseract.image_to_string(image)