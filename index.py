import numpy as np
from copy import deepcopy

sudoku_puzzle = [
    [0, 7, 0, 0, 2, 0, 0, 4, 6],
    [0, 6, 0, 0, 0, 0, 8, 9, 0],
    [2, 0, 0, 8, 0, 0, 7, 1, 5],
    [0, 8, 4, 0 ,9 ,7, 0, 0, 0],
    [7, 1, 0, 0, 0, 0, 0, 5, 9],
    [0, 0, 0, 1, 3, 0, 4, 8, 0],
    [6, 9, 7, 0, 0, 2, 0, 0, 8],
    [0, 5, 8, 0, 0, 0, 0, 6, 0],
    [4, 3, 0, 0, 8, 0, 0, 7, 0]
]

sudoku_puzzle = np.array(sudoku_puzzle)

def sub_grid_heuristic(sudoku_puzzle):
    current_state = deepcopy(sudoku_puzzle)
    zero_count = [0 for i in range(len(sudoku_puzzle))]
    zero_count = np.array(zero_count)
    zero_index =[[] for i in range(len(sudoku_puzzle))]

    for i in range(len(sudoku_puzzle)):
        for j in range(len(sudoku_puzzle)):
            if current_state[i][j] == 0:
                root = int(len(sudoku_puzzle)**0.5)
                if (i//root == 0 and j//root == 0):
                    zero_count[0] +=1
                    zero_index[0].append((i, j))
                elif (i//root == 1 and j//root == 0):
                    zero_count[1] +=1
                    zero_index[1].append((i, j))
                elif (i//root == 2 and j//root == 0):
                    zero_count[2] +=1
                    zero_index[2].append((i, j))
                elif( i//root == 0 and j//root == 1):
                    zero_count[3] +=1
                    zero_index[3].append((i, j))
                elif (i//root == 1 and j//root == 1):
                    zero_count[4] +=1
                    zero_index[4].append((i, j))
                elif (i//root == 2 and j//root == 1):
                    zero_count[5] +=1
                    zero_index[5].append((i, j))
                elif (i//root == 0 and j//root == 2):
                    zero_count[6] +=1
                    zero_index[6].append((i, j))
                elif (i//root == 1 and j//root == 2):
                    zero_count[7] +=1
                    zero_index[7].append((i, j))
                elif (i//root == 2 and j//root == 2):
                    zero_count[8] +=1
                    zero_index[8].append((i, j))

    for i in range(len(sudoku_puzzle)):
        if zero_count[i] == 0:
            zero_count[i] = 999

    search_key = min(zero_count)
    item_index = np.where(zero_count == search_key)[0]

    return item_index, zero_index

def position_heuristic(min_grid, zero_index):
    next_position = ()
    max_count = 0
    for i in min_grid:
        for j in zero_index[i]:
            row, col = j
            count = 0
            for x in range(len(sudoku_puzzle)):
                if sudoku_puzzle[row][x] != 0:
                    count += 1
                if sudoku_puzzle[x][col] != 0:
                    count += 1
            if max_count <= count:
                max_count = count
                next_position = j
    return next_position

def heuristic(sudoku_puzzle):
    min_grid, zero_index = sub_grid_heuristic(sudoku_puzzle)
    target = position_heuristic(min_grid, zero_index)
    # print(target)
    return target

def gen_next_state(target, sudoku_puzzle):
    if target == ():
        return []
    row,col = target

    root = int(len(sudoku_puzzle)**0.5)
    subgrid_row, subgrid_col = (row//root * root, col//root * root)

    sub_grid = sudoku_puzzle[subgrid_row:subgrid_row+2, subgrid_col:subgrid_col+2]

    values = np.isin([i + 1 for i in range(len(sudoku_puzzle))], sub_grid).astype(int)
    values += np.isin([i + 1 for i in range(len(sudoku_puzzle))], sudoku_puzzle[row,:]).astype(int)
    values += np.isin([i + 1 for i in range(len(sudoku_puzzle))], sudoku_puzzle[:,col]).astype(int)

    possible_values = np.where(values == 0)[0] + 1
    next_states = []

    for i in possible_values:
        next_state = deepcopy(sudoku_puzzle)
        next_state[row,col] = i
        next_states.append(next_state)
    return next_states

def count_zeros(sudoku_puzzle):
    num_zeros = np.count_nonzero(sudoku_puzzle == 0)
    return num_zeros

def dfs(sudoku_puzzle):
    opened = []
    closed = []

    opened.append(sudoku_puzzle)
    count = 0
    while opened:
        print(count) if count%100 == 0 else None
        count += 1
        current_state = opened.pop(0)
        # print(current_state)
        closed.append(current_state)
        if count_zeros(current_state) == 0:
            print("Number of iterations: ",count)
            return current_state
        target = heuristic(current_state)
        next_states = gen_next_state(target, current_state)
        for next_state in next_states:
            if not any(np.array_equal(next_state, state) for state in closed):
                opened.append(next_state)
    return "No solution found"

sudoku_puzzle = dfs(sudoku_puzzle)
print(sudoku_puzzle, sep = '\n')