# Import libraries
import pytesseract

# Set the tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
xconfig = r'--oem 3 --psm 6'

class OCR_Model:
    def recognise(self, image):
        return pytesseract.image_to_string(image)