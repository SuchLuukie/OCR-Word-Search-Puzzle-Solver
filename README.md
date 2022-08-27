# OCR Word search puzzle solver
 Creating a model that uses OCR to detect word search puzzles and solves them.
 (Using tesseract https://github.com/UB-Mannheim/tesseract/wiki)


# Planning
* Input <br>
    Building and using OCR (Optical Character Recognition) model to derive a word search puzzle from an image.

* Solver <br>
    Creating an algorithm to scan the word search puzzle looking for the given words inside the puzzle.

* Remaining letters <br>
    Some word search puzzles contain a sentence or word within the remaining/unused letters in the puzzle.
    Another algorithm is needed to try and solve that list of randomised letters.


# Tasks
* Input
    * Get bounding boxes of the letters and process them
    * Turn the search puzzle into 2D array
    * Turn the given words into 1D array
    
* OCR
    * Use the images from the input and treshold them
    * Apply some post processing to ensure higher quality results
    * Use the OCR model (Tesseract) to identify the letters

* Solver
    * TODO

# What I've learned
I'm currently postboning this project, I've tweaked and worked on the OCR and image proccesing side of this and currently in this state it's not accurate enough to start solving word search puzzles with it. I've learned quite a bit on image processing using contrats, tresholds, etc.

I'll be working on the puzzle solving side of things on a different repository. 


# What the script extracts. This is what the OCR model receives, the model is not accurate enough to proceed with this project.
<img src="/showcase/showcase.png" width="360" height="240"/>