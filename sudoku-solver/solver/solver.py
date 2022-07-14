import numpy as np


class Solver:
    total = 45
    grid_size = (3, 3)

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def initialise_potentials(self):
        for r, row in enumerate(self.puzzle):
            for c, cell in enumerate(row):
                if not cell:
                    self.puzzle[r,c] = set(range(1, 10)) - set(x for x in self.puzzle[r] if isinstance(x, int)) - set(x for x in self.puzzle.T[c] if isinstance(x, int))
        for rows in range(0, 9, 3):
            for cols in range(0, 9, 3):
                subgrid = set(list(x for x in self.puzzle[rows:rows + 3, cols:cols + 3].flatten() if isinstance(x, int)))
                for r in range(rows, rows + 3):
                    for c in range(cols, cols + 3):
                        if isinstance(self.puzzle[r][c], set):
                            self.puzzle[r][c] -= subgrid

    def check_potentials(self):
        for r, row in enumerate(self.puzzle):
            for c, cell in enumerate(row):
                if isinstance(cell, set) and len(cell) == 1:
                    self.puzzle[r, c] = next(iter(cell))
                    self.update_grid(set([self.puzzle[r,c]]), r, c)

    def update_grid(self, val, row, col):
        self.update_line(val, self.puzzle[row])
        self.update_line(val, self.puzzle.T[col])
        self.update_subgrid(val, row, col)

    def update_line(self, val, line):
        for ele in line:
            if isinstance(ele, set):
                ele -= val

    def update_subgrid(self, val, row, col):
        idx_row_0 = row - row % 3
        idx_col_0 = col - col % 3
        for r in range(idx_row_0, idx_row_0 + 3):
            for c in range(idx_col_0, idx_col_0 + 3):
                if isinstance(self.puzzle[r][c], set):
                    self.puzzle[r][c] -= val

    def check_only_potentials(self):
        self.check_only_potential_row()
        self.check_only_potential_col()
        self.check_only_potential_subgrid()

    def check_only_potential_row(self):
        for row in self.puzzle:
            for i, cell in enumerate(row):
                if isinstance(cell, set):
                    r = list(row)
                    check = Solver.check_only_potential_value(cell.copy(), r[:i] + r[i+1:])
                    if check:
                        cell = check

    def check_only_potential_col(self):
        pass

    def check_only_potential_subgrid(self):
        pass

    def check_only_potential_value(cell, potentials):
        for c in potentials:
            if isinstance(c, set):
                cell -= c
        if len(cell) == 1:
            return next(iter(cell))
        else:
            return False

    # If only ints are left in the puzzle it's solved
    def solved(self):
        return all([isinstance(x,int) for x in self.puzzle.flatten()])

    # If there's any empty set of potentials in the puzzle then it's not solvable
    def solvable(self):
        return not any([x == set() for x in self.puzzle.flatten()])

    def solve(self):
        self.initialise_potentials()
        while not self.solved():
            self.check_potentials()
