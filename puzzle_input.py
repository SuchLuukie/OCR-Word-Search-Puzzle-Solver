# Import libraries
import cv2
from itertools import permutations

class PuzzleInput:
    def __init__(self):
        # Get image and convert to grayscale (To be safe)
        self.image = cv2.imread('puzzles/puzzle1.jpg')
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image_area = self.image.shape[0] * self.image.shape[1]

        # Letter spacing range
        self.lsr = self.image.shape[0] * 0.04

        # Extract the puzzle from the image
        self.extract_puzzle(self.gray)


    # Extract the puzzle from image
    def extract_puzzle(self, img):
        # Get the contours of the letters
        contours = self.extract_contours(img)

        # Now determine which are letters and words
        contours, word_contours = self.extract_word_contours(contours)
        board = self.extract_board(contours)

        self.visualise(self.image.copy(), [i for row in board for i in row])
        self.visualise(self.image.copy(), [j for word in word_contours for j in word])

        # Now use OCR to determine what letters the contours are
        #TODO


    # Extracts words and removes them from contour
    def extract_word_contours(self, contours):
        letter_combos = []
        new_contours = contours.copy()

        # We check if it's a word when the contours collide with eachother
        for contour1, contour2 in permutations(contours, 2):
            if self.check_if_word_letter(contour1, contour2):
                combo = [contour1, contour2]
                if not combo in letter_combos and not list(reversed(combo)) in letter_combos:
                    letter_combos.append(combo)

                try:
                    new_contours.remove(contour1)

                except ValueError:
                    continue

        words = []
        word = [letter_combos[0][0]]
        for combo in letter_combos:
            if combo[0] in word:
                if not combo[1] in word:
                    word.append(combo[1])

            else:
                words.append(word)
                word = combo

        # To add the last word
        words.append(word)

        return new_contours, words


    # Extracts letters
    def extract_board(self, contours):
        matches = []
        # We check if it's a word when the contours collide with eachother
        for contour1, contour2 in permutations(contours, 2):
            combo = [contour1, contour2]
            if self.check_if_horizontal_match(contour1, contour2):
                if not combo in matches and not list(reversed(combo)) in matches:
                    matches.append([contour1, contour2])

        board = []
        row = [matches[0][0]]
        for match in matches:
            if match[0] in row:
                if not match[1] in row:
                    row.append(match[1])

            else:
                board.append(row)
                row = match

        # To add the last row
        board.append(row)

        # Sort rows by X to ensure proper sequence
        for row in board:
            row.sort(key=lambda filler:filler[0])

        return board


    def check_if_word_letter(self, rect1, rect2):
        # Get the center of both rectangles
        r1_center = [rect1[0] + (rect1[2] / 2), rect1[1] + (rect1[3] / 2)]
        r2_center = [rect2[0] + (rect2[2] / 2), rect2[1] + (rect2[3] / 2)]

        # Return if it's in range of eachother with the letter spacing
        return r1_center[0] - self.lsr <= r2_center[0] <= r1_center[0] + self.lsr and r1_center[1] - self.lsr <= r2_center[1] <= r1_center[1] + self.lsr


    def check_if_horizontal_match(self, rect1, rect2):
        # Corners of the rectangle (left)
        r1_corner = [rect1[1], rect1[1] + rect1[3]]
        r2_range = range(rect2[1], rect2[1] + rect2[3])

        # Return if it's in the range of the other rectangle's y 
        return r1_corner[0] in r2_range or r1_corner[1] in r2_range


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

        # Reverse for convenience
        segments = list(reversed(segments))

        return segments

    # Visualise the contours onto the image
    def visualise(self, image, contours):
        for idx, contour in enumerate(contours):
            x, y, w, h = contour
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
            #cv2.putText(self.image, str(idx), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)

        cv2.imshow("img", image)
        cv2.waitKey()