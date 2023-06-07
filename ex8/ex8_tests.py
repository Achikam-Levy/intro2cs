from puzzle_solver import *
from random import random


def test_max_seen():
    pic1 = [
        [0, 0, -1, 1],
        [0, 1, 1, 1],
        [-1, 0, -1, 0]
    ]
    pic2 = [
        [0, 0],
        [0, 0]
    ]
    pic3 = [
        [1, 1],
        [-1, 1]
    ]
    pic1_seen = [[0, 0, 4, 3],
                 [0, 3, 5, 4],
                 [1, 0, 3, 0]]
    pic4 = [
        [-1, 0, 1, -1],
        [0, 1, -1, 1],
        [1, 0, 1, 0]
    ]
    pic4_seen = [
        [1, 0, 4, 3],
        [0, 3, 5, 4],
        [1, 0, 3, 0]
    ]
    for i in range(3):
        for j in range(4):
            assert max_seen_cells(pic1, i, j) == pic1_seen[i][j]
    for i in range(2):
        for j in range(2):
            assert max_seen_cells(pic2, i, j) == 0
            assert max_seen_cells(pic3, i, j) == 3
    for i in range(3):
        for j in range(4):
            assert max_seen_cells(pic4, i, j) == pic4_seen[i][j]
    assert max_seen_cells(pic4, 0, 0) == 1
    assert max_seen_cells(pic4, 1, 0) == 0
    assert max_seen_cells(pic4, 1, 2) == 5
    assert max_seen_cells(pic4, 1, 1) == 3


def test_min_seen():
    pic1 = [
        [0, 0, -1, 1],
        [0, 1, 1, 1],
        [-1, 0, -1, 0]
    ]
    pic2 = [
        [-1, 0],
        [0, 0]
    ]
    pic3 = [
        [1, 1],
        [1, 1]
    ]
    pic1_seen = [[0, 0, 0, 2],
                 [0, 3, 3, 4],
                 [0, 0, 0, 0]]
    pic4 = [
        [-1, 0, 1, -1],
        [0, 1, -1, 1],
        [1, 0, 1, 0]
    ]
    pic4_seen = [
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0]
    ]
    for i in range(3):
        for j in range(4):
            assert min_seen_cells(pic1, i, j) == pic1_seen[i][j]
    for i in range(2):
        for j in range(2):
            assert min_seen_cells(pic2, i, j) == 0
            assert min_seen_cells(pic3, i, j) == 3
    for i in range(3):
        for j in range(4):
            assert min_seen_cells(pic4, i, j) == pic4_seen[i][j]
    assert min_seen_cells(pic4, 0, 0) == 0
    assert min_seen_cells(pic4, 1, 0) == 0
    assert min_seen_cells(pic4, 1, 2) == 0
    assert min_seen_cells(pic4, 1, 1) == 1


def test_constraints():
    pic1 = [
        [-1, 0, 1, -1],
        [0, 1, -1, 1],
        [1, 0, 1, 0]
    ]
    pic2 = [
        [0, 0, 1, 1],
        [0, 1, 1, 1],
        [1, 0, 1, 0]
    ]
    assert check_constraints(pic1, {(0, 3, 5), (1, 2, 5), (2, 0, 1)}) == 0
    assert check_constraints(pic2, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 1
    assert check_constraints(pic1, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 2


def test_solver():
    assert solve_puzzle({(0,3,3),(1,2,5),(2,0,1),(0,0,0)},3,4) == \
           [[0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0]]
    assert solve_puzzle({(0,3,3),(1,2,5),(2,0,1),(0,0,0)},3,4) == \
           [[0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0]]
    assert solve_puzzle({(0,3,3),(1,2,5),(2,0,1),(0,0,0),(2,3,5)},3,4) is None
    assert solve_puzzle({(0,2,3),(1,1,4),(2,2,5)},3,3) == [[0, 0, 1], [1, 1, 1], [1, 1, 1]]


def test_solutions():
    cnt0 = {(0,3,3),(1,2,5),(2,0,1),(2,3,5)}
    cnt1 = {(0,3,3),(1,2,5),(2,0,1),(0,0,1)}
    cnt2 = {(0,2,3),(1,1,4),(2,2,5)}
    cnt3 = {(i,j,0) for i in range(3) for j in range(3)}
    cnt4 = set()
    cnt5 = {(0,3,3),(2,0,1)}

    assert how_many_solutions(cnt0, 3, 4) == 0
    assert how_many_solutions(cnt1, 3, 4) == 1
    assert how_many_solutions(cnt2, 3, 3) == 2
    assert how_many_solutions(cnt3, 3, 3) == 1
    assert how_many_solutions(cnt4, 2, 2) == 16
    assert how_many_solutions(cnt5, 3, 4) == 64


def test_puzzle():
    pic1 = [[0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0]]
    cnt1 = generate_puzzle(pic1)
    assert how_many_solutions(cnt1, 3, 4) == 1
    assert solve_puzzle(cnt1, 3, 4) == pic1
    for i in range(1, 6):
        for j in range(1, 6):
            for _ in range(20):
                pic = random_pic(i, j)
                cnt = generate_puzzle(pic)
                sol_count = how_many_solutions(cnt, i, j)
                sol_pic = solve_puzzle(cnt, i, j)
                if not sol_count==1 or not sol_pic==pic:
                    print()
                    print(pic)
                    print(cnt)
                    print(sol_count)
                    print(sol_pic)
                assert sol_count==1 and sol_pic==pic


def random_pic(rows, cols):
    return [[round(random()) for i in range(cols)] for j in range(rows)]
