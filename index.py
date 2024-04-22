import numpy as np
from copy import deepcopy

sudoku_puzzle = [
    [0, 0, 0, 0],
    [0, 0, 3, 0],
    [4, 0, 2, 1],
    [0, 2, 0, 0]
]

sudoku_puzzle = np.array(sudoku_puzzle)

def sub_grid_heuristic(sudoku_puzzle):
    current_state = deepcopy(sudoku_puzzle)
    zero_count = [0,0,0,0]
    zero_count = np.array(zero_count)
    zero_index =[[],[],[],[]]

    for i in range(4):
        for j in range(4):
            if (i//2 == 0 and j//2 ==0 and current_state[i][j]==0):
                zero_count[0] +=1
                zero_index[0].append((i, j))
            elif (i//2 == 1 and j//2 ==0 and current_state[i][j]==0):
                zero_count[1] +=1
                zero_index[1].append((i, j))
            elif( i//2 == 0 and j//2 == 1 and current_state[i][j] == 0):
                zero_count[2] +=1
                zero_index[2].append((i, j))
            elif( i//2 == 1 and j//2 == 1 and current_state[i][j] == 0):
                zero_count[3] +=1
                zero_index[3].append((i, j))

    for i in range(4):
        if zero_count[i] == 0:
            zero_count[i] = 999

    search_key = min(zero_count)
    item_index = np.where(zero_count == search_key)[0]
    # print(item_index)

    # for i in item_index:
    #     subgrid_row, subgrid_col = (i//2 * 2, i%2 * 2)
    #     for i in range(subgrid_row, subgrid_row + 2):
    #         for j in range(subgrid_col, subgrid_col + 2):
    #             print(current_state[i][j], end=" ")
    #         print()


    return item_index, zero_index

def position_heuristic(min_grid, zero_index):
    next_position = ()
    max_count = 0
    for i in min_grid:
        for j in zero_index[i]:
            row, col = j
            count = 0
            for x in range(4):
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
    print(target)
    return target

def gen_next_state(target, sudoku_puzzle):
    row,col = target

    subgrid_row, subgrid_col = (row//2 * 2, col//2 * 2)

    sub_grid = sudoku_puzzle[subgrid_row:subgrid_row+2, subgrid_col:subgrid_col+2]

    values = np.isin([1, 2, 3, 4], sub_grid).astype(int)
    values += np.isin([1, 2, 3, 4], sudoku_puzzle[row,:]).astype(int)
    values += np.isin([1, 2, 3, 4], sudoku_puzzle[:,col]).astype(int)

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
        count += 1
        current_state = opened.pop()
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
    print(current_state)
    return "No solution found"

sudoku_puzzle = dfs(sudoku_puzzle)
print(sudoku_puzzle, sep = '\n')

