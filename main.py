from opencv import sudoku_grid,grid_lines,img
import numpy as np
import cv2 
def find_next_emty(sudoku_grid):
    for r in range(9):
        for c in range(9):
            if sudoku_grid[r][c] == 0:
                return r, c
    return None, None

def is_valid(sudoku_grid, row, col, guess):
    row_vals = sudoku_grid[row]
    if guess in row_vals:
        return False
    
    col_vals = [sudoku_grid[i][col] for i in range(9)]
    if guess in col_vals:
        return False
    
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if sudoku_grid[r][c] == guess:
                return False
    return True

def solve_sudoku(sudoku_grid):
    row, col = find_next_emty(sudoku_grid)
    if row is None:
        return True
    for guess in range(1, 10):
        if is_valid(sudoku_grid, row, col, guess):
            sudoku_grid[row][col] = guess
            if solve_sudoku(sudoku_grid):
                return True
            sudoku_grid[row][col] = 0
    return False


solve_sudoku(sudoku_grid)

blank = np.zeros((500, 500, 3), dtype='uint8')
blank=cv2.bitwise_not(grid_lines)


for i in range(9):
    for j in range(9):
        cv2.putText(
            img=blank,
            text=str(sudoku_grid[i][j]),
            org=(j*55 + 20, i*55 + 40),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 0, 0),  
            thickness=2
        )

cv2.imshow('sudoku after solving', blank)
cv2.imshow('sudoku', img)



cv2.waitKey(0)
cv2.destroyAllWindows()