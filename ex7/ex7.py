from ex7_helper import *
from typing import Any, List


def mult(x: float, y: int) -> float:
    if y == 0:
        return 0.0
    return add(x, mult(x, subtract_1(y)))

def is_even(n: int) -> bool:
    if n == 0:
        return True
    return not is_even(subtract_1(n))


def log_mult(x: float, y: int) -> float:
    if y == 0 or x == 0:
        return 0.0
    if is_odd(y) == True:
        if y == 1:
            return x
        return add(x, log_mult(add(x, x), divide_by_2(y)))
    else:
        if y == 2:
            x = add(x, x)
            return x
        return log_mult(add(x, x), divide_by_2(y))


def is_power_helper(a: float, b: float, z: float) -> bool:
    a = int(a)
    if b > z:
        return False
    if int(b) == z:
        return True
    return is_power_helper(a, log_mult(b, a), z)


def is_power(b: int, x: int) -> bool:
    if (b == 0 and x > 1) or (x == 0 and b > 1):
        return False
    if b == 1 or x == 1 or (b == 0 and x == 0) or b == x:
        return True
    else:
        return is_power_helper(b, b, x)


def execute_reverse(s: str, c: str, z: str) -> str:
    if len(s) == len(c):
        return c
    x = add(subtract_1(len(s)), - len(c))
    return execute_reverse(s, append_to_end(c, s[x]), z)


def reverse(s: str) -> str:
    return execute_reverse(s, "", s)


def play_hanoi(Hanoi: Any, n: int, src: Any, dst: Any, temp: Any) -> Any:
    if n == 1:
        return Hanoi.move(src, dst)
    if n != 0:
        play_hanoi(Hanoi, n - 1, src, temp, dst)
        Hanoi.move(src, dst)
        play_hanoi(Hanoi, n - 1, temp, dst, src)


def _number_of_ones_helper(n: int, c: int) -> int:
    if n == 0:
        return c
    if n < 100:
        if n % 10 == 1:
            c += 1
        if n // 10 == 1:
            c += 1
    return _number_of_ones_helper(n - 1, c)


def number_of_ones(n: int) -> int:
    if n < 100:
        return _number_of_ones_helper(n, 0)
    n_99 = _number_of_ones_helper(99, 0)
    n_hundrends = 100 + (
                (n_99 * (n // 100)) + _number_of_ones_helper(n % 100, 0))
    if 99 < n < 200:
        return (n - 100) + 20 + (_number_of_ones_helper(n - 100, 0)) + 1
    if 199 < n < 1099:
        return n_hundrends
    else:
        return (n - 1099)*1 + n_99*(n // 100) + n_hundrends


def _compare_2d_numbers_helper(l1: List[int], l2: List[int], x: int) -> bool:
    if x < 0:
        return True
    if len(l1) != len(l2):
        return False
    if (l1[x]) != (l2[x]):
        return False
    else:
        return _compare_2d_numbers_helper(l1, l2, x - 1)


def _compare_2d_lists_helper(l1: List[List[int]], l2: List[List[int]], c: int) -> bool:
    y = len(l1)
    if c == 0:
        return True
    if len(l1) != len(l2):
        return False
    else:
        z = _compare_2d_numbers_helper(l1[y - c], l2[y - c],
                                       subtract_1(len(l1[y - c])))
    if z == False:
        return z
    return _compare_2d_lists_helper(l1, l2, subtract_1(c))


def compare_2d_lists(l1: List[List[int]], l2: List[List[int]]) -> bool:
    r = len(l1)
    if len(l2) > len(l1):
        r = len(l2)
    return _compare_2d_lists_helper(l1, l2, r)




def magic_list(n: int) -> List[Any]:
    empty_lst: List[Any] = []
    if n == 0:
        return empty_lst
    else:
        m_lst = magic_list(n - 1)
        m_lst.append(magic_list(n - 1))
    return m_lst

