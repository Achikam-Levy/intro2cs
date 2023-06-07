from unittest import TestCase, mock

from board import Board
from car import Car
# Change the init_board to be your function for initializing the board/game (If you implemented all in the main,
# extract it out to another function, this is the only way to test the logic)
from game import main, initial_board, Game

init_board_func = initial_board


class TestRushHour(TestCase):
    ######### CAR #########
    def test_car_name(self):
        c = Car('Y', length=1, location=(0, 0), orientation=0)
        self.assertEqual('Y', c.get_name())
        c = Car('Yoyoyo', length=1, location=(0, 0), orientation=0)
        self.assertEqual('Yoyoyo', c.get_name())

    def test_car_coordinates(self):
        c = Car('car', length=1, location=(0, 0), orientation=0)
        self.assertEqual([(0, 0)], c.car_coordinates())
        c = Car('car', length=3, location=(0, 0), orientation=0)
        self.assertEqual([(0, 0), (1, 0), (2, 0)], c.car_coordinates())
        c = Car('car', length=3, location=(-1, 0), orientation=0)
        self.assertEqual([(-1, 0), (0, 0), (1, 0)], c.car_coordinates())
        c = Car('car', length=3, location=(-1, 0), orientation=1)
        self.assertEqual([(-1, 0), (-1, 1), (-1, 2)], c.car_coordinates())
        c = Car('car', length=3, location=(2, 5), orientation=0)
        self.assertEqual([(2, 5), (3, 5), (4, 5)], c.car_coordinates())
        c = Car('car', length=3, location=(2, 5), orientation=1)
        self.assertEqual([(2, 5), (2, 6), (2, 7)], c.car_coordinates())

    def test_car_length(self):
        c = Car('car', length=-1, location=(0, 0), orientation=0)
        self.assertEqual(0, len(c.car_coordinates()))
        c = Car('car', length=-1, location=(0, 0), orientation=1)
        self.assertEqual(0, len(c.car_coordinates()))
        c = Car('car', length=-2, location=(2, 2), orientation=0)
        self.assertEqual(0, len(c.car_coordinates()))
        c = Car('car', length=7, location=(2, 2), orientation=0)
        self.assertEqual(7, len(c.car_coordinates()))
        c = Car('car', length=7, location=(2, 2), orientation=1)
        self.assertEqual(7, len(c.car_coordinates()))

    def test_car_orientation(self):
        c = Car('car', length=2, location=(0, 0), orientation=0)
        self.assertEqual([(0, 0), (1, 0)], c.car_coordinates())
        c = Car('car', length=2, location=(0, 0), orientation=1)
        self.assertEqual([(0, 0), (0, 1)], c.car_coordinates())
        c = Car('car', length=2, location=(0, 0), orientation=3)
        self.assertEqual([], c.car_coordinates())
        self.assertEqual({}, c.possible_moves())
        c = Car('car', length=2, location=(0, 0), orientation=2)
        self.assertEqual([], c.car_coordinates())
        self.assertEqual({}, c.possible_moves())

    def test_possible_moves(self):
        c = Car('car', length=0, location=(0, 0), orientation=0)
        self.assertEqual([], list(c.possible_moves().keys()))
        c = Car('car', length=2, location=(0, 0), orientation=0)
        self.assertEqual(['d', 'u'], sorted(list(c.possible_moves().keys())))
        c = Car('car', length=2, location=(0, 0), orientation=1)
        self.assertEqual(['l', 'r'], sorted(list(c.possible_moves().keys())))

    def test_movement_requirements(self):
        c = Car('car', length=0, location=(0, 0), orientation=0)
        self.assertEqual([], c.movement_requirements('u'))
        c = Car('car', length=1, location=(0, 0), orientation=0)
        self.assertEqual([(-1, 0)], c.movement_requirements('u'))
        self.assertEqual([(1, 0)], c.movement_requirements('d'))
        self.assertEqual([], c.movement_requirements('r'))
        self.assertEqual([], c.movement_requirements('l'))
        self.assertEqual([], c.movement_requirements('f'))
        self.assertEqual([], c.movement_requirements('s'))
        c = Car('car', length=1, location=(0, 0), orientation=1)
        self.assertEqual([(0, 1)], c.movement_requirements('r'))
        self.assertEqual([(0, -1)], c.movement_requirements('l'))
        self.assertEqual([], c.movement_requirements('u'))
        self.assertEqual([], c.movement_requirements('d'))
        self.assertEqual([], c.movement_requirements('gggg'))
        c = Car('car', length=7, location=(0, 0), orientation=1)
        self.assertEqual([(0, 7)], c.movement_requirements('r'))

    def test_move(self):
        c = Car('car', length=1, location=(0, 0), orientation=0)
        self.assertTrue(c.move('u'))
        self.assertEqual([(-1, 0)], c.car_coordinates())
        self.assertTrue(c.move('d'))
        self.assertEqual([(0, 0)], c.car_coordinates())
        self.assertFalse(c.move('r'))
        self.assertFalse(c.move('l'))
        self.assertFalse(c.move('zz'))
        self.assertEqual([(0, 0)], c.car_coordinates())

        c = Car('car', length=3, location=(3, 4), orientation=1)
        self.assertFalse(c.move('u'))
        self.assertFalse(c.move('d'))
        self.assertFalse(c.move('zz'))
        self.assertTrue(c.move('r'))
        self.assertEqual([(3, 5), (3, 6), (3, 7)], c.car_coordinates())
        self.assertTrue(c.move('r'))
        self.assertEqual([(3, 6), (3, 7), (3, 8)], c.car_coordinates())
        self.assertTrue(c.move('l'))
        self.assertEqual([(3, 5), (3, 6), (3, 7)], c.car_coordinates())

        c = Car('car', length=3, location=(3, 4), orientation=2)
        self.assertFalse(c.move('l'))
        self.assertFalse(c.move('r'))
        self.assertFalse(c.move('u'))
        self.assertFalse(c.move('d'))
        self.assertEqual([], c.car_coordinates())

    ######### BOARD #########
    def test_board_cell_list(self):
        b = Board()
        cells = b.cell_list()
        self.assertEqual(7 * 7 + 1, len(cells))
        self.assertIn((3, 7), cells)
        cells.remove((3, 7))
        self.assertTrue(all(
            map(lambda cell: 0 <= cell[0] < 7 and 0 <= cell[1] < 7, cells)
        ))

    def test_board_cell_content(self):
        b = Board()
        cells = b.cell_list()
        for cell in cells:
            self.assertIsNone(b.cell_content(cell))
        self.assertIsNone(b.cell_content((-1, -1)))
        self.assertIsNone(b.cell_content((-1, 0)))
        self.assertIsNone(b.cell_content((0, -1)))
        self.assertIsNone(b.cell_content((7, 2)))
        self.assertIsNone(b.cell_content((4, 7)))
        self.assertIsNone(b.cell_content((8, 8)))
        c = Car('YXX', length=2, location=(2, 4), orientation=0)
        self.assertTrue(b.add_car(c))
        self.assertEqual(['YXX', 'YXX'], [b.cell_content((2, 4)), b.cell_content((3, 4))])
        c = Car('Y', length=2, location=(1, 4), orientation=1)
        self.assertTrue(b.add_car(c))
        self.assertEqual(['YXX', 'YXX'], [b.cell_content((2, 4)), b.cell_content((3, 4))])
        self.assertEqual(['Y', 'Y'], [b.cell_content((1, 4)), b.cell_content((1, 5))])
        c = Car('G', length=2, location=(3, 6), orientation=1)
        self.assertTrue(b.add_car(c))
        self.assertEqual('G', b.cell_content((3, 7)))

    def test_board_add_car(self):
        b = Board()
        c = Car('Y', length=2, location=(1, 4), orientation=1)
        self.assertTrue(b.add_car(c))
        self.assertTrue(all(map(lambda coordinate: b.cell_content(coordinate) == 'Y', c.car_coordinates())))
        c = Car('X', length=2, location=(1, 4), orientation=1)
        self.assertFalse(b.add_car(c))
        c = Car('X', length=2, location=(1, 3), orientation=1)
        self.assertFalse(b.add_car(c))
        c = Car('X', length=2, location=(-1, -1), orientation=1)
        self.assertFalse(b.add_car(c))
        c = Car('X', length=8, location=(0, 0), orientation=1)
        self.assertFalse(b.add_car(c))
        c = Car('Z', length=7, location=(0, 0), orientation=1)
        self.assertTrue(b.add_car(c))
        c = Car('D', length=6, location=(1, 0), orientation=0)
        self.assertTrue(b.add_car(c))
        c = Car('B', length=5, location=(4, 4), orientation=0)
        self.assertFalse(b.add_car(c))
        c = Car('B', length=5, location=(4, 4), orientation=2)
        self.assertTrue(b.add_car(c))
        self.assertEqual(None, b.cell_content((4, 4)))
        c = Car('C', length=0, location=(4, 4), orientation=2)
        self.assertTrue(b.add_car(c))
        self.assertEqual(None, b.cell_content((4, 4)))

    def test_board_possible_moves(self):
        def remove_descriptions(moves):
            return sorted(list(map(lambda m: (m[0], m[1]), moves)))
        b = Board()
        c = Car('A', length=2, location=(0, 0), orientation=1)
        b.add_car(c)
        self.assertListEqual([('A', 'r')], remove_descriptions(b.possible_moves()))
        c = Car('B', length=2, location=(1, 1), orientation=1)
        b.add_car(c)
        self.assertListEqual([('A', 'r'), ('B', 'l'), ('B', 'r')], remove_descriptions(b.possible_moves()))

        b = Board()
        c = Car('A', length=2, location=(0, 0), orientation=0)
        b.add_car(c)
        self.assertListEqual([('A', 'd')], remove_descriptions(b.possible_moves()))
        c = Car('B', length=2, location=(1, 1), orientation=0)
        b.add_car(c)
        self.assertListEqual([('A', 'd'), ('B', 'd'), ('B', 'u')], remove_descriptions(b.possible_moves()))

        b = Board()
        b.add_car(Car('A', length=2, location=(0, 0), orientation=0))
        b.add_car(Car('B', length=3, location=(4, 3), orientation=1))
        b.add_car(Car('C', length=2, location=(5, 3), orientation=0))
        self.assertListEqual([('A', 'd'), ('B', 'l'), ('B', 'r')], remove_descriptions(b.possible_moves()))

        b = Board()
        b.add_car(Car('A', length=2, location=(3, 5), orientation=1))
        self.assertListEqual([('A', 'l'), ('A', 'r')], remove_descriptions(b.possible_moves()))

        b = Board()
        b.add_car(Car('A', length=0, location=(0, 0), orientation=1))
        b.add_car(Car('B', length=2, location=(3, 0), orientation=2))
        self.assertListEqual([], remove_descriptions(b.possible_moves()))

    def test_board_move_car(self):
        b = Board()
        c = Car('A', length=2, location=(0, 0), orientation=1)
        b.add_car(c)
        self.assertTrue(b.move_car('A', 'r'))
        self.assertIsNone(b.cell_content((0, 0)))
        self.assertEqual('A', b.cell_content((0, 2)))
        self.assertEqual([(0, 1), (0, 2)], c.car_coordinates())
        self.assertFalse(b.move_car('A', 'd'))
        self.assertTrue(b.move_car('A', 'l'))
        self.assertFalse(b.move_car('A', 'l'))
        self.assertEqual([(0, 0), (0, 1)], c.car_coordinates())

        self.assertFalse(b.move_car('Whhat', 'd'))
        c2 = Car('B', length=2, location=(1, 1), orientation=0)
        b.add_car(c2)
        self.assertFalse(b.move_car('B', 'u'))
        self.assertEqual([(1, 1), (2, 1)], c2.car_coordinates())
        self.assertTrue(b.move_car('B', 'd'))
        self.assertEqual([(2, 1), (3, 1)], c2.car_coordinates())

        v = Car('C', length=5, location=(3, 2), orientation=1)
        b.add_car(v)
        self.assertFalse(b.move_car('C', 'l'))
        self.assertEqual([(3, 2), (3, 3), (3, 4), (3, 5), (3, 6)], v.car_coordinates())
        self.assertTrue(b.move_car('C', 'r'))
        self.assertEqual([(3, 3), (3, 4), (3, 5), (3, 6), (3, 7)], v.car_coordinates())
        self.assertTrue(b.move_car('C', 'l'))

        u = Car('Winner', length=1, location=(3, 7), orientation=0)
        b.add_car(u)
        self.assertFalse(b.move_car('C', 'l'))
        self.assertEqual([(3, 2), (3, 3), (3, 4), (3, 5), (3, 6)], v.car_coordinates())
        self.assertEqual([(3, 7)], u.car_coordinates())

    def test_board_target_location(self):
        b = Board()
        self.assertEqual((3, 7), b.target_location())

    def test_board_print(self):
        b = Board()
        self.assertIsNotNone(str(b))
        self.assertIsInstance(str(b), str)

    ######### GAME #########
    def initialize_board(self, board_configuration):
        """ Substitutes the json with the given configuration """
        with mock.patch('game.load_json', lambda x: board_configuration), \
                mock.patch('game.sys.argv', ['python', 'game', 'config']):
            return init_board_func()

    def test_game_initialization(self):
        board = self.initialize_board({
            'Y': [2, [0, 0], 0],
            'B': [1, [0, 1], 0], # Length smaller than allowed
            'O': [5, [0, 2], 0], # Length bigger than allowed
            'D': [2, [0, 3], 0], # Name not allowed
            'W': [2, [0, 4], 3], # Orientation not allowed
        })
        self.assertEqual([
            'Y', 'Y',
            None,
            None, None, None, None, None,
            None, None,
            None, None],
            [board.cell_content(cell) for cell in [
                (0, 0), (1, 0),
                (0, 1),
                (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
                (0, 3), (1, 3),
                (0, 4), (1, 4)
            ]])
        board = self.initialize_board({
            'Y': [2, [0, 0], 0],
            'B': [3, [3, 2], 1],
            'O': [4, [1, 6], 0],
            'W': [2, [6, 0], 1],
            'G': [2, [5, 0], 1],
            'R': [3, [4, 3], 1],
        })
        self.assertEqual([
            'Y', 'Y',
            'B', 'B', 'B',
            'O', 'O', 'O', 'O',
            'W', 'W',
            'G', 'G',
            'R', 'R', 'R'
        ], [
            board.cell_content(cell) for cell in [
                (0, 0), (1, 0),
                (3, 2), (3, 3), (3, 4),
                (1, 6), (2, 6), (3, 6), (4, 6),
                (6, 0), (6, 1),
                (5, 0), (5, 1),
                (4, 3), (4, 4), (4, 5)
            ]])

    def play_game(self, game, inputs):
        counter = 0

        def mock_input(prompt):
            nonlocal counter
            val = inputs[counter]
            print(prompt, val)
            counter += 1
            return val

        with mock.patch('game.input', mock_input):
            game.play()
        return len(inputs) - counter

    def test_game_user_input_negative(self):
        board = self.initialize_board({
            'Y': [2, [0, 0], 0],
            'B': [3, [3, 2], 1]
        })
        game = Game(board=board)
        inputs_left = self.play_game(game, ['Y,r,l', 'Y,rr', 'XX,r', 'Y , r', '    ', '!']) # length of input is wrong
        self.assertEqual(0, inputs_left)
        self.assertEqual(['Y', 'Y'], [board.cell_content((0, 0)), board.cell_content((1, 0))]) # check unchanged

        inputs_left = self.play_game(game, ['Yd', 'Y d', '!']) # wrong format
        self.assertEqual(0, inputs_left)
        self.assertEqual(['Y', 'Y'], [board.cell_content((0, 0)), board.cell_content((1, 0))]) # check unchanged

        inputs_left = self.play_game(game, ['O,r', 'Y,r', 'Y,l', 'Y,u', 'B,u', 'B,d', '!'])  # wrong names / actions
        self.assertEqual(0, inputs_left)
        self.assertEqual(['Y', 'Y'], [board.cell_content((0, 0)), board.cell_content((1, 0))])  # check unchanged
        self.assertEqual(['B', 'B', 'B'], [board.cell_content((3, 2)), board.cell_content((3, 3)),
                                           board.cell_content((3, 4))])  # check unchanged

    def test_game_user_input_positive(self):
        board = self.initialize_board({
            'Y': [2, [0, 0], 0],
            'B': [3, [3, 2], 1]
        })
        game = Game(board=board)
        inputs_left = self.play_game(game, ['Y,d', 'B,r', '!'])
        self.assertEqual(0, inputs_left)
        self.assertEqual(['Y', 'Y'], [board.cell_content((1, 0)), board.cell_content((2, 0))])  # check changed
        self.assertEqual(['B', 'B', 'B'], [board.cell_content((3, 3)), board.cell_content((3, 4)),
                                           board.cell_content((3, 5))])  # check changed

        board = self.initialize_board({
            'Y': [2, [0, 0], 0],
            'B': [3, [3, 2], 1]
        })
        game = Game(board=board)
        inputs_left = self.play_game(game, ['Y,d', 'Y,r', 'B,l', 'D,   l', '!']) # positive and negative
        self.assertEqual(0, inputs_left)
        self.assertEqual(['Y', 'Y'], [board.cell_content((1, 0)), board.cell_content((2, 0))])  # check changed
        self.assertEqual(['B', 'B', 'B'], [board.cell_content((3, 1)), board.cell_content((3, 2)),
                                           board.cell_content((3, 3))])  # check changed

    def test_game_win(self):
        board = self.initialize_board({
            'Y': [2, [0, 0], 0],
            'B': [3, [3, 4], 1]
        })
        game = Game(board=board)
        inputs_left = self.play_game(game, ['Y,d', 'B,r']) # the game should exit here
        self.assertEqual(0, inputs_left)
        self.assertEqual(['Y', 'Y'], [board.cell_content((1, 0)), board.cell_content((2, 0))])  # check changed
        self.assertEqual(['B', 'B', 'B'], [board.cell_content((3, 5)), board.cell_content((3, 6)),
                                           board.cell_content((3, 7))])  # check changed

    def test_full_run(self):
        counter = 0
        inputs = ['Y,d', 'B,l', 'B,r', 'B,r']

        def mock_input(prompt):
            nonlocal counter, inputs
            val = inputs[counter]
            print(prompt, val)
            counter += 1
            return val

        with mock.patch('game.load_json', lambda x: {
            'Y': [2, [0, 0], 0],
            'B': [3, [3, 4], 1]
        }), mock.patch('sys.argv', ['python', 'game', 'mock']), mock.patch('game.input', mock_input):
            main()
        self.assertEqual(counter, len(inputs))