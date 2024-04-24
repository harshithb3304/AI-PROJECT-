import numpy as np
from copy import deepcopy

# Function to check if the sudoku puzzle is valid
def valid_sudoku(sudoku_puzzle):
    n = len(sudoku_puzzle)
    root = int(n ** 0.5)

    # Check if elements in the row and column are unique
    for i in sudoku_puzzle:
        for j in i:
            if j != 0 and np.sum(i == j) > 1:
                return False
            
    # Check if elements in the subgrid are unique
    for i in range(0, n, root):
        for j in range(0, n, root):
            subgrid = sudoku_puzzle[i:i + root, j:j + root].flatten()
            for k in subgrid:
                if k != 0 and np.sum(subgrid == k) > 1:
                    return False
    
    return True

# Heuristic function to find the sub_grid to be explored
def sub_grid_heuristic(sudoku_puzzle):
    current_state = deepcopy(sudoku_puzzle)
    n = len(sudoku_puzzle)
    zero_count = [0 for _ in range(n)]
    zero_index = [[] for _ in range(n)]

    root = int(n ** 0.5)

    # Count the number of zeros in each subgrid
    for i in range(n):
        for j in range(n):
            if current_state[i][j] == 0:
                subgrid = (i // root) * root + j // root
                zero_count[subgrid] += 1
                zero_index[subgrid].append((i, j))

    # Set the count to a large value if the subgrid is filled
    for i in range(n):
        if zero_count[i] == 0:
            zero_count[i] = n * n 

    # Find the subgrids with minimum number of zeros
    min_count = min(zero_count)
    min_indices = [i for i, count in enumerate(zero_count) if count == min_count]

    return min_indices, zero_index

# Heuristic function to find the position to be explored
def position_heuristic(min_grid, zero_index):
    next_position = ()
    max_count = 0

    # Find the position with maximum number of constraints hence minimum number of possible branches
    for i in min_grid:
        for j in zero_index[i]:
            row, col = j
            
            # Count the number of non-zero elements in the row, column and subgrid
            count = sum(1 for x in range(len(sudoku_puzzle)) if sudoku_puzzle[row][x] != 0)
            count += sum(1 for x in range(len(sudoku_puzzle)) if sudoku_puzzle[x][col] != 0)
            count += sum(1 for x in range(len(sudoku_puzzle)) if sudoku_puzzle[row // 3 * 3 + x // 3][col // 3 * 3 + x % 3] != 0)

            if max_count <= count:
                max_count = count
                next_position = j

    return next_position

#overall heuristic function
def heuristic(sudoku_puzzle):
    min_grid, zero_index = sub_grid_heuristic(sudoku_puzzle)
    return position_heuristic(min_grid, zero_index)

#function to generate next states
def gen_next_state(target, sudoku_puzzle):
    if not target:
        return []

    # Find the subgrid of the target position
    row, col = target
    n = len(sudoku_puzzle)
    root = int(n ** 0.5)
    subgrid_row, subgrid_col = (row // root * root, col // root * root)
    sub_grid = sudoku_puzzle[subgrid_row:subgrid_row + root, subgrid_col:subgrid_col + root]

    # Values that are already present in the row, column and subgrid
    values = np.isin(np.arange(1, n + 1), sub_grid).astype(int)
    values += np.isin(np.arange(1, n + 1), sudoku_puzzle[row, :]).astype(int)
    values += np.isin(np.arange(1, n + 1), sudoku_puzzle[:, col]).astype(int)

    # Possible values that can be placed in the target position
    possible_values = np.where(values == 0)[0] + 1
    next_states = []

    # Generate the next states
    for i in possible_values:
        next_state = deepcopy(sudoku_puzzle)
        next_state[row, col] = i
        next_states.append(next_state)

    return next_states

# Function to count the number of zeros in the sudoku puzzle
def count_zeros(sudoku_puzzle):
    return np.count_nonzero(sudoku_puzzle == 0)

# Depth First Search Algorithm
def dfs(sudoku_puzzle):
    opened = []
    closed = set()
    path = []
    count = 0
    i = 0
    opened.append(sudoku_puzzle)    

    while opened:
        current_state = opened.pop()
        count+=1
        current_state_tuple = tuple(map(tuple, current_state))
        closed.add(current_state_tuple)

        # Termination condition 
        if count_zeros(current_state) == 0:
            print("Totol number of iterations : ", count)
            return current_state, path

        # Find the target position to be explored
        target = heuristic(current_state)
        if(target in path):
            path.remove(target)
            path.append(target)
        else:
            path.append(target)
        
        # Generate the next states
        next_states = gen_next_state(target, current_state)       

        next_state_tuple = ()
        # Add the next states to the opened list if it is not already explored
        for next_state in next_states:
            next_state_tuple = tuple(map(tuple, next_state))
            if next_state_tuple not in closed:
                opened.append(next_state)
        
        # if next_state_tuple == ():
        #     continue
        
        # i += 1
        # next_state_tuple = np.array(next_state_tuple)
        # current_state_tuple = np.array(current_state_tuple)
        # pos = np.where(next_state_tuple != current_state_tuple)
        # print(i, pos)

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

None if valid_sudoku(sudoku_puzzle) else exit("Invalid Sudoku Puzzle")

print("Number of empty spaces : ", count_zeros(sudoku_puzzle))
solution, solution_path = dfs(sudoku_puzzle)
print(solution)
print(len(solution_path))
print(solution_path)