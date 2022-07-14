from solver.solver import Solver
import numpy as np


def main():
    puzzle = np.array([[None, None, None, None, None, 8, None, 5, None],
                       [4, 1, None, None, None, None, 2, None, 9],
                       [None, 5, 2, None, 4, None, None, None, None],
                       [1, None, None, None, 2, None, None, None, None],
                       [None, None, 3, None, None, 4, 5, None, 8],
                       [None, None, None, None, 9, 3, None, 2, 7],
                       [None, 2, 7, 4, 3, None, 8, 9, 6],
                       [8, 3, 1, 5, 6, None, None, 4, 2],
                       [9, None, None, 7, 8, None, None, None, None]])
    puzzle = Solver(puzzle)
    puzzle.solve()
    puzzle


if __name__ == '__main__':
    main()
