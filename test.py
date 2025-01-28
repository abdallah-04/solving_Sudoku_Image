import cv2
import numpy as np
import pytesseract
from PIL import Image

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the image
img_path = r"C:\my_python_project\solving_Sudoku_Image\Sudoku_Puzzle_by_L2G-20050714_standardized_layout.svg.png"
img = cv2.imread(img_path)

if img is None:
    raise ValueError("Failed to load image. Check the file path or format!")

# Resize image
img = cv2.resize(img, (400, 400), interpolation=cv2.INTER_CUBIC)
cv2.imshow('Original Image', img)

# Convert to grayscale and threshold
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

# Detect grid lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))

vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

grid_lines = cv2.add(vertical_lines, horizontal_lines)
cv2.imshow('Detected Grid Lines', grid_lines)

# Remove grid lines using inpainting
mask = cv2.bitwise_not(grid_lines)
result = cv2.inpaint(img, grid_lines, 3, cv2.INPAINT_TELEA)
cv2.imshow("Image Without Grid Lines", result)

# Convert to grayscale for OCR
result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
result_gray = cv2.GaussianBlur(result_gray, (3, 3), 0)
_, result_gray = cv2.threshold(result_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imshow('Processed for OCR', result_gray)

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

        # Display the cell (optional)
        #cv2.imshow(f'Cell at ({x}, {y})', cell)
        cv2.waitKey(100)  # Wait for 100ms to show each cell

    sudoku_grid.append(row)

# Print the Sudoku grid
print("Sudoku Grid:")
for row in sudoku_grid:
    print(row)

cv2.waitKey(0)
cv2.destroyAllWindows()