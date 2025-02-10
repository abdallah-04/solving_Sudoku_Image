import cv2
import numpy as np
import pytesseract
from PIL import Image
from dotenv import load_dotenv,dotenv_values
import os
load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv("OCR_TH")

img_path = os.getenv("IMG_pATH")
img = cv2.imread(img_path)

if img is None:
    raise ValueError("Failed to load image. Check the file path or format!")

# Resize image
img = cv2.resize(img, (500, 500), interpolation=cv2.INTER_CUBIC)
#cv2.imshow('Original Image', img)

# Convert to grayscale and threshold
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

# Detect grid lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))

vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

grid_lines = cv2.add(vertical_lines, horizontal_lines)
#cv2.imshow('Detected Grid Lines', grid_lines)

# Remove grid lines using inpainting
mask = cv2.bitwise_not(grid_lines)
result = cv2.inpaint(img, grid_lines, 3, cv2.INPAINT_TELEA)
#cv2.imshow("Image Without Grid Lines", result)

# Convert to grayscale for OCR
result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
result_gray = cv2.GaussianBlur(result_gray, (3, 3), 0)
_, result_gray = cv2.threshold(result_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#cv2.imshow('Processed for OCR', result_gray)

# Define the size of each Sudoku cell
cell_size = result_gray.shape[0] // 9  # Assuming a 9x9 Sudoku grid

# Iterate over the grid and crop each cell
sudoku_grid = []
for y in range(0, result_gray.shape[0], cell_size):  # Rows
    row = []
    for x in range(0, result_gray.shape[1], cell_size):  # Columns
        # Crop the cell
        cell = result_gray[y:y + cell_size, x:x + cell_size]

        # Perform OCR on the cell
        try:
            ocr_result = pytesseract.image_to_string(cell, config='--psm 10')  # PSM 10 for single character
            ocr_result = ocr_result.strip()  # Remove whitespace
            if ocr_result.isdigit():  # Check if the result is a digit
                row.append(int(ocr_result))
            else:
                row.append(0)  # Empty cell
        except Exception as e:
            print(f"OCR failed for cell at ({x}, {y}): {e}")
            row.append(0)  # Assume empty cell if OCR fails

        
        cv2.waitKey(100)  

    sudoku_grid.append(row)

# Print the Sudoku grid
sudoku_grid = [row[:-1] for row in sudoku_grid[:-1]]

print("Sudoku Grid:")
for row in sudoku_grid:
    print(row)

cv2.waitKey(0)
cv2.destroyAllWindows()
