from unittest import TestCase

from puzzle_solver import max_seen_cells, min_seen_cells, check_constraints, solve_puzzle, how_many_solutions, \
    generate_puzzle


class TestEx8(TestCase):
    def test_max_seen_cells(self):
        picture = [[-1, 0, 1, -1], [0, 1, -1, 1], [1, 0, 1, 0]]
        self.assertEqual(1, max_seen_cells(picture, 0, 0))
        self.assertEqual(0, max_seen_cells(picture, 1, 0))
        self.assertEqual(5, max_seen_cells(picture, 1, 2))
        self.assertEqual(3, max_seen_cells(picture, 1, 1))
        picture = [[-1, -1, -1, 1, 1], [0, -1, -1, 0, 1], [1, 1, 0, 1, 0]]
        self.assertEqual([[5, 7, 6, 5, 6], [0, 4, 3, 0, 2], [2, 4, 0, 1, 0]],
                         [[max_seen_cells(picture, i, j) for j in range(5)] for i in range(3)])
        self.assertEqual(int, type(max_seen_cells(picture, 0, 0)))

    def test_min_seen_cells(self):
        picture = [[-1, 0, 1, -1], [0, 1, -1, 1], [1, 0, 1, 0]]
        self.assertEqual(0, min_seen_cells(picture, 0, 0))
        self.assertEqual(0, min_seen_cells(picture, 1, 0))
        self.assertEqual(0, min_seen_cells(picture, 1, 2))
        self.assertEqual(1, min_seen_cells(picture, 1, 1))
        picture = [[-1, -1, -1, 1, 1], [0, -1, -1, 0, 1], [1, 1, 0, 1, 0]]
        self.assertEqual([[0, 0, 0, 2, 3], [0, 0, 0, 0, 2], [2, 2, 0, 1, 0]],
                         [[min_seen_cells(picture, i, j) for j in range(5)] for i in range(3)])
        self.assertEqual(int, type(min_seen_cells(picture, 0, 0)))

    def test_check_constraints(self):
        picture = [[-1, 0, 1, -1], [0, 1, -1, 1], [1, 0, 1, 0]]
        self.assertEqual(0, check_constraints(picture, {(0, 3, 5), (1, 2, 5), (2, 0, 1)}))
        self.assertEqual(2, check_constraints(picture, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}))

        picture = [[0, 0, 1, 1],
                   [0, 1, 1, 1],
                   [1, 0, 1, 0]]
        self.assertEqual(1, check_constraints(picture, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}))
        self.assertEqual(0, check_constraints(picture, {(0, 3, 3), (2, 3, 2), (2, 0, 1)}))
        self.assertEqual(0, check_constraints(picture, {(0, 3, 3), (2, 3, 0), (1, 2, 3), (2, 0, 1)}))
        # self.assertEqual(2, check_constraints(picture, {(0, 3, 3), (2, 3, 2), (2, 0, 1)}))

    def test_solve_puzzle(self):
        self.assertEqual([[0, 0], [0, 1]],
                         solve_puzzle({(0, 0, 0), (1, 1, 1)}, 2, 2))
        self.assertEqual([[0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0]],
                         solve_puzzle({(0, 3, 3), (1, 2, 5), (2, 0, 1), (0, 0, 0)}, 3, 4))
        self.assertIsNone(solve_puzzle({(0, 3, 3), (1, 2, 5), (2, 0, 1), (2, 3, 5)}, 3, 4))
        self.assertIn(solve_puzzle({(0, 2, 3), (1, 1, 4), (2, 2, 5)}, 3, 3), [[[0, 0, 1], [1, 1, 1], [1, 1, 1]],
                                                                              [[1, 0, 1], [1, 1, 1], [1, 1, 1]]])
        self.assertEqual(0, solve_puzzle({(0, 0, 0)}, 3, 3)[0][0])
        self.assertEqual([[1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]], solve_puzzle({(0, 0, 2), (0, 3, 5), (1, 5, 7)}, 2, 6))

    def test_how_many_solutions(self):
        self.assertEqual(0, how_many_solutions({(0, 3, 3), (1, 2, 5), (2, 0, 1), (2, 3, 5)}, 3, 4))
        self.assertEqual(1, how_many_solutions({(0, 0, 0), (1, 1, 1)}, 2, 2))
        self.assertEqual(2, how_many_solutions({(0, 2, 3), (1, 1, 4), (2, 2, 5)}, 3, 3))
        self.assertEqual(1, how_many_solutions({(0, 3, 3), (1, 2, 5), (2, 0, 1), (0, 0, 1)}, 3, 4))
        self.assertEqual(2, how_many_solutions({(0, 2, 3), (1, 1, 4), (2, 2, 5)}, 3, 3))
        self.assertEqual(1, how_many_solutions({(i, j, 0) for i in range(3) for j in range(3)}, 3, 3))
        self.assertEqual(16, how_many_solutions(set(), 2, 2))
        self.assertEqual(64, how_many_solutions({(0, 3, 3), (2, 0, 1)}, 3, 4))

    def test_generate_puzzle(self):
        picture = [[0, 1], [1, 1]]
        self.assertIn(generate_puzzle(picture), [{(0, 0, 0), (1, 1, 3)},
                                                 {(1, 1, 3), (1, 0, 2)},
                                                 {(0, 1, 2), (0, 0, 0), (1, 0, 2)},
                                                 {(0, 0, 0), (1, 0, 2), (1, 1, 3)}])

        picture = [[1, 0, 0], [1, 1, 1]]
        self.assertIn(generate_puzzle(picture), [{(0, 0, 2), (1, 2, 3)},
                                                 {(1, 0, 4), (0, 1, 0), (0, 2, 0)},
                                                 {(1, 0, 4), (0, 0, 2), (0, 2, 0)},
                                                 {(1, 0, 4), (1, 1, 3), (0, 2, 0)},
                                                 {(1, 0, 4), (1, 1, 3), (1, 2, 3)},
                                                 {(1, 0, 4), (0, 1, 0), (1, 2, 3)},
                                                 {(0, 0, 2), (1, 1, 3), (0, 1, 0), (0, 2, 0)}])

        picture = [[1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0]]
        self.assertIn(generate_puzzle(picture), [
            {(0, 5, 6), (1, 4, 0), (1, 5, 0), (2, 2, 4), (2, 0, 4), (2, 3, 4), (2, 5, 0), (2, 1, 4)},
            {(0, 0, 6), (0, 1, 6), (0, 2, 6), (0, 3, 6), (0, 4, 6), (0, 5, 6), (2, 0, 4), (2, 5, 0)}])