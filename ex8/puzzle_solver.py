import copy
from typing import List, Tuple, Set, Optional

# We define the types of a partial picture and a constraint (for type checking)
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def num_seen_column_down(picture: Picture, row: int, col: int) -> int:
    c = 0
    while row <= len(picture) - 1 and col <= len(picture[0]) - 1:
        row += 1
        if row <= len(picture) - 1 and col <= len(picture[0]) - 1:
            if picture[row][col] == 1:
                c += 1
            else:
                break
    return c


def num_seen_column_up(picture: Picture, row: int, col: int) -> int:
    c = 0
    while row >= 0 and col <= len(picture[0]) - 1:
        row -= 1
        if row >= 0 and col <= len(picture[0]) - 1:
            if picture[row][col] == 1:
                c += 1
            else:
                break
    return c


def num_seen_column(picture: Picture, row: int, col: int) -> int:
    c = (num_seen_column_down(picture, row, col) + num_seen_column_up(picture,
                                                                      row,
                                                                      col))
    return c


def num_seen_row_right(picture: Picture, row: int, col: int) -> int:
    c = 0
    while row <= len(picture) - 1 and col <= len(picture[0]) - 1:
        col += 1
        if row <= len(picture) - 1 and col <= len(picture[0]) - 1:
            if picture[row][col] == 1:
                c += 1
            else:
                break
    return c


def num_seen_row_left(picture: Picture, row: int, col: int) -> int:
    c = 0
    while row <= len(picture) - 1 and col >= 0:
        col -= 1
        if row <= len(picture) - 1 and col >= 0:
            if picture[row][col] == 1:
                c += 1
            else:
                break
    return c


def num_seen_row(picture: Picture, row: int, col: int) -> int:
    c = (num_seen_row_right(picture, row, col) + num_seen_row_left(picture,
                                                                   row, col))
    return c


def num_seen_column_down_max(picture: Picture, row: int, col: int) -> int:
    c = 0
    while row <= len(picture) - 1 and col <= len(picture[0]) - 1:
        row += 1
        if row <= len(picture) - 1 and col <= len(picture[0]) - 1:
            if picture[row][col] == 1 or picture[row][col] == -1:
                c += 1
            else:
                break
    return c


def num_seen_column_up_max(picture: Picture, row: int, col: int) -> int:
    c = 0
    while row >= 0 and col <= len(picture[0]) - 1:
        row -= 1
        if row >= 0 and col <= len(picture[0]) - 1:
            if picture[row][col] == 1 or picture[row][col] == -1:
                c += 1
            else:
                break
    return c


def num_seen_column_max(picture: Picture, row: int, col: int) -> int:
    c = (num_seen_column_down_max(picture, row, col) + num_seen_column_up_max(
        picture, row, col))
    return c


def num_seen_row_right_max(picture: Picture, row: int, col: int) -> int:
    c = 0
    while row <= len(picture) - 1 and col <= len(picture[0]) - 1:
        col += 1
        if row <= len(picture) - 1 and col <= len(picture[0]) - 1:
            if picture[row][col] == 1 or picture[row][col] == -1:
                c += 1
            else:
                break
    return c


def num_seen_row_left_max(picture: Picture, row: int, col: int) -> int:
    c = 0
    while row <= len(picture) - 1 and col >= 0:
        col -= 1
        if row <= len(picture) - 1 and col >= 0:
            if picture[row][col] == 1 or picture[row][col] == -1:
                c += 1
            else:
                break
    return c


def num_seen_row_max(picture: Picture, row: int, col: int) -> int:
    c = (num_seen_row_right_max(picture, row, col) + num_seen_row_left_max(
        picture, row, col))
    return c


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """
    check the number of seen cells including -1
    :param picture: innit picture
    :param row: current row
    :param col: current col
    :return: number of seen cells
    """
    if picture[row][col] == 0:
        return 0
    if picture[row][col] == 1 or picture[row][col] == -1:
        c = num_seen_row_max(picture, row, col) + num_seen_column_max(picture,
                                                                      row, col)
        return c + 1


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """
        check the number of seen cells not include -1
        :param picture: innit picture
        :param row: current row
        :param col: current col
        :return: number of seen cells
        """
    if picture[row][col] == 0 or picture[row][col] == - 1:
        return 0
    if picture[row][col] == 1:
        c = num_seen_row(picture, row, col) + num_seen_column(picture, row,
                                                              col)
        return c + 1


def check_constraints(picture: Picture,
                      constraints_set: Set[Constraint]) -> int:
    """
    check a lis of constrains in picture
    :param picture: a picture
    :param constraints_set: set of constrains
    :return: value from(0,1,2) according tot tha constrains
    """
    value = 1
    for i in constraints_set:
        row = i[0]
        column = i[1]
        constraint = i[2]
        max_cells = max_seen_cells(picture, row, column)
        min_cells = min_seen_cells(picture, row, column)
        if max_cells == min_cells and max_cells == constraint:
            pass
        elif max_cells != min_cells and min_cells <= constraint <= max_cells:
            value = 2
        else:
            value = 0
            return value
    return value


