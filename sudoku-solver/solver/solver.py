import numpy as np


class Solver:
    total = 45
    grid_size = (3, 3)

    def __init__(self, puzzle):
        self.potential = None
        self.puzzle = puzzle

    def complete_rows(self):
        for row in [x for x in self.puzzle if sum(x == None) == 1]:
            row[np.where(row == None)] = self.total - sum(row[np.where(row != None)])

    def complete_cols(self):
        for col in [x for x in self.puzzle.T if sum(x == None) == 1]:
            col[np.where(col == None)] = self.total - sum(col[np.where(col != None)])

    def complete_subgrid(self):
        for rows in range(0, 9, 3):
            for cols in range(0, 9, 3):
                subgrid = self.puzzle[cols:cols + 3, rows:rows + 3]
                if sum(subgrid.flatten() == None) == 1:
                    subgrid[np.where(subgrid == None)] = self.total - sum(subgrid[np.where(subgrid != None)])

    def generate_potentials(self):
        self.potential = list(self.puzzle.copy())
        for r, row in enumerate(self.potential):
            for c, cell in enumerate(row):
                if not cell:
                    self.potential[r][c] = set(range(1, 10)) - set(self.puzzle[r]) - set(self.puzzle[:, c])
        for rows in range(0, 9, 3):
            for cols in range(0, 9, 3):
                subgrid = set(list(self.puzzle[rows:rows + 3, cols:cols + 3].flatten()))
                for r in range(rows, rows + 3):
                    for c in range(cols, cols + 3):
                        if isinstance(self.potential[r][c], set):
                            self.potential[r][c] -= subgrid

    def check_potentials(self):
        for r, row in enumerate(self.potential):
            for c, cell in enumerate(row):
                if isinstance(cell, set) and len(cell) == 1:
                    self.potential[r][c] = cell.pop()
                    self.puzzle[r, c] = self.potential[r][c]

    def check_only_potentials(self):
        self.check_only_potential_row()
        self.check_only_potential_col()
        self.check_only_potential_subgrid()

    def check_only_potential_row(self):
        for row in self.potential:
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


    def solved(self):
        if sum(self.puzzle.flatten() == None) == 0:
            return True
        else:
            return False

    def solve(self):
        self.generate_potentials()
        while not self.solved():
            self.complete_rows()
            self.complete_cols()
            self.complete_subgrid()
            self.generate_potentials()
            self.check_potentials()
            self.check_only_potentials()
