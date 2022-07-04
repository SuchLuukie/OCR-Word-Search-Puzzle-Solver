# Import libraries
from PIL import Image

class OCR:
    def __init__(self) -> None:
        img = Image.open("puzzle.jpg")
        print(self.recognise(img))

    def recognise(self, img):
        return

if __name__ == "__main__":
    OCR()