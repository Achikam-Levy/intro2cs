######################################
# File : apple.py
# WRITER : yotam_suliman yotamsu26 206922205,aaa997 208764944
# EXERCISE intro2cs1 ex10 2021
# Students I spoke to about the exercise: none
# Web pages I used : none
######################################
from boggle_board_randomizer import randomize_board


def is_valid_path(board, path, words):
    """
    :param board: the randomize board.
    :param path: the tried path.
    :param words: list of all the relevant words.
    :return: if the path is leading to a word that in the list.
    """
    word = ""
    old_path = []
    for valid in path:
        if valid[0] >= len(board) or valid[0] < 0:
            return None
        if valid[1] >= len(board[0]) or valid[1] < 0:
            return None
    if not path:
        return None
    for p in range(len(path) - 1):
        temp_check = neighbor(len(board), len(board[0]),
                              path[p][0], path[p][1])
        if not temp_check:
            return None
        if path[p + 1] not in temp_check:
            return None
        if path[p] in old_path or path[p + 1] in old_path:
            return None
        else:
            word += board[path[p][0]][path[p][1]]
            old_path.append(path[p])
    word += board[path[-1][0]][path[-1][1]]
    if word not in words:
        return None
    return word


def neighbor(length, width, x, y):
    """
    :param length: the length of the board.
    :param width: the width of the board.
    :param x: the current col.
    :param y: the current row.
    :return: list of tuples of all the valid neighbors of the cor.
    """
    neighbor_lst = [(x + 1, y + 1), (x + 1, y - 1), (x + 1, y), (x, y + 1),
                    (x, y - 1),
                    (x - 1, y), (x - 1, y + 1), (x - 1, y - 1)]
    final_lst = []
    for t in neighbor_lst:
        if 0 <= t[0] < length and 0 <= t[1] < width:
            final_lst.append(t)
    return final_lst


def find_length_n_paths(n, board, words):
    """
    :param n: integer.
    :param board: the relevant board full of letters.
    :param words: all the words in a list of words.
    :return: all the paths in size n that leading to relevant word.
    """
    all_paths = []
    final_all_paths = []
    cor_lst = board_index(board)
    for word in words:
        find_word_path_helper(word, 0, [], all_paths, cor_lst, board)
    for index in all_paths:
        if len(index) == n:
            final_all_paths.append(index)
    return final_all_paths


def find_length_n_words(n, board, words):
    """
    :param n: integer.
    :param board: the relevant board full of letters.
    :param words: all the words in a list of words.
    :return: all the paths that leading to words in size n.
    """
    words = filter_words(n, words)
    all_paths = []
    cor_lst = board_index(board)
    for word in words:
        find_word_path_helper(word, 0, [], all_paths, cor_lst, board)
    return all_paths


def find_word_path_helper(word, index, current_path, all_paths, cor_lst,
                          board):
    """
    :param word: the current word.
    :param index: the current index.
    :param current_path: the current path,
    :param all_paths: all the paths until now.
    :param cor_lst: all the relevant neighbors.
    :param board: the relevant board full of letters.
    :return: add the paths to the list of all paths.
    """
    if index == len(word):
        if current_path not in all_paths:
            all_paths.append(current_path)
        return

    for r in range(len(board)):
        for c in range(len(board[0])):
            if word[index: len(board[r][c]) + index] == board[r][c] \
                    and (r, c) in cor_lst and (r, c) not in current_path:
                find_word_path_helper(word, index + len(board[r][c]), current_path + [(r, c)], all_paths,neighbor(len(board), len(board[0]), r, c) , board)
    return None


def list_letters(board):
    """
    :param board: the relevant board full of letters.
    :return: list of all the letters in the board.
    """
    letter_list = []
    for r in board:
        for c in r:
            letter_list.append(c)
    return letter_list


def filter_words(n, words):
    """
    :param n: integer.
    :param words: all the words that relevant.
    :return:
    """
    lst = []
    for w in words:
        if len(w) == n:
            lst.append(w)
    return lst


def filter_board_words(board, words):
    """
    :param board: the relevant board full of letters.
    :param words: all the words that relevant.
    :return: filter relevant words from the list.
    """
    check_lst = list_letters(board)
    final_lst = []
    flag = True
    for word in words:
        for l in word:
            if l not in check_lst:
                flag = False
        if flag:
            final_lst.append(word)
        flag = True
    return final_lst


def board_index(board):
    """
    :param board: the relevant board full of letters.
    :return: list of all the board indexes.
    """
    index_lst = []
    for r in range(len(board)):
        for c in range(len(board)):
            index_lst.append((r, c))
    return index_lst


def max_score_paths(board, words):
    """
    :param board: the relevant board full of letters.
    :param words: all the relevant words.
    :return: all the paths that will lead you the the max score.
    """
    total_path_lst = []
    score = 0
    for word in words:
        temp_lst = find_length_n_words(len(word), board, [word])
        if temp_lst:
            path = temp_lst[0]
            for i in temp_lst:
                if len(i) > len(path):
                    path = i
            score += len(path)**2
            total_path_lst.append(path)
    return total_path_lst


