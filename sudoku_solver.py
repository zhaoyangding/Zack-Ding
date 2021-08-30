#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pulp
from termcolor import colored
#initialize a sudoku and colored these value in pink
init_choices = {
    ("1", "1"): "5",
    ("2", "1"): "6",
    ("4", "1"): "8",
    ("5", "1"): "4",
    ("6", "1"): "7",
    ("1", "2"): "3",
    ("3", "2"): "9",
    ("7", "2"): "6",
    ("3", "3"): "8",
    ("2", "4"): "1",
    ("5", "4"): "8",
    ("8", "4"): "4",
    ("1", "5"): "7",
    ("2", "5"): "9",
    ("4", "5"): "6",
    ("6", "5"): "2",
    ("8", "5"): "1",
    ("9", "5"): "8",
    ("2", "6"): "5",
    ("5", "6"): "3",
    ("8", "6"): "9",
    ("7", "7"): "2",
    ("3", "8"): "6",
    ("7", "8"): "8",
    ("9", "8"): "7",
    ("4", "9"): "3",
    ("5", "9"): "1",
    ("6", "9"): "6",
    ("8", "9"): "5",
}
# create a list include all index
a = ["1","2","3","4","5","6","7","8","9"]
# initial the grid,row,column,and box
Grids = a
Rows = a
Cols = a
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
for (r, c), v in init_choices.items():
    f+= choices[v][r][c]==1,""
    f.solve()
    print(pulp.LpStatus[f.status])
    if pulp.LpStatus[f.status] == "Optimal":
# Separate each boxes using +-----+
        for r in Rows:
            if r=="1"or r=="4" or r=="7":
                print("+-------+-------+-------+")
            s=''
            for c in Cols:
                for v in Grids:
                    if pulp.value(choices[v][r][c]) == 1:
                        if c=="1"or c=="4"or c=="7":
                            s+="| "
                        if init_choices.get((r, c)) == v:
                            s+=(colored(v,'white','on_magenta') + " ")
                        else:
                            s+=(v + " ")
            s+="|"
            print(s)
            print("+-------+-------+-------+")
            f+= pulp.lpSum([choices[v][r][c] for v in Grids
                                             for r in Rows
                                             for c in Cols
                                                if pulp.value(choices[v][r][c]) == 1]) <= 80
    else:
        break

