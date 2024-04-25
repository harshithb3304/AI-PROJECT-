import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

prob = [    
    [
        [0, 0, 0, 5, 4, 0, 0, 7, 8],      
        [0, 0, 9, 0, 0, 3, 6, 4, 0],
        [5, 4, 6, 0, 7, 9, 0, 0, 0],    #easy
        [0, 2, 4, 0 ,0 ,0, 7, 0, 0],
        [0, 0, 7, 1, 2, 0, 5, 0, 0],
        [6, 0, 0, 9, 8, 0, 4, 2, 0],
        [0, 0, 0, 0, 0, 8, 1, 0, 3],
        [3, 5, 0, 4, 0, 0, 8, 9, 0],
        [7, 9, 0, 3, 5, 1, 0, 0, 0]     
    ],
    [
        [0, 0, 7, 2, 8, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 5, 0, 6],     #medium
        [4, 1, 3, 0, 0, 6, 0, 8, 0],
        [7, 2, 0, 3, 9, 0, 0, 0, 0],
        [3, 4, 0, 0, 0, 0, 8, 1, 0],
        [6, 8, 0, 1, 0, 7, 0, 0, 2],
        [0, 0, 0, 6, 7, 4, 0, 2, 3],
        [0, 0, 0, 0, 0, 5, 7, 0, 0],
        [1, 0, 6, 0, 2, 3, 0, 4, 0]
    ],
    [
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [3, 0, 0, 2, 0, 9, 6, 0, 0],
        [0, 7, 0, 5, 0, 0, 0, 1, 0],    #hard
        [1, 6, 0, 4 ,0 ,7, 5, 8, 0],
        [0, 5, 4, 6, 0, 0, 7, 0, 2],
        [7, 2, 0, 0, 0, 5, 0, 0, 6],
        [0, 0, 0, 0, 0, 8, 2, 0, 0],
        [0, 9, 0, 1, 0, 0, 4, 3, 0],
        [2, 0, 1, 7, 5, 4, 0, 6, 0] 
    ],    
    [
        [0, 4, 3, 9, 0, 0, 0, 0, 8],        #evil
        [0, 0, 0, 0, 8, 6, 1, 4, 3],
        [0, 1, 0, 0, 3, 4, 0, 0, 0],
        [6, 0, 8, 4, 0, 0, 0, 2, 0],
        [4, 3, 0, 0, 0, 2, 8, 9, 6],
        [0, 0, 1, 0, 0, 8, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 0],
        [7, 0, 2, 0, 0, 3, 0, 0, 0],
        [0, 0, 4, 0, 9, 0, 2, 0, 0]
    ],
    [
        [7, 0, 0, 0, 0, 5, 0, 0, 0],        #incorrect
        [7, 0, 0, 0, 6, 0, 0, 0, 2],
        [9, 0, 0, 0, 0, 0, 0, 0, 5],
        [6, 3, 9, 0, 2, 7, 0, 0, 1],
        [0, 7, 0, 0, 0, 0, 2, 0, 3],
        [0, 0, 0, 1, 0, 0, 9, 0, 0],
        [5, 0, 0, 0, 3, 0, 1, 0, 4],
        [0, 0, 0, 0, 0, 4, 0, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [0,3,0,0],
        [0,2,0,3],                      #easy
        [2,0,0,0],
        [3,0,2,0]
    ],
    [
        [3,0,0,0],                      #medium
        [1,0,0,0],
        [4,0,0,0],
        [0,1,0,3]
    ],
    [
        [0,0,0,0],                      #hard
        [2,1,0,4],
        [0,2,0,0],
        [0,3,0,2]
    ],
    [
        [0,0,2,0],                      #evil
        [0,0,3,0],
        [3,0,0,0],
        [0,0,0,3]
    ],
    [
        [3,0,0,0],                      #invalid
        [1,0,0,0],
        [4,0,0,0],
        [0,1,1,3]
    ],    
    [
        [0, 2, 0, 0, 5, 0, 7, 8, 0, 0, 11, 0, 0, 14, 15, 0],
        [9, 0, 0, 12, 13, 14, 15, 0, 1, 0, 0, 4, 0, 6, 7, 8],
        [5, 6, 0, 0, 1, 0, 3, 4, 0, 14, 0, 16, 9, 0, 11, 12],
        [13, 14, 15, 0, 9, 0, 0, 0, 5, 6, 7, 8, 0, 2, 3, 0],
        [3, 0, 1, 2, 7, 0, 0, 6, 0, 12, 9, 0, 0, 0, 13, 0],
        [11, 12, 9, 0, 0, 0, 0, 14, 3, 4, 1, 2, 7, 0, 5, 6],
        [7, 8, 5, 0, 11, 12, 9, 0, 0, 0, 13, 0, 0, 4, 0, 0],
        [15, 0, 0, 14, 3, 4, 1, 2, 7, 8, 5, 6, 11, 12, 9, 0],
        [2, 1, 0, 0, 6, 0, 8, 7, 0, 9, 0, 11, 14, 13, 16, 0],
        [0, 9, 0, 0, 0, 13, 0, 0, 2, 1, 4, 3, 6, 5, 0, 7],
        [6, 5, 0, 7, 0, 9, 0, 11, 0, 0, 16, 0, 2, 1, 4, 3],
        [0, 0, 16, 0, 2, 1, 4, 3, 6, 5, 8, 7, 0, 9, 12, 11],
        [4, 3, 2, 0, 8, 7, 6, 5, 0, 0, 0, 9, 16, 15, 14, 0],
        [0, 0, 0, 9, 0, 0, 0, 0, 4, 3, 0, 1, 0, 7, 6, 5],
        [8, 7, 0, 5, 12, 11, 0, 9, 16, 15, 0, 13, 4, 3, 2, 1],
        [0, 15, 14, 13, 4, 0, 2, 1, 8, 0, 6, 5, 12, 11, 0, 9]
    ]
]

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
def position_heuristic(min_grid, zero_index, sudoku_puzzle):
    next_position = ()
    max_count = 0

    # Find the position with maximum number of constraints hence minimum number of possible branches
    for i in min_grid:
        for j in zero_index[i]:
            row, col = j
            n = len(sudoku_puzzle)
            root = int(n ** 0.5)
            
            # Count the number of non-zero elements in the row, column and subgrid
            count = sum(1 for x in range(len(sudoku_puzzle)) if sudoku_puzzle[row][x] != 0)
            count += sum(1 for x in range(len(sudoku_puzzle)) if sudoku_puzzle[x][col] != 0)
            count += sum(1 for x in range(len(sudoku_puzzle)) if sudoku_puzzle[row // root * root + x // root][col // root * root + x % root] != 0)

            if max_count <= count:
                max_count = count
                next_position = j

    return next_position

#overall heuristic function
def heuristic(sudoku_puzzle):
    min_grid, zero_index = sub_grid_heuristic(sudoku_puzzle)
    return position_heuristic(min_grid, zero_index, sudoku_puzzle)

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
    opened.append(sudoku_puzzle)    

    while opened:
        current_state = opened.pop()
        count+=1
        current_state_tuple = tuple(map(tuple, current_state))
        closed.add(current_state_tuple)

        # Termination condition 
        if count_zeros(current_state) == 0:
            return current_state, path, count

        # Find the target position to be explored
        target = heuristic(current_state)
        
        # Add most recent target to the path
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

    return "No solution found"

def bfs(sudoku_puzzle):
    opened = []
    closed = set()
    path = []
    count = 0
    opened.append(sudoku_puzzle)    

    while opened:
        current_state = opened.pop(0)
        count+=1
        current_state_tuple = tuple(map(tuple, current_state))
        closed.add(current_state_tuple)

        # Termination condition 
        if count_zeros(current_state) == 0:
            return current_state, path, count

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

    return "No solution found"

def compare(prob):
    # comparing the number of iterations for each difficulty level
    l_dfs = []
    l_bfs = []
    labels = ["Easy", "Medium", "Hard", "Evil"]
    for i in range(4):
        l_dfs.append(dfs(np.array(prob[i]))[2])
        l_bfs.append(bfs(np.array(prob[i]))[2])

    barWidth = 0.25
    br1 = np.arange(len(l_dfs))
    br2 = [x + 0.10 for x in br1]
    br3 = [x + barWidth for x in br2]
    
    plt.bar(br1, l_dfs, color ='b', width = barWidth, edgecolor ='grey', label ='DFS')
    plt.bar(br3, l_bfs, color ='g', width = barWidth, edgecolor ='white', label ='BFS')
    
    plt.xlabel('Puzzles', fontweight ='bold', fontsize = 15)
    plt.ylabel('Iterations', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(l_dfs))], labels)
    
    plt.legend()
    plt.show()
    
    # comparing the number of iterations for different sizes of puzzles
    dfs_4 = dfs(np.array(prob[5]))[2]
    dfs_9 = dfs(np.array(prob[3]))[2]
    dfs_16 = dfs(np.array(prob[10]))[2]
    plt.bar(["4x4", "9x9", "16x16"], [dfs_4, dfs_9, dfs_16], color ='b', width = 0.5, edgecolor ='grey', label ='DFS')
    plt.xlabel('Puzzles', fontweight ='bold', fontsize = 15)
    plt.ylabel('Iterations', fontweight ='bold', fontsize = 15)
    
    plt.legend()
    plt.show()   

# Problem to be solved
sudoku_puzzle = np.array(prob[0])
print("Problem:\n",sudoku_puzzle)

# Check if the sudoku puzzle is valid
None if valid_sudoku(sudoku_puzzle) else exit("Invalid Sudoku Puzzle")

print("Number of empty spaces : ", count_zeros(sudoku_puzzle))

print("\nDFS solution")
solution, solution_path, count = dfs(sudoku_puzzle)
print("Totol number of iterations : ", count)
print(solution)
print("Solution path:")
print(solution_path)

print("\nBFS solution")
solution, solution_path, count = bfs(sudoku_puzzle)
print("Totol number of iterations : ", count)
print(solution)
print("Solution path:")
print(solution_path)

# Give comparison of the number of iterations for each difficulty level and different sizes of puzzles
compare(prob)