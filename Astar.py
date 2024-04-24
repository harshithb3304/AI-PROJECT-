import numpy as np
from copy import deepcopy
import heapq

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
def position_heuristic(min_grid, zero_index, sudoku_puzzle):
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

# Overall heuristic function
def heuristic(sudoku_puzzle):
    min_grid, zero_index = sub_grid_heuristic(sudoku_puzzle)
    return position_heuristic(min_grid, zero_index, sudoku_puzzle)

# Function to count the number of zeros in the sudoku puzzle
def count_zeros(sudoku_puzzle):
    return np.count_nonzero(sudoku_puzzle == 0)

# Function to calculate the cost for A* algorithm
def cost(node):
    return 1

# Function to generate next states
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

# A* Algorithm
def astar(sudoku_puzzle):
    opened = []
    closed = set()

    heapq.heappush(opened, (0, sudoku_puzzle))
    count = 0

    while opened:
        cost , current_state = heapq.heappop(opened)
        count += 1
        current_state_tuple = tuple(map(tuple, current_state))
        closed.add(current_state_tuple)

        # Termination condition 
        if count_zeros(current_state) == 0:
            print("Total number of iterations: ", count)
            return current_state

        # Find the target position to be explored
        target = heuristic(current_state)
        
        # Generate the next states
        next_states = gen_next_state(target, current_state)

        # Add the next states to the opened list if it is not already explored
        for next_state in next_states:
            next_state_tuple = tuple(map(tuple, next_state))
            if next_state_tuple not in closed:
                heapq.heappush(opened, (cost + 1, next_state))

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
])

print("Number of empty spaces: ", count_zeros(sudoku_puzzle))
solution_path = astar(sudoku_puzzle)
print(solution_path)
