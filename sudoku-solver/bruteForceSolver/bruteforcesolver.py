import numpy as np
import functools


class BruteForceSolver:
    @staticmethod
    def solve(puzzle):
        stack = [puzzle.copy()]
        while len(stack) > 0:
            current = stack.pop()
            for val in range(1,10):
                idx_next_guess_coords = list(zip(*np.where(current == 0)))[0]
                proposed = current.copy()
                proposed[idx_next_guess_coords] = val
                if BruteForceSolver.is_valid(proposed, val, idx_next_guess_coords[0], idx_next_guess_coords[1]):
                    if BruteForceSolver.solved(proposed):
                        return proposed
                    stack.append(proposed)

    @staticmethod
    def is_valid(puzzle, val, r, c):
        row = [x for x in puzzle[r] if x in list(range(1,10))]
        if len(row) != len(set(row)):
            return False
        col = [x for x in puzzle.T[c] if x in list(range(1,10))]
        if len(col) != len(set(col)):
            return False
        subgrid = [x for x in puzzle[r-r%3:r-r%3+3, c-c%3:c-c%3+3].flatten() if x in list(range(1,10))]
        if len(subgrid) != len(set(subgrid)):
            return False
        return True

    @staticmethod
    def solved(puzzle):
        return all(puzzle.flatten())