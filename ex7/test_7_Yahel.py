from unittest import TestCase
from unittest.mock import patch

from ex7 import*


def mock_function(func):
    def wrapper(*args):
        return func(*args)
    return wrapper


class TestEx7Functional(TestCase):
    def setUp(self) -> None:
        self.move_counter = 0

    def test_mult_positive(self):
        self.assertEqual(1.0, mult(1.0, 1))
        self.assertEqual(12.0, mult(3.0, 4))
        self.assertEqual(12.4, mult(3.1, 4))
        self.assertEqual(1000.0, mult(10.0, 100))
        self.assertEqual(0.0, mult(1.0, 0))
        self.assertEqual(-4.0, mult(-1.0, 4))
        self.assertEqual(0.0, mult(0.0, 0))
        self.assertEqual(0.0, mult(0.0, 1))
        self.assertEqual(float, type(mult(1.0, 0)))
        self.assertEqual(float, type(mult(0.0, 0)))

    def test_is_even(self):
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(8))
        self.assertFalse(is_even(9))
        self.assertFalse(is_even(101))
        self.assertFalse(is_even(479))
        self.assertTrue(is_even(480))
        self.assertEqual(bool, type(is_even(101)))

    def test_log_mult(self):
        self.assertEqual(1.0, log_mult(1.0, 1))
        self.assertEqual(-1.0, log_mult(-1.0, 1))
        # self.assertEqual(-1.0, log_mult(1.0, -1
        # ))
        # self.assertEqual(1.0, log_mult(-1.0, -1))
        self.assertEqual(12.0, log_mult(3.0, 4))
        self.assertEqual(12.4, log_mult(3.1, 4))
        self.assertEqual(1000.0, log_mult(10.0, 100))
        self.assertEqual(0.0, log_mult(1.0, 0))
        self.assertEqual(0.0, log_mult(0, 0))
        self.assertEqual(0.0, log_mult(0, 1))
        self.assertEqual(float, type(log_mult(1.0, 0)))

    def test_is_power(self):
        self.assertEqual(False, is_power(10, 0))
        self.assertEqual(False, is_power(0, 10))
        self.assertEqual(True, is_power(0, 0))
        self.assertEqual(True, is_power(0, 1))
        self.assertEqual(True, is_power(10, 100))
        self.assertEqual(False, is_power(100, 10000000))
        self.assertEqual(True, is_power(100, 1))
        self.assertEqual(bool, type(is_power(100, 1)))

    def test_reverse(self):
        self.assertEqual('ortni', reverse('intro'))
        self.assertEqual('ba', reverse('ab'))
        self.assertEqual('b', reverse('b'))
        self.assertEqual('', reverse(''))
        self.assertEqual(str, type(reverse('b')))

    def test_hanoi(self):
        class Hanoi:
            @staticmethod
            def move(s, t):
                self.move_counter += 1
                item = s.pop()
                last = t[-1] if len(t) > 0 else item
                self.assertGreaterEqual(last, item, "Tried adding a bigger disc than the last disc in the stack")
                t.append(item)

        def run_game(discs):
            self.move_counter = 0
            src, dst, temp = list(range(discs, 0, -1)), [], []
            play_hanoi(Hanoi, discs, src, dst, temp)
            self.assertEqual([], src)
            self.assertEqual(list(range(discs, 0, -1)), dst)
            self.assertEqual([], temp)
            self.assertEqual(self.move_counter, (2 ** discs) - 1, "Not fast enough")

        for i in range(15):
            run_game(i)

    def test_number_of_ones(self):
        self.assertEqual(1, number_of_ones(1))
        self.assertEqual(2, number_of_ones(10))
        self.assertEqual(4, number_of_ones(11))
        self.assertEqual(6, number_of_ones(13))
        self.assertEqual(12, number_of_ones(20))
        self.assertEqual(20, number_of_ones(99))
        self.assertEqual(140, number_of_ones(199))
        self.assertEqual(164, number_of_ones(311))
        self.assertEqual(int, type(number_of_ones(1)))

    def test_compare_2d_lists(self):
        self.assertEqual(True, compare_2d_lists([], []))
        self.assertEqual(True, compare_2d_lists([[]], [[]]))
        self.assertEqual(False, compare_2d_lists([[], []], [[]]))
        self.assertEqual(False, compare_2d_lists([[]], [[], []]))
        self.assertEqual(False, compare_2d_lists([], [[]]))
        self.assertEqual(False, compare_2d_lists([[]], []))
        self.assertEqual(False, compare_2d_lists([[1, 2, 3], [], [3, 4, 5]], [[]]))
        self.assertEqual(False, compare_2d_lists([[1, 2, 3]], [[], [2]]))
        self.assertEqual(False, compare_2d_lists([[100, 0]], [[1, 4, 5]]))
        self.assertEqual(True, compare_2d_lists([[1, 2, 3], [4], [9, 7, 5, 8]], [[1, 2, 3], [4], [9, 7, 5, 8]]))
        self.assertEqual(True, compare_2d_lists([[1]], [[1]]))
        self.assertEqual(False, compare_2d_lists([[1, 2]], [[1, 3]]))
        self.assertEqual(bool, type(compare_2d_lists([[]], [])))
    #
    def test_magic_list(self):
        self.assertEqual([], magic_list(0))
        self.assertEqual([[]], magic_list(1))
        self.assertEqual([[], [[]]], magic_list(2))
        self.assertEqual([[], [[]], [[], [[]]]], magic_list(3))
        self.assertEqual([
            [],
            [[]],
            [[], [[]]],
            [[], [[]], [[], [[]]]],
            [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]]],
            [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]]]],
            [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]]]]],
            [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]], [[], [[]], [[], [[]]], [[], [[]], [[], [[]]]]]]]]
        ], magic_list(8))
        self.assertEqual(list, type(magic_list(0)))


