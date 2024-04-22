from copy import deepcopy

def solve_sudoku(grid):
    empty_cells = find_empty_cell(grid)

    stack = [(grid, empty_cells)]
    while stack:
        current_grid, empty_cells = stack.pop()
        if empty_cells == []:
            return current_grid
        for i, j in empty_cells:
            possible_values = heuristic(current_grid, i, j, 0)
            for val in possible_values:
                new_grid = deepcopy(current_grid)
                new_grid[i][j] = val
                new_empty_cells = deepcopy(empty_cells)
                new_empty_cells.remove((i, j))
                stack.append((new_grid, new_empty_cells))
        

    return [[0] * 9 for _ in range(9)]


def find_empty_cell(grid):
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                empty_cells.append((i, j))

    return empty_cells

def heuristic(grid, row, col, num):
    rem_val = set()
    
    for i in range(9):
        if grid[row][i] == num:
            rem_val.add(num)

    for i in range(9):
        if grid[i][col] == num:
            rem_val.add(num)

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                rem_val.add(num)

    return set(range(1, 10)) - rem_val

def print_board(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j], end=" ")
        print()

def solve_sudoku_wrapper(board):
    # solve_sudoku(board)
    # print("Solved Sudoku:")
    # print_board(board)
    print_board(solve_sudoku(board))

if __name__ == "__main__":
    board = [
        [8, 2, 0, 0, 0, 0, 3, 0, 6], 
    [9, 0, 0, 0, 2, 0, 1, 0, 0],
    [3, 4, 0, 0, 8, 0, 0, 5, 2],
    [5, 0, 3, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 5, 0, 3, 0, 0, 9],
    [6, 0, 0, 0, 0, 0, 4, 3, 0],
    [0, 0, 0, 2, 0, 5, 0, 0, 4],
    [0, 5, 4, 0, 0, 0, 0, 0, 0],
    [2, 3, 9, 8, 4, 1, 5, 6, 7]
    ]

    solve_sudoku_wrapper(board)