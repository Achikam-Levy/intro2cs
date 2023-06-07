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

#words = load_words()

#correct_letters = ''

#score = POINTS_INITIAL

#wrong_guess_lst = []

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


def filter_words_list(words, pattern, wrong_guess_lst,):
    """
    this function makes a list of optional hints
    :param words: words.txt
    :param pattern: the current pattern of the game
    :param wrong_guess_lst: wrong_guess_lst
    :param correct_letters: correct_letters list
    :return: list of the hints for the user
    """
    optional_hints = []
    letters_in_pattern = ''
    for i in pattern:
        if i in alphabet:
            letters_in_pattern += i
    if len(wrong_guess_lst) > 0:
        for word in range(len(words)):
            for letter in range(len(wrong_guess_lst)):
                if wrong_guess_lst[letter] not in words[word]:
                    pattern_hint = reverse_update_pattern(words[word],
                                                          letters_in_pattern)
                    if pattern_hint == pattern:
                        optional_hints.append(words[word])
    if len(wrong_guess_lst) == 0:
        for word in range(len(words)):
            pattern_hint = reverse_update_pattern(words[word],
                                                  letters_in_pattern)
            if pattern_hint == pattern:
                optional_hints.append(words[word])
    optional_hints = list(dict.fromkeys(optional_hints))
    return optional_hints


def guess_is_word( guess, score, guess_word, pattern, correct_letters, chosen_letters, msg):
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
        if word != guess_word:
            msg = ''
            for i in range(len(word)):
                if word[i] not in alphabet:
                    continue
            else:
                score -= 1
        if word == guess_word:
            n = 0
            score -= 1
            msg = "you won the game !"
            for i in range(len(guess[1])):
                if word[i] in guess_word and word[i] not in pattern:
                    correct_letters += word[i]
                    n += 1
                    chosen_letters += word[i]
            score += ((n * (n + 1)) // 2)
            for i in range(len(guess[1])):
               pattern = update_word_pattern(guess_word, pattern, guess[1][i])
        if score == 0:
            msg = "you lost the game. the word was " + guess_word + " ."
    return score, pattern, correct_letters, chosen_letters, msg


def guess_is_letter(guess, chosen_letters, score, pattern, correct_letters, guess_word, wrong_guess_lst, msg):
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
        if letter not in alphabet or len(letter) == 0 or len(letter) > 1:
            msg = "the letter you entered is invalid"
        if letter in alphabet:
            if letter in chosen_letters and len(letter) != 0:
                msg = "the letter you entered was already chosen"
            if (letter not in guess_word and letter not in chosen_letters
                    and letter not in wrong_guess_lst):
                score -= 1
                wrong_guess_lst.append(letter)
                msg = ''
            if score == 0:
                msg = "you lost the game. the word was "+guess_word+" ."
            if letter in guess_word and letter not in chosen_letters:
                n = 0
                for i in range(len(guess_word)):
                    if letter == guess_word[i]:
                        n += 1
                        pattern = update_word_pattern(guess_word,pattern,letter)
                score += ((n * (n + 1)) // 2)-1
                correct_letters += letter
                msg = ''
            if guess_word == pattern:
                msg = "you won the game !"
            chosen_letters += letter
    return score, pattern, chosen_letters, correct_letters, wrong_guess_lst, msg


def guess_is_hint(words,guess, pattern, score,  wrong_guess_lst,  guess_word, msg):
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
        list_for_hint = filter_words_list(words, pattern, wrong_guess_lst,)
        n = len(list_for_hint)
        if n > HINT_LENGTH:
            for i in range(HINT_LENGTH):
                hint = list_for_hint[i*n // HINT_LENGTH]
                matches.append(hint)
            show_suggestions(matches)
        if n <= HINT_LENGTH:
            for i in range(len(list_for_hint)):
                matches.append(list_for_hint[i])
            show_suggestions(matches)
        if score == 0:
            msg = "you lost the game. the word was " + guess_word + " ."
    return score, pattern, msg


def run_single_game(words, score):
    """
    this function runs a one single game
    :param score: the initial score or the sum of the score
    :return: the score the player have at the end of the game
    """
    guess_word = get_random_word(words)
    wrong_guess_lst = []
    pattern = '_'*len(guess_word)
    chosen_letters = ''
    correct_letters = ''
    msg = ''
    display_state(pattern, wrong_guess_lst, score, msg)
    while score > 0 and pattern != guess_word:
        guess = get_input()
        score, pattern, correct_letters, chosen_letters, msg = guess_is_word \
            ( guess, score, guess_word, pattern,
             correct_letters, chosen_letters, msg)
        score, pattern, chosen_letters, correct_letters, wrong_guess_lst, msg =\
            guess_is_letter(guess, chosen_letters, score, pattern,
                            correct_letters, guess_word, wrong_guess_lst, msg)
        score, pattern, msg = guess_is_hint(words, guess, pattern, score,
                                            wrong_guess_lst, guess_word, msg)
        display_state(pattern, wrong_guess_lst, score, msg)
    return score


def main():
    """
    this function runs a multyplie games
    :return: None
    """
    words = load_words()
    games_so_far = 1
    score = POINTS_INITIAL
    last_game_score = run_single_game(words, score)
    while True:
        if last_game_score > 0:
            msg = "you play "+str(games_so_far)+" games, your score is " \
                    ""+str(last_game_score)+" do you want to play another game?"
            if play_again(msg) == True:
                games_so_far += 1
                last_game_score = run_single_game(words,last_game_score)
            else:
                break
        if last_game_score == 0:
            msg = " number of game survived: "+ str(games_so_far)+  \
                  " start a new series of games?"
            if play_again(msg) == True:
                run_single_game(words, score)
            else:
                break


if __name__ == "__main__":
    main()
    #print(filter_words_list(['a', 'ab' , '', 'ac','abc'],'__',[]))
    #print(run_single_game(['abc'],1))