class TestEx7Complexity(TestCase):
    def test_mult_complexity(self):
        mock_mult = mock_function(mult)
        with patch('ex7.mult') as mc:
            mc.side_effect = mock_mult
            self.assertEqual(1000.0, mult(10.0, 100))
            self.assertEqual(100, mc.call_count)

    def test_log_mult_complexity(self):
        mock_log_mult = mock_function(log_mult)
        with patch('ex7.log_mult') as mc:
            mc.side_effect = mock_log_mult
            self.assertEqual(128.0, log_mult(2.0, 64))
            self.assertEqual(7, mc.call_count)

        with patch('ex7.log_mult') as mc:
            mc.side_effect = mock_log_mult
            self.assertEqual(4096.0, log_mult(2.0, 2048))
            self.assertEqual(12, mc.call_count)

    def test_is_power_complexity(self):
        mock_power_helper = mock_function(is_power_helper)
        mock_mult = mock_function(log_mult)
        with patch('ex7.is_power_helper') as power, patch('ex7.log_mult') as mul:
            power.side_effect = mock_power_helper
            mul.side_effect = mock_mult
            self.assertEqual(True, is_power(100, 100000000000000))
            self.assertGreaterEqual(80, mul.call_count)

    def test_reverse_complexity(self):
        mock_reverse = mock_function(execute_reverse)
        with patch('ex7.execute_reverse') as mc:
            mc.side_effect = mock_reverse
            self.assertEqual('abcdefghijklmnop', reverse('ponmlkjihgfedcba'))
            self.assertEqual(17, mc.call_count)

    # def test_magic_list_complexity(self):
    #         mock_magic_list = mock_function(magic_list)
    #         with patch('ex7.magic_list') as mc:
    #             mc.side_effect = mock_magic_list
    #             magic_list(n)
    #             self.assertEqual((2 ** (n + 1)) - 2, mc.call_count)
    #                 run_test(5)
    #                 run_test(10)