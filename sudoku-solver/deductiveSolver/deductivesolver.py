import numpy as np
import itertools
from collections import Counter


class DeductiveSolver:
    total = 45
    grid_size = (3, 3)

    def __init__(self, puzzle):
        self.puzzle = puzzle.astype("object")

    def initialise_potentials(self):
        for r, row in enumerate(self.puzzle):
            for c, cell in enumerate(row):
                if cell == 0:
                    self.puzzle[r][c] = set(range(1, 10)) - set(x for x in self.puzzle[r] if isinstance(x, int)) - set(
                        x for x in self.puzzle.T[c] if isinstance(x, int))
        for rows in range(0, 9, 3):
            for cols in range(0, 9, 3):
                subgrid = set(
                    list(x for x in self.puzzle[rows:rows + 3, cols:cols + 3].flatten() if isinstance(x, int)))
                for r in range(rows, rows + 3):
                    for c in range(cols, cols + 3):
                        if isinstance(self.puzzle[r][c], set):
                            self.puzzle[r][c] -= subgrid

    def check_potentials(self):
        cell_updated = True
        while cell_updated:
            cell_updated = False
            for r, row in enumerate(self.puzzle):
                for c, cell in enumerate(row):
                    if isinstance(cell, set) and len(cell) == 1:
                        self.puzzle[r, c] = next(iter(cell))
                        self.update_grid(set([self.puzzle[r, c]]), r, c)
                        cell_updated = True

    def update_grid(self, val, row, col):
        self.update_line(val, self.puzzle[row])
        self.update_line(val, self.puzzle.T[col])
        self.update_subgrid(val, row, col)
        self.check_potentials()

    @staticmethod
    def update_line(val, line):
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

    def check_naked_vals(self):
        for r, row in enumerate(self.puzzle):
            array_modified, deduced_val_loc = DeductiveSolver.check_naked_vals_in_array(row)
            for c in deduced_val_loc:
                self.update_grid(set([self.puzzle[r][c]]), r, c)
            if array_modified:
                self.check_potentials()
        for c, col in enumerate(self.puzzle.T):
            array_modified, deduced_val_loc = DeductiveSolver.check_naked_vals_in_array(col)
            for r in deduced_val_loc:
                self.update_grid(set([self.puzzle[r][c]]), r, c)
            if array_modified:
                self.check_potentials()
        # TODO
        # for subgrid in

        # for r, row in enumerate(self.puzzle):
        #     for c, cell in enumerate(row):
        #         if isinstance(cell, set):
        #             _r = list(row)
        #             check = DeductiveSolver.check_only_potential_value(cell.copy(), _r[:c] + _r[c + 1:])
        #             if not check:
        #                 _c = list(self.puzzle.T[c])
        #                 check = DeductiveSolver.check_only_potential_value(cell.copy(), _c[:r] + _c[r + 1:])
        #                 if not check:
        #                     r0 = r - r % 3
        #                     c0 = c - c % 3
        #                     _linearPos = r0 * 3 + c0
        #                     _sg = list(self.puzzle[r0:r0 + 3, c0:c0 + 3].flatten())
        #                     check = DeductiveSolver.check_only_potential_value(cell.copy(), _sg[:_linearPos] + _sg[_linearPos + 1:])
        #             if check:
        #                 self.puzzle[r][c] = check
        #                 self.update_grid(set([check]), r, c)

    @staticmethod
    def check_naked_vals_in_array(arr):
        array_modified = False
        deduced_val_loc = []
        arr_counts = Counter(frozenset(s) for s in arr if isinstance(s, set))
        for pots in arr_counts:
            if len(pots) == 1:
                deduced_val_loc.append(int(np.where(arr == pots)[0][0]))
                arr[deduced_val_loc[-1]] = next(iter(pots))
            if len(pots) == arr_counts[pots]:
                for cell in arr:
                    if isinstance(cell, set) and cell != set(pots):
                        cell -= pots
                        array_modified = True
        return array_modified, deduced_val_loc

    def check_pointing_val(self):
        for rows in range(0, 9, 3):
            for cols in range(0, 9, 3):
                subgrid = self.puzzle[rows:rows + 3, cols:cols + 3]
                DeductiveSolver.check_pointing_val_in_line(self.puzzle, subgrid, rows, cols)
                DeductiveSolver.check_pointing_val_in_line(self.puzzle.T, subgrid.T, cols, rows)

    @staticmethod
    def check_pointing_val_in_line(puzzle, subgrid, rows, cols):
        r_pots = [set().union(*(x for x in row if isinstance(x, set))) for row in subgrid]
        r_val_has_to_be_here = [r_pots[a] - r_pots[b] - r_pots[c] for a, b, c in [[0, 1, 2], [1, 0, 2], [2, 0, 1]]]
        for idx_r, r in enumerate(r_val_has_to_be_here):
            if len(r) > 0:
                # Propagate across row without touching this subgrid
                cols_to_modify = set(range(9)) - set(range(cols, cols + 3))
                for _col in cols_to_modify:
                    if isinstance(puzzle[rows + idx_r][_col], set):
                        puzzle[rows + idx_r][_col] -= r

    # If only ints are left in the puzzle it's solved
    def solved(self):
        return all([isinstance(x, int) for x in self.puzzle.flatten()])

    # If there's any empty set of potentials in the puzzle then it's not solvable
    def solvable(self):
        return not any([x == set() for x in self.puzzle.flatten()])

    def solve(self):
        self.initialise_potentials()
        self.check_potentials()
        # while not self.solved():
        for __ in range(1000):
            self.check_naked_vals()
            self.check_pointing_val()
