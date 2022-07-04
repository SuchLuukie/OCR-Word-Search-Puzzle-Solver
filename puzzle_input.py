# Import libraries
from PIL import Image
import cv2


class PuzzleInput:
    def __init__(self):
        # Get image and convert to grayscale (To be safe)
        self.image = cv2.imread('puzzles/puzzle0.jpg')
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Extract the puzzle from the image
        self.extract_puzzle(self.gray)


    # Extract the puzzle from 
    def extract_puzzle(self, img):
        segments = self.extract_segments(img)
        

    # Extract the segments of the letters in the image (Preparing for OCR)
    def extract_segments(self, img):
        threshold = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
        contours = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        segments = []
        for c in contours:
            segment = cv2.boundingRect(c)
            segments.append(segment)

            # Box around the segment to show the letters
            x,y,w,h = segment
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (36,255,12), 2)

        cv2.imshow("image", self.image)
        cv2.waitKey()
        return segments

    # Extract the background colour of an image
    def extract_background_colour(self, img):
        # Get all the colours used in the image
        colours = img.getcolors()

        # The most used colour is the background colour
        count, background_colour = max(colours)

        return background_colour

if __name__ == "__main__":
    PuzzleInput()