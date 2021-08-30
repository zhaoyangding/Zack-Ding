#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pulp
from termcolor import colored
# initial the grid,row,column,and box
Grids = range(1,10)
Rows = range(0,9)
Cols = range(0,9)
Boxes =[]
# Create a 9x9 Sudoku game
for i in range(3):
    for j in range(3):
        Boxes += [[(Rows[3*i+p], Cols[3*j+q]) for p in range(3) for q in range(3)]]
choices = pulp.LpVariable.dicts("Choice", (Grids, Rows, Cols), 0, 1, pulp.LpInteger)
f = pulp.LpProblem("Sudoku Problem", pulp.LpMinimize)
f += 0, "Arbitrary Objective Function"
# Constraint to ensure only one value is filled for a cell
for r in Rows:
    for c in Cols:
        f+=pulp.lpSum([choices[v][r][c] for v in Grids]) == 1, ""
# Constraint to ensure that values from 1 to 9 is filled only once in a row 
for v in Grids:
    for r in Rows:
        f+=pulp.lpSum([choices[v][r][c] for c in Cols]) == 1, ""
# Constraint to ensure that values from 1 to 9 is filled only once in a column  
    for c in Cols:
        f+=pulp.lpSum([choices[v][r][c] for r in Rows]) == 1, ""
# Constraint to ensure that values from 1 to 9 is filled only once in each boxes  
    for b in Boxes:
        f+=pulp.lpSum([choices[v][r][c] for (r,c) in b]) == 1, ""
# Main loop for solving Sudoku game
    f.solve()
    print(pulp.LpStatus[f.status])
    # Code to extract the final solution grid
    solution = [[0 for c in Cols] for r in Rows]
    grid_list = []
    for r in Rows:
        for c in Cols:
            for v in Grids:
                if pulp.value(choices[v][r][c]):
                    solution[r][c] = v

    # Print the final solution as a grid
    print(f"\nFinal result:")

    print("\n\n+ ----------- + ----------- + ----------- +",end="")
    for r in Rows:
        print("\n",end="\n|  ")
        for c in Cols:
            num_end = "  |  " if ((c+1)%3 == 0) else "   "
            print(solution[r][c],end=num_end)
        if ((r+1)%3 == 0):
            print("\n\n+ ----------- + ----------- + ----------- +",end="")
  


# In[ ]:




