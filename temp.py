import numpy as np
from copy import deepcopy


sudoku_puzzle = [
    [4, 3, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 2, 0],
    [0, 0, 0, 0]
]

sudoku_puzzle = np.array(sudoku_puzzle)

def heuristic():
    current_state = deepcopy(sudoku_puzzle)
    zero_count = [0,0,0,0]
    zero_count = np.array(zero_count)

    for i in range(4):
        for j in range(4):
            if (i//2 == 0 and j//2 ==0 and current_state[i][j]==0):
                zero_count[0] +=1                
            elif (i//2 == 1 and j//2 ==0 and current_state[i][j]==0):
                zero_count[1] +=1
            elif( i//2 == 0 and j//2 == 1 and current_state[i][j] == 0):
                zero_count[2] +=1
            elif( i//2 == 1 and j//2 == 1 and current_state[i][j] == 0):
                zero_count[3] +=1

    for i in range(4):
        if zero_count[i] == 0:
            zero_count[i] = 999

    search_key = min(zero_count)
    item_index = np.where(zero_count == search_key)[0] 
    print(item_index)
    for i in item_index:
        subgrid_row, subgrid_col = (i//2 * 2, i%2 * 2)    
        for i in range(subgrid_row, subgrid_row + 2):
            for j in range(subgrid_col, subgrid_col + 2):
                print(current_state[i][j], end=" ")
            print()
    
    
    

    return zero_count

temp2 = heuristic()
print(temp2)
