


import matplotlib.pyplot as plt
import numpy as np
import timeit
import sys
import warnings

warnings.filterwarnings('ignore')

SIMPLE = """example:
log_mult(987,%s)
%s mark the n we want to test for
this call will time the function log_mult(987, n)

*the timer fluctuates, so you should not trust the outcome especially if 
there are major jumps*"""
ADVANCED = """example:
log_mult(987,%s) 763
test for n in range(1,763)
default value is 1000
"""
AADVANCED = """example:
log_mult(987,%s) 1000 8 1 0 10000
func_call N ROUNDS SMOOTH EXP recursion_limit
func_call: log_mult(987,%s)
N: time for range(1,N)
ROUNDS: how many rounds to time each n
SMOOTH: if to smooth measured time in graph (1/0)
EXP: if to plot O(2^n) on graph (1/0)
all parameters above are int
(warning: is much larger than all other times
recursion_limit: setting for python recursion limit
Note: values in example are used as defaults"""
GENERAL = """enter help for help
enter examples for examples
enter exit for exit :)
enter a for advanced user guide
enter aa for very advance (only if you know what your doing)"""
EXAMPLES = """mult(34.2,%s)
is_even(%s)
log_mult(546.2,%s)
is_power(2,%s)
is_power(%s,1000)
reverse(%s)
number_of_ones(%s)
compare_2d_lists(%s,%s) 
magic_list(%s)

*you can test any other function that receives parameter n: int*
*will not work for hanoi, or other functions that receive lists or str"""


def build_2d_list(n):
    return [[0]*50 for _ in range(n)]


def top10(arr):
    return np.average(arr[len(arr) * 9 // 10:])


def time_code(func_call: str, N: int, ROUNDS: int = 4):
    """
    :param func_call: 'log_mult(987, %s)'
    :param N: 5000
    """
    time_series = []
    func_name = func_call.split('(')[0]
    if func_name == 'compare_2d_lists':
        print('the total number of values in both lists is n')
    for n in range(1, N):
        if func_name == 'reverse':
            param = "'" + "x" * n + "'"
        # elif func_name == 'play_hanoi':
        #     pass # TODO call "hanoi_game.play_hanoi(...)"
        elif func_name == 'compare_2d_lists':
            param = (build_2d_list(n), build_2d_list(n))
        else:
            param = n
        t = timeit.Timer(stmt="ex7." + func_call % param, setup="import ex7")
        time_series.append(t.timeit(ROUNDS)/ROUNDS)
    return np.array(time_series)


def plot_complexity(func_call: str, N: int = 1000, ROUNDS: int = 4,
                    SMOOTH: bool = True, EXP: bool = False,
                    recursion_limit: int = 10000) -> None:
    """
    examples for parameters:
    :param func_call:
    :param N: 5000
    """
    base_recursion_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(recursion_limit)
    KERNEL = N // 50 + 1

    o_1 = np.ones(N)
    o_log_n = np.log(np.arange(N))
    o_n = np.arange(N)
    o_n_log_n = o_n * o_log_n
    o_n_2 = o_n * o_n
    time_complexity = {'O(1)': o_1, 'O(log n)': o_log_n, 'O(n)': o_n,
                       'O(n log n)': o_n_log_n, 'O(n^2)': o_n_2}
    time_series = time_code(func_call, N, ROUNDS)
    limit = top10(time_series)
    if SMOOTH:
        plt.plot(np.convolve(time_series / limit, np.ones(KERNEL) / KERNEL,
                             mode='valid'))
    else:
        plt.plot(time_series / limit)
    lg = ['code']
    for key in time_complexity.keys():
        ratio = top10(time_complexity[key])
        plt.plot(time_complexity[key] / ratio)
        lg.append(key)
    if EXP:
        o_2_n = np.exp2(o_n)
        ratio = o_2_n[-1]
        plt.plot(o_2_n / ratio)
        lg.append('O(2^n)')

    plt.title(func_call)
    plt.xlabel('n')
    plt.ylabel('sec/%f' % limit)
    plt.legend(lg)
    plt.show()

    sys.setrecursionlimit(base_recursion_limit)


if __name__ == '__main__':
    mode = input(GENERAL)
    if mode == 'a':
        print(ADVANCED)
    elif mode == 'aa':
        print(AADVANCED)
    elif mode == 'examples':
        print(EXAMPLES)
    else:
        print(SIMPLE)
    while True:
        user_input = input('Enter new call: ')
        if user_input == 'exit':
            break
        elif user_input == 'a':
            print(ADVANCED)
        elif user_input == 'aa':
            print(AADVANCED)
        elif user_input == 'help':
            print(SIMPLE)
        elif user_input == 'examples':
            print(EXAMPLES)
        else:
            params = user_input.split(')')
            try:
                if len(params[1]) == 0:
                    plot_complexity(params[0]+')')
                else:
                    plot_complexity(params[0]+')', *[int(p) for p in params[
                                                                     1:]])
            except:
                print('incorrect input')
