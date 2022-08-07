from deductiveSolver.deductivesolver import DeductiveSolver
from bruteForceSolver.bruteforcesolver import BruteForceSolver
from viewer.viewer import Viewer
import numpy as np


def main():
    # puzzle = np.array([[0, 0, 0, 0, 0, 8, 0, 5, 0],
    #                    [4, 1, 0, 0, 0, 0, 2, 0, 9],
    #                    [0, 5, 2, 0, 4, 0, 0, 0, 0],
    #                    [1, 0, 0, 0, 2, 0, 0, 0, 0],
    #                    [0, 0, 3, 0, 0, 4, 5, 0, 8],
    #                    [0, 0, 0, 0, 9, 3, 0, 2, 7],
    #                    [0, 2, 7, 4, 3, 0, 8, 9, 6],
    #                    [8, 3, 1, 5, 6, 0, 0, 4, 2],
    #                    [9, 0, 0, 7, 8, 0, 0, 0, 0]])
    # https://www.sudoku-solutions.com/ sample puzzle 9312 easy
    # puzzle = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                    [0, 0, 6, 0, 5, 0, 2, 0, 7],
    #                    [0, 7, 0, 9, 0, 0, 0, 1, 0],
    #                    [0, 2, 9, 0, 3, 0, 8, 5, 1],
    #                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                    [5, 6, 0, 0, 8, 0, 7, 9, 3],
    #                    [0, 1, 0, 0, 0, 2, 0, 7, 0],
    #                    [8, 0, 3, 0, 6, 0, 4, 2, 0],
    #                    [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    # sample puzzle 322 medium
    # puzzle = np.array([[0, 0, 0, 0, 0, 9, 0, 0, 2],
    #                    [0, 0, 0, 0, 0, 0, 0, 1, 4],
    #                    [1, 3, 0, 0, 5, 0, 0, 0, 7],
    #                    [0, 0, 5, 6, 0, 0, 0, 0, 0],
    #                    [0, 6, 0, 2, 9, 7, 0, 4, 0],
    #                    [0, 0, 0, 0, 0, 3, 6, 0, 0],
    #                    [9, 0, 0, 0, 7, 0, 0, 8, 1],
    #                    [4, 8, 0, 0, 0, 0, 0, 0, 0],
    #                    [2, 0, 0, 9, 0, 0, 0, 0, 0]])
    # sample puzzle 1981 hard
    # puzzle = np.array([[7, 4, 0, 0, 0, 0, 1, 0, 0],
    #                    [9, 5, 3, 0, 0, 0, 0, 2, 0],
    #                    [0, 8, 0, 0, 0, 9, 0, 0, 5],
    #                    [0, 0, 0, 5, 1, 0, 4, 0, 0],
    #                    [0, 0, 0, 9, 0, 2, 0, 0, 0],
    #                    [0, 0, 4, 0, 3, 6, 0, 0, 0],
    #                    [8, 0, 0, 2, 0, 0, 0, 4, 0],
    #                    [0, 6, 0, 0, 0, 0, 5, 7, 2],
    #                    [0, 0, 9, 0, 0, 0, 0, 8, 6]])

    # 8038 hard
    # puzzle = np.array([[3,9,0,6,0,1,0,0,0],
    #                    [0,0,0,5,0,0,0,8,0],
    #                    [0,0,6,0,0,2,0,0,0],
    #                    [8,0,0,0,0,9,5,2,1],
    #                    [0,2,0,4,0,0,0,0,0],
    #                    [0,0,9,0,2,0,0,7,4],
    #                    [0,0,7,9,0,0,2,0,0],
    #                    [0,3,0,0,5,0,7,0,9],
    #                    [0,0,0,0,0,7,0,0,5]])
    # 1020 hard
    puzzle = np.array([[0,9,3,0,0,5,8,0,0],
                       [1,0,0,8,0,0,0,0,0],
                       [0,0,6,9,2,0,5,0,0],
                       [4,0,0,3,0,0,7,0,0],
                       [0,8,0,7,0,2,0,5,0],
                       [0,0,9,0,0,8,0,0,6],
                       [0,0,8,0,3,1,6,0,0],
                       [0,0,0,0,0,4,0,0,8],
                       [0,0,2,5,0,0,9,4,0]])

    puzzle = DeductiveSolver(puzzle)
    puzzle.solve()
    Viewer.view(puzzle.puzzle)

    # puzzle = BruteForceSolver.solve(puzzle)
    # Viewer.view(puzzle)


if __name__ == '__main__':
    main()
