#################################################################
# FILE : largest_and_smallest.py
# WRITER : achikam levy , aaa997 , 208764944
# EXERCISE : intro2cs2 ex4 2021
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################

from hangman_helper import *

alphabet = 'abcdefghijgklmnopqrstuvwxyz'

#chosen_letters = ''

words = load_words()

#correct_letters = ''

#score = POINTS_INITIAL

wrong_guess_lst = []

def update_word_pattern(word, pattern, letter):
    """
    the function return pattern according to the parameters
    :param word:the random choise
    :param pattern: according to the letter
    :param letter: the user input
    :return: pattern
    """
    pattern = list(pattern)
    word = list(word)
    for i in range(len(word)):
        if word[i] == letter:
            pattern[i] = letter
    pattern = ''.join(pattern)
    return pattern


def reverse_update_pattern(word, letter_list):
    """
    this function makes a pattern from a word according to letter_list
    :param word: the words from word.txt
    :param letter_list: the right letter that the user guess
    :return: pattern of every word
    """
    word = list(word)
    letter_list = list(letter_list)
    for i in range(len(word)):
        if word[i] not in letter_list:
            word[i] = '_'
    word = ''.join(word)
    return word


def filter_words_list(words, pattern, wrong_guess_lst, correct_letters):
    """
    this function makes a list of optional hints
    :param words: words.txt
    :param pattern: the current pattern of the game
    :param wrong_guess_lst: wrong_guess_lst
    :param correct_letters: correct_letters list
    :return: list of the hints for the user
    """
    optional_hints = []
    if len(wrong_guess_lst) > 0:
        for word in range(len(words)):
            for letter in range(len(wrong_guess_lst)):
                if wrong_guess_lst[letter] not in words[word]:
                    pattern_hint = reverse_update_pattern(words[word],
                                                          correct_letters)
                    if pattern_hint == pattern:
                        optional_hints.append(words[word])
    if len(wrong_guess_lst) == 0:
        for word in range(len(words)):
            pattern_hint = reverse_update_pattern(words[word],
                                                  correct_letters)
            if pattern_hint == pattern:
                optional_hints.append(words[word])
    optional_hints = list(dict.fromkeys(optional_hints))
    return optional_hints


