# Sudoku Solver with OCR

This project detects and extracts a Sudoku puzzle from an image using OpenCV and Tesseract OCR, then solves the Sudoku puzzle using a backtracking algorithm.

## Features

- Detects and removes grid lines from the Sudoku image.
- Uses OCR to extract numbers from the Sudoku grid.
- Implements a backtracking algorithm to solve the Sudoku puzzle.
- Displays the original image and the solved Sudoku grid.

## Requirements

Ensure you have the following installed:

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Tesseract OCR
- Pillow
- python-dotenv

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/sudoku-ocr-solver.git
   cd sudoku-ocr-solver
   ```
2. Install dependencies:
   ```sh
   pip install opencv-python numpy pytesseract pillow python-dotenv
   ```
3. Set up environment variables:
   - Create a `.env` file in the project root with the following variables:
     ```env
     OCR_TH="C:/Program Files/Tesseract-OCR/tesseract.exe"
     IMG_pATH="path/to/your/sudoku/image.jpg"
     ```
   - Update the paths according to your system.

## Usage

Run the script to detect and solve the Sudoku puzzle:

```sh
python sudoku_solver.py
```

## Explanation

1. **Image Preprocessing**:

   - Converts the image to grayscale.
   - Applies thresholding to enhance contrast.
   - Detects and removes grid lines.

2. **OCR Extraction**:

   - Each cell is processed separately using Tesseract OCR.
   - Non-digit values are replaced with 0 (empty cell).

3. **Solving Sudoku**:

   - Uses a backtracking algorithm to fill in missing numbers.

4. **Displaying Results**:

   - The original image is displayed.
   - The solved Sudoku grid is visualized and displayed.

## Example Output

```
Sudoku Grid Before Solving:
[[5, 3, 0, 0, 7, 0, 0, 0, 0],
 [6, 0, 0, 1, 9, 5, 0, 0, 0],
 [...]]

Sudoku Grid After Solving:
[[5, 3, 4, 6, 7, 8, 9, 1, 2],
 [6, 7, 2, 1, 9, 5, 3, 4, 8],
 [...]]
```

## Notes

- Ensure Tesseract is installed and its path is correctly set.
- OCR might misread numbers; tweaking preprocessing steps can improve accuracy.

## License

This project is licensed under the MIT License.

