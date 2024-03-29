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
                        self.update_grid({self.puzzle[r, c]}, r, c)
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

    def check_naked_and_hidden_sets(self):
        for r, row in enumerate(self.puzzle):
            array_modified, deduced_val_loc = DeductiveSolver.check_naked_vals_in_array(row)
            array_modified = DeductiveSolver.check_hidden_vals_in_array(row)
            for c in deduced_val_loc:
                self.update_grid({self.puzzle[r][c]}, r, c)
            if array_modified and not deduced_val_loc:
                self.check_potentials()
        for c, col in enumerate(self.puzzle.T):
            array_modified, deduced_val_loc = DeductiveSolver.check_naked_vals_in_array(col)
            array_modified = DeductiveSolver.check_hidden_vals_in_array(col)
            for r in deduced_val_loc:
                self.update_grid({self.puzzle[r][c]}, r, c)
            if array_modified and not deduced_val_loc:
                self.check_potentials()
        for r0 in range(0, 9, 3):
            for c0 in range(0, 9, 3):
                subgrid = self.puzzle[r0:r0 + 3, c0:c0 + 3].flatten()
                array_modified, deduced_val_loc = DeductiveSolver.check_naked_vals_in_array(subgrid)
                array_modified = DeductiveSolver.check_hidden_vals_in_array(subgrid)
                for loc in deduced_val_loc:
                    r = r0 + np.floor(loc, 3)
                    c = c0 + (loc % 3)
                    self.update_grid({self.puzzle[r][c]}, r, c)
                if array_modified and not deduced_val_loc:
                    self.check_potentials()

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

    @staticmethod
    def check_hidden_vals_in_array(arr):
        array_modified = False
        foo = Counter(itertools.chain(*[x for x in arr if isinstance(x,set)]))
        count = dict()
        for k,v in foo.items():
            if v not in count.keys():
                count[v] = []
            count[v].append(k)
        for k,v in count.items():
            if len(v) >= k:
                for proposed_set in itertools.combinations(v, k):
                    is_subset = [(set(proposed_set).issubset(x) if isinstance(x, set) else False) for x in arr]
                    # If hidden sets exist
                    if sum(is_subset) == k:
                        for i in list(itertools.compress(range(len(is_subset)), is_subset)):
                            arr[i] = set(proposed_set)
                            array_modified = True
        return array_modified

    def check_pointing_val(self):
        for rows in range(0, 9, 3):
            for cols in range(0, 9, 3):
                subgrid = self.puzzle[rows:rows + 3, cols:cols + 3]
                DeductiveSolver.check_pointing_val_in_subgrid(self.puzzle, subgrid, rows, cols)
                DeductiveSolver.check_pointing_val_in_subgrid(self.puzzle.T, subgrid.T, cols, rows)
        for idx_line in range(9):
            DeductiveSolver.check_pointing_val_in_line(self.puzzle, idx_line)
            DeductiveSolver.check_pointing_val_in_line(self.puzzle.T, idx_line)

    @staticmethod
    def check_pointing_val_in_subgrid(puzzle, subgrid, rows, cols):
        # Find all potentials in each row in the subgrid
        r_pots = [set().union(*(x for x in row if isinstance(x, set))) for row in subgrid]
        r_val_has_to_be_here = [r_pots[a] - r_pots[b] - r_pots[c] for a, b, c in [[0, 1, 2], [1, 0, 2], [2, 0, 1]]]
        for idx_r, r in enumerate(r_val_has_to_be_here):
            if len(r) > 0:
                # Propagate across row without touching this subgrid
                cols_to_modify = set(range(9)) - set(range(cols, cols + 3))
                for _col in cols_to_modify:
                    if isinstance(puzzle[rows + idx_r][_col], set):
                        puzzle[rows + idx_r][_col] -= r

    @staticmethod
    def check_pointing_val_in_line(puzzle, idx_line):
        # Find all potentials for each subgrid row in each row
        r_pots = [set().union(*([puzzle[idx_line][x] for x in range(y,y+3) if isinstance(puzzle[idx_line][x],set)])) for y in range(0,9,3)]
        r_val_has_to_be_here = [r_pots[a] - r_pots[b] - r_pots[c] for a, b, c in [[0, 1, 2], [1, 0, 2], [2, 0, 1]]]
        for idx_r, r in enumerate(r_val_has_to_be_here):
            if len(r) > 0:
                for row in range(idx_line-(idx_line%3),idx_line-(idx_line%3)+3):
                    if row == idx_line:
                        continue
                    for col in range(idx_r*3,idx_r*3+3):
                        if isinstance(puzzle[row][col], set):
                            puzzle[row][col] -= r

    def check_x_wings(self):
        DeductiveSolver.check_x_wings_in_line(self.puzzle)
        DeductiveSolver.check_x_wings_in_line(self.puzzle.T)

    @staticmethod
    def check_x_wings_in_line(puzzle):
        for idx_line1, line1 in enumerate(puzzle):
            # Find positions of each potential value
            pots = {k:v for (k,v) in zip (range(1,10), [[idx for idx,x in enumerate(line1) if (isinstance(x,set) and {i}.issubset(x))] for i in range(1,10)])}
            for digit, pos in pots.items():
                if len(pos) != 2:
                    continue
                for idx_line2, line2 in enumerate(puzzle):
                    if idx_line2 == idx_line1:
                        continue
                    if [idx for idx,x in enumerate(line2) if (isinstance(x,set) and {digit}.issubset(x))] == pos:
                        for l in range(9):
                            if l == idx_line1 or l == idx_line2:
                                continue
                            puzzle[l][pos[0]] -= set([digit]) if isinstance(puzzle[l][pos[0]],set) else 0
                            puzzle[l][pos[1]] -= set([digit]) if isinstance(puzzle[l][pos[1]],set) else 0

    def check_xy_wings(self):
        for pots1 in self.xy_find_potential_cell():
            for pots1_val in list(self.puzzle[pots1]):
                for pots2 in self.xy_find_potential_cell({pots1_val}):
                    # If same cell
                    if pots2 == pots1:
                        continue
                    # If same values
                    if self.puzzle[pots2] == self.puzzle[pots1]:
                        continue
                    if not DeductiveSolver.xy_check_intersection(pots1, pots2):
                        continue
                    # Find uncommon values
                    pots3_val = self.puzzle[pots1].union(self.puzzle[pots2]) - self.puzzle[pots1].intersection(self.puzzle[pots2])
                    for pots3 in self.xy_find_potential_cell(pots3_val):
                        if pots3 == pots2 or pots3 == pots1:
                            continue
                        # Check intersections with pots1 or pots2
                        intersections = [DeductiveSolver.xy_check_intersection(pots1, pots3),
                                         DeductiveSolver.xy_check_intersection(pots2, pots3)]
                        if all(intersections) or not any(intersections):
                            continue
                        if intersections[0]:
                            wings = [pots2, pots3]
                        elif intersections[1]:
                            wings = [pots1, pots3]
                        shared_marking = self.puzzle[wings[0]].intersection(self.puzzle[wings[1]])
                        for r, c in DeductiveSolver.xy_find_intersecting_cells(*wings):
                            if isinstance(self.puzzle[r][c], set):
                                self.puzzle[r][c] -= shared_marking

    def xy_find_potential_cell(self, scribble_must_have=set()):
        if len(scribble_must_have) == 2:
            idx = [(x, y) for x, y in zip(*np.where(self.puzzle == scribble_must_have))]
            if not any(idx):
                idx = []
        else:
            idx = []
            for r, row in enumerate(self.puzzle):
                for c, cell in enumerate(row):
                    if isinstance(cell, set) and len(cell) == 2 and scribble_must_have.issubset(cell):
                        idx.append((r, c))
        return idx

    @staticmethod
    def xy_check_intersection(loc1, loc2):
        intersects = True
        if loc1[0] != loc2[0] and loc1[1] != loc2[1]:
            if not (np.floor_divide(loc1[0], 3) == np.floor_divide(loc2[0], 3) and np.floor_divide(loc1[1], 3) == np.floor_divide(loc2[1], 3)):
                intersects = False
        return intersects

    @staticmethod
    def xy_find_intersecting_cells(cell1, cell2):
        intersections = []
        for r in range(9):
            for c in range(9):
                if (r, c) == cell1 or (r, c) == cell2:
                    continue
                if DeductiveSolver.xy_check_intersection((r, c), cell1) and DeductiveSolver.xy_check_intersection((r, c), cell2):
                    intersections.append((r, c))
        return intersections

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
            self.check_pointing_val()
            self.check_naked_and_hidden_sets()
            self.check_xy_wings()
            self.check_x_wings()