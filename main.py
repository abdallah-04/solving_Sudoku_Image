import cv2
import numpy as np
import pytesseract
from PIL import Image

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the image
img_path = r"C:\my_python_project\Sudoku_Puzzle_by_L2G-20050714_standardized_layout.svg.png"
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

# Draw grid lines (for visualization)
img_c = result_gray.copy()
for x in range(0, img_c.shape[1], 45):  # Vertical lines
    cv2.line(img_c, (x, 0), (x, img_c.shape[0]), (36, 255, 12), thickness=5)
for y in range(0, img_c.shape[0], 45):  # Horizontal lines
    cv2.line(img_c, (0, y), (img_c.shape[1], y), (36, 255, 12), thickness=5)

cv2.imshow('Grid Overlay', img_c)

# Perform OCR
try:
    ocr_result = pytesseract.image_to_string(result_gray, config='--psm 6')
    print("OCR Result:\n", ocr_result)
except Exception as e:
    print(f"OCR failed: {e}")

cv2.waitKey(0)
cv2.destroyAllWindows()
