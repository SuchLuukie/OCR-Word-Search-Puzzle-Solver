# Import libraries
import cv2

# https://stackoverflow.com/questions/60515216/extracting-and-saving-characters-from-an-image

class PuzzleInput:
    def __init__(self):
        # Get image and convert to grayscale (To be safe)
        self.image = cv2.imread('puzzles/puzzle1.jpg')
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image_area = self.image.shape[0] * self.image.shape[1]

        # Extract the puzzle from the image
        self.extract_puzzle(self.gray)


    # Extract the puzzle from image
    def extract_puzzle(self, img):
        # Get the contours of the letters
        contours = self.extract_contours(img)

        self.visualise(self.image, contours)

        # Now determine which are letters and words
        contours, words = self.extract_words(contours)
        letters = self.extract_letters(contours)


    # Extracts words and removes them from contour
    def extract_words(self, contour):
        words = []
        return contour, words


    # Extracts letters
    def extract_letters(self, contours):
        return


    def get_image_from_contour(self, img, contour):
        x, y, w, h = contour
        image = img[y:y+h, x:x+w]
        return image
        

    # Extract the contours of the letters in the image (Preparing for OCR)
    def extract_contours(self, img):
        threshold = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
        contours = list(cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0])

        segments = []
        # Check if there's a contour that's too large
        for contour in contours:
            if cv2.contourArea(contour) > self.image_area * 0.1:
                # This means that it most likely contains a box/grid of the puzzle
                # If so, we look inside that contour for new contours
                new_segment = list(cv2.boundingRect(contour))
                new_image = self.get_image_from_contour(img, new_segment)

                new_threshold = cv2.threshold(new_image, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
                new_contours = cv2.findContours(new_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

                # Add the new contour's bounding box to the segments
                for new_contour in new_contours:
                    segment = list(cv2.boundingRect(new_contour))

                    # If the x and y of the segment is 0 then it's the original contour
                    if segment[0] != 0 and segment[1] != 0:
                        # Offset the contour by the location of the original contour and add it
                        segment[0] += new_segment[0]
                        segment[1] += new_segment[1]
                        segments.append(segment)

                    
            else:
                # Also get the bounding boxes of the contours as list
                segments.append(list(cv2.boundingRect(contour)))

        return segments

    # Visualise the contours onto the image
    def visualise(self, image, contours):
        for idx, contour in enumerate(contours):
            x, y, w, h = contour
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.putText(self.image, str(idx), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (36,255,12), 2)

        cv2.imshow("img", image)
        cv2.waitKey()


if __name__ == "__main__":
    PuzzleInput()