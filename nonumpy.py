import numpy as np
from copy import deepcopy

def sub_grid_heuristic(sudoku_puzzle):
    current_state = deepcopy(sudoku_puzzle)
    n = len(sudoku_puzzle)
    zero_count = [0 for _ in range(n)]
    zero_index = [[] for _ in range(n)]

    root = int(n ** 0.5)

    for i in range(n):
        for j in range(n):
            if current_state[i][j] == 0:
                subgrid = (i // root) * root + j // root
                zero_count[subgrid] += 1
                zero_index[subgrid].append((i, j))

    for i in range(n):
        if zero_count[i] == 0:
            zero_count[i] = n * n  # Set to a large value if no zero found in subgrid

    min_count = min(zero_count)
    min_indices = [i for i, count in enumerate(zero_count) if count == min_count]

    return min_indices, zero_index

def position_heuristic(min_grid, zero_index):
    next_position = ()
    max_count = 0

    for i in min_grid:
        for j in zero_index[i]:
            row, col = j
            count = sum(1 for x in range(len(sudoku_puzzle)) if sudoku_puzzle[row][x] != 0)
            count += sum(1 for x in range(len(sudoku_puzzle)) if sudoku_puzzle[x][col] != 0)

            if max_count <= count:
                max_count = count
                next_position = j

    return next_position

def heuristic(sudoku_puzzle):
    min_grid, zero_index = sub_grid_heuristic(sudoku_puzzle)
    return position_heuristic(min_grid, zero_index)

def gen_next_state(target, sudoku_puzzle):
    if not target:
        return []

    row, col = target
    n = len(sudoku_puzzle)
    root = int(n ** 0.5)
    subgrid_row, subgrid_col = (row // root * root, col // root * root)
    sub_grid = sudoku_puzzle[subgrid_row:subgrid_row + root, subgrid_col:subgrid_col + root]

    values = np.isin(np.arange(1, n + 1), sub_grid).astype(int)
    values += np.isin(np.arange(1, n + 1), sudoku_puzzle[row, :]).astype(int)
    values += np.isin(np.arange(1, n + 1), sudoku_puzzle[:, col]).astype(int)

    possible_values = np.where(values == 0)[0] + 1
    next_states = []

    for i in possible_values:
        next_state = deepcopy(sudoku_puzzle)
        next_state[row, col] = i
        next_states.append(next_state)

    return next_states

def count_zeros(sudoku_puzzle):
    return np.count_nonzero(sudoku_puzzle == 0)

def dfs(sudoku_puzzle):
    opened = []
    closed = set()

    opened.append(sudoku_puzzle)
    count = 0

    while opened:
        current_state = opened.pop()
        count+=1
        current_state_tuple = tuple(map(tuple, current_state))
        closed.add(current_state_tuple)

        if count_zeros(current_state) == 0:
            print("Totol number of iterations : ", count)
            return current_state

        target = heuristic(current_state)
        print(target)
        next_states = gen_next_state(target, current_state)

        for next_state in next_states:
            next_state_tuple = tuple(map(tuple, next_state))
            if next_state_tuple not in closed:
                opened.append(next_state)

    return "No solution found"

# Example 4x4 Sudoku
sudoku_puzzle = np.array([
    [0, 0, 0, 5, 4, 0, 0, 7, 8],
    [0, 0, 9, 0, 0, 3, 6, 4, 0],
    [5, 4, 6, 0, 7, 9, 0, 0, 0],
    [0, 2, 4, 0 ,0 ,0, 7, 0, 0],
    [0, 0, 7, 1, 2, 0, 5, 0, 0],
    [6, 0, 0, 9, 8, 0, 4, 2, 0],
    [0, 0, 0, 0, 0, 8, 1, 0, 3],
    [3, 5, 0, 4, 0, 0, 8, 9, 0],
    [7, 9, 0, 3, 5, 1, 0, 0, 0]
]
)

print("Number of empty spaces : ", count_zeros(sudoku_puzzle))
solution_path = dfs(sudoku_puzzle)
print(solution_path)