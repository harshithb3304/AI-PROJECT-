def solve_sudoku(grid):
    row, col = find_empty_cell(grid)
    if row == -1:
        return True

    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row][col] = num

            if solve_sudoku(grid):
                return True

            grid[row][col] = 0

    return False

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)

    return (-1, -1)

def is_safe(grid, row, col, num):
    # Check if the number is already in the current row
    for i in range(9):
        if grid[row][i] == num:
            return False

    # Check if the number is already in the current column
    for i in range(9):
        if grid[i][col] == num:
            return False

    # Check if the number is already in the current 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

def print_board(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j], end=" ")
        print()

def solve_sudoku_wrapper(board):
    solve_sudoku(board)
    print("Solved Sudoku:")
    print_board(board)

if __name__ == "__main__":
    board = [
        [0, 0, 0, 0, 0, 0, 5, 0, 0],
    [6, 0, 5, 0, 9, 0, 3, 2, 8],
    [0, 4, 3, 0, 2, 8, 0, 1, 6],
    [3, 7, 0, 1 ,0 ,0, 0, 9, 4],
    [4, 5, 2, 9, 8, 0, 1, 6, 0],
    [1, 9, 0, 0, 0, 6, 0, 0, 2],
    [0, 2, 0, 0, 7, 9, 0, 0, 0],
    [0, 3, 7, 0, 0, 5, 0, 0, 1],
    [5, 6, 0, 0, 3, 0, 2, 0, 9] 
    ]

    solve_sudoku_wrapper(board)