def create_picture(n, m):
    """
    create an initial picture with -1 values
    :param n: row num
    :param m: columns num
    :return: a picture with n rows and m columns, all values = -1
    """
    lst = []
    for column in range(n):
        n_lst = []
        for row in range(m):
            n_lst.append(-1)
        lst.append(n_lst)
    return lst


def good_to_place(picture, constraints_set, n, row, column):
    """
    check if a value is ok to place in a given coordinate,
     according to the constrains set
    :param picture: current picture
    :param constraints_set: constraints_set
    :param n: the value
    :param row: row
    :param column: column
    :return: bool value
    """
    new_picture = copy.deepcopy(picture)
    new_picture[row][column] = n
    if check_constraints(new_picture, constraints_set) != 0:
        return True
    else:
        return False


def solve_puzzle_helper(innit_picture: Picture,
                        constraints_set: Set[Constraint],
                        n: int, m: int, ind) -> Optional[Picture]:
    """
    the helper function to solve a puzzle
    :param innit_picture: a picture with n rows and m columns, all values = -1
    :param constraints_set: constraints_set
    :param n: rows
    :param m: columns
    :param ind: a changing index
    :return: solved puzzle
    """
    if ind == (n * m):
        return innit_picture

    row, column = ind // m, ind % m

    if innit_picture[row][column] != -1:
        solve_puzzle_helper(innit_picture, constraints_set, n, m, ind + 1)
        return

    for value in range(2):
        if good_to_place(innit_picture, constraints_set, value, row, column):
            innit_picture[row][column] = value
            if solve_puzzle_helper(innit_picture, constraints_set, n, m,
                                   ind + 1) is not None:
                return innit_picture
            innit_picture[row][column] = - 1


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[
    Picture]:
    """
    the main function
    :param constraints_set: constraints_set
    :param n: rows
    :param m: columns
    :return: solved puzzle
    """
    innit_picture = create_picture(n, m)
    return solve_puzzle_helper(innit_picture, constraints_set, n, m, 0)


def how_many_solutions_helper(innit_picture: Picture,
                              constraints_set: Set[Constraint],
                              n: int, m: int, ind) -> int:
    """
    the helper function to find a number of solutions of a puzzle
    :param innit_picture: a picture with n rows and m columns, all values = -1
    :param constraints_set: constraints_set
    :param n: rows
    :param m: columns
    :param ind: a changing index
    :return: number of solutions of a puzzle
    """
    if ind == (n * m):
        return 1

    row, column = ind // m, ind % m

    c = 0

    if innit_picture[row][column] != -1:
        solve_puzzle_helper(innit_picture, constraints_set, n, m, ind + 1)

    for value in range(2):
        if good_to_place(innit_picture, constraints_set, value, row, column):
            innit_picture[row][column] = value
            c += how_many_solutions_helper(innit_picture, constraints_set, n,
                                           m, ind + 1)
            innit_picture[row][column] = - 1
    return c


def how_many_solutions(constraints_set: Set[Tuple[int, int, int]], n: int,
                       m: int) -> int:
    """
    the main function to find a number of solutions of a puzzle
    :param constraints_set: constraints_set
    :param n: rows
    :param m: columns
    :return: number of solutions of a puzzle
    """
    innit_picture = create_picture(n, m)
    return how_many_solutions_helper(innit_picture, constraints_set, n, m, 0)


def create_constraints(picture: Picture):
    """
    create list of all the constraints of a picture
    :param picture: given picture
    :return: list of all the constraints of a picture
    """
    constraints_set = []
    for row in range(len(picture)):
        for column in range(len(picture[0])):
            constraints_set.append(
                (row, column, min_seen_cells(picture, row, column)))
    return constraints_set


def generate_puzzle_helper(picture: Picture, constraints_set, n: int, m: int) \
        -> set:
    """
     create list of all the constrains of a picture
     :param picture:
     :param constraints_set:
     :param n: rows
     :param m: column
     :return: final constraints_set
     """
    new_constraints_set = copy.deepcopy(constraints_set)
    for constraint in new_constraints_set:
        constraints_set.remove(constraint)
        if how_many_solutions(set(constraints_set), n, m) != 1 or solve_puzzle(
                set(constraints_set), n, m) != picture:
            constraints_set.append(constraint)
    return set(constraints_set)


def generate_puzzle(picture: Picture) -> set:
    """
    the main function for generate a puzzle
    :param picture: picture
    :return: final set of constrains
    """
    full_constraints_set = create_constraints(picture)
    final_constraints_set = generate_puzzle_helper(picture,
                                                   full_constraints_set,
                                                   len(picture),
                                                   len(picture[0]))
    return final_constraints_set
