# Import libraries
import cv2

# https://stackoverflow.com/questions/60515216/extracting-and-saving-characters-from-an-image

class PuzzleInput:
    def __init__(self):
        # Get image and convert to grayscale (To be safe)
        self.image = cv2.imread('puzzles/puzzle0.jpg')
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Extract the puzzle from the image
        self.extract_puzzle(self.gray)


    # Extract the puzzle from image
    def extract_puzzle(self, img):
        # Get the segments of the letters
        segments = self.extract_segments(img)

        self.visualise(segments)

        # Now determine which are letters and words
        segments, words = self.extract_words(segments)
        letters = self.extract_letters(segments)


    # Extracts words and removes them from segments
    def extract_words(self, segments):
        words = []
        return segments, words


    # Extracts letters
    def extract_letters(self, segments):
        return


    def get_image_from_segment(self, img, segment):
        x, y, w, h = segment
        image = img[y:y+h, x:x+w]
        return image
        

    # Extract the segments of the letters in the image (Preparing for OCR)
    def extract_segments(self, img):
        threshold = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
        contours = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        # Get the bounding box of the contour
        segments = [cv2.boundingRect(contour) for contour in contours]

        # Reverse list for convenience
        segments = list(reversed(segments))

        return segments

    # Visualise the segments onto the image
    def visualise(self, segments):
        for idx, segment in enumerate(segments):
            x, y, w, h = segment
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.putText(self.image, str(idx), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (36,255,12), 2)
        cv2.imshow("img", self.image)
        cv2.waitKey()


if __name__ == "__main__":
    PuzzleInput()