def guess_is_word(guess, score, guess_word, pattern, correct_letters, chosen_letters):
    """
    this function run the game uf the user guess is a word
    :param guess: the guess word
    :param score: current score
    :param guess_word: word the user need to guess
    :param pattern: current pattern
    :param correct_letters: current correct_letters
    :param chosen_letters: current chosen_letters
    :return: the update - score, pattern, correct_letters, chosen_letters
    """
    if guess[0] == WORD:
        word = guess[1]
        n = 0
        for i in range(len(guess[1])):
            pattern = update_word_pattern(guess_word, pattern, guess[1][i])
            chosen_letters += word[i]
            if word[i] in guess_word:
                correct_letters = correct_letters + word[i]
                n = n + 1
            if word[i] not in guess_word and word[i] not in wrong_guess_lst:
                wrong_guess_lst.append(word[i])
        score += ((n * (n + 1)) // 2)
        if word != pattern:
            msg = "the word "+word+" is not the right word"
            display_state(pattern, wrong_guess_lst, score, msg)
        if word == pattern:
            msg = "congratulation you won the game"
            display_state(pattern, wrong_guess_lst, score, msg)
    return score, pattern, correct_letters, chosen_letters


def guess_is_letter(guess, chosen_letters, score, pattern, correct_letters, guess_word):
    """
    this function run the game uf the user guess is a letter
    :param guess: the guess letter
    :param chosen_letters: current chosen_letters
    :param score: current pattern
    :param pattern: current pattern
    :param correct_letters: current correct_letters
    :param guess_word: word the user need to guess
    :return: the update - guess, chosen_letters, score, pattern, correct_letters, guess_word
    """
    if guess[0] == LETTER:
        letter = guess[1]
        if letter not in alphabet:
            print("the input should be a single alphabet lowercase letter")
        if letter in alphabet:
            if letter in chosen_letters:
                print("you already chose this letter")
            if (letter not in guess_word and letter not in chosen_letters
                    and letter not in wrong_guess_lst):
                score -= 1
                wrong_guess_lst.append(letter)
                msg = "the letter " + letter + " not in guess word"
                display_state(pattern, wrong_guess_lst, score, msg)
            elif score == 0:
                msg = 'you loose, The word was:' + guess_word + '.'
                display_state(pattern, wrong_guess_lst, score, msg)
            if letter in guess_word and letter not in chosen_letters:
                n = 0
                for i in range(len(guess_word)):
                    if letter == guess_word[i]:
                        n += 1
                        pattern = update_word_pattern(guess_word,pattern,letter)
                score += ((n * (n + 1)) // 2)-1
                correct_letters += letter
                msg = '' #'you chose: ' + letter
                display_state(pattern, wrong_guess_lst, score, msg)
            elif guess_word == pattern:
                msg = "congratulation you won the game"
                display_state(pattern, wrong_guess_lst, score, msg)
            chosen_letters += letter
    return score, pattern, chosen_letters, correct_letters, wrong_guess_lst


def guess_is_hint(guess, pattern, score, correct_letters):
    """
    this function gives to tje user a list of optional words
     according to the current pattern
    :param guess: the input asking for a hint
    :param pattern: current pattern
    :param score: current score
    :param correct_letters: current list of correct_letters
    :return: the hint - list of optional words
    """
    if guess[0] == HINT:
        matches = []
        score -= 1
        list_for_hint = filter_words_list(words, pattern, wrong_guess_lst, correct_letters)
        n = len(list_for_hint)
        if n > HINT_LENGTH:
            for i in range(HINT_LENGTH):
                hint = list_for_hint[i*n // HINT_LENGTH]
                matches.append(hint)
            show_suggestions(matches)
        if n < HINT_LENGTH:
            show_suggestions(list_for_hint)
    return score, pattern


def run_single_game(score):
    """
    this function runs a one single game
    :param score: the initial score or the sum of the score
    :return: the score the player have at the end of the game
    """
    guess_word = get_random_word(words)
    wrong_guess_lst = []
    #print(guess_word)
    pattern = '_'*len(guess_word)
    chosen_letters = ''
    correct_letters = ''
    msg = ''
    display_state(pattern, wrong_guess_lst, score, msg)
    while score > 0 and pattern != guess_word:
        guess = get_input()
        score, pattern, correct_letters, chosen_letters = guess_is_word\
            (guess, score, guess_word, pattern, correct_letters, chosen_letters)
        score, pattern, chosen_letters, correct_letters, wrong_guess_lst = \
            guess_is_letter(guess, chosen_letters,
                            score, pattern, correct_letters,guess_word)
        score, pattern = guess_is_hint(guess, pattern, score, correct_letters)
    return score


def main():
    """
    this function runs a multyplie games
    :return: None
    """
    load_words()
    games_so_far = 1
    score = POINTS_INITIAL
    last_game_score = run_single_game(score)
    while last_game_score > 0:
        msg = "you play "+str(games_so_far)+" games, your score is "+str(last_game_score)+"/" \
              "do you want to play another game?"
        if play_again(msg) == True :
            games_so_far += 1
            wrong_guess_lst.clear()
            last_game_score = run_single_game(last_game_score)
        else:
            break
    while last_game_score == 0:
        msg = "you play " + str(games_so_far)+ " games, your score is "+str(last_game_score)+"/" \
              "do you want to play another game?"
        if play_again(msg) == True :
            games_so_far += 1
            wrong_guess_lst.clear()
            run_single_game(score)
        else:
            break

if __name__ == "__main__":
    #run_single_game(words, score)
    #print(update_word_pattern( 'apple' , '___l_' ,'a'))
    main()
    #print(filter_words_list(words, 'p_________', wrong_guess_lst))
    #print(index_letter_pattern('apple' , '___l_' , 'p'))
    #print(reverse_update_pattern('damagingly', 'dan'))
