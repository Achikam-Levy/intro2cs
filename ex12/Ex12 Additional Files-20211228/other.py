import tkinter as tk
from ex12_utils import *
from boggle_board_randomizer import randomize_board
# import time

BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": "grey",
                "activebackground": "slateblue"}


class BoggleGUI:
    WORDS = ""
    MASSAGE = "to start a game, \nenter the 'start game' button"
    round_counter = 0
    _buttons_dict = {}
    board_dict = {}
    clicked_lst = []
    word_letters = []
    right_words = []
    game_time = 180

    def __init__(self, tk_main, all_words):

        self.all_words = all_words
        self.main_root = tk_main
        self._time_label = tk.Label(self.main_root, font=("Courier", 15), text=180)
        self._time_label.grid(row=0, column=1)
        self._main_window = tk_main


        self._top_frame = tk.Frame(tk_main, width=10, height=10).grid(row=0, column=0)
        self._bottom_frame = tk.Frame(tk_main, width=10, height=70).grid(row=3, column=1)
        self._right_frame = tk.Frame(tk_main, width=140, height=10).grid(row=1, column=1)
        self._left_frame = tk.Frame(tk_main, width=70, height=1).grid(row=0, column=0)

        self._start_massage = tk.Text(self._bottom_frame, bg="white",fg="black", width=28, height=2)
        self._start_massage.insert(1.0, self.MASSAGE)
        self._start_massage.tag_config("center", justify="center")
        self._start_massage.tag_add("center", 1.0, "end")
        self._start_massage.grid(row=2, column=1)

        self.cur_word_box = tk.Text(self._main_window, bg="white",fg="black", width=28, height=2)
        self.cur_word_box.grid(row=3, column=1)

        self._words_box = tk.Text(self._main_window, bg="white",fg="black", width=17, height=13)
        self._words_box.grid(row=1, column=2)

        self._words_label = tk.Label(tk_main, text="words:" ,font=("Courier", 15)).grid(row=0, column=2)
        self._leave_game = tk.Button(self._right_frame, text="quit", fg="red", command=lambda: quit() ,font=("Courier", 15)).grid(row=4, column=2)
        self._new_game = tk.Button(self._left_frame, text="srart game",command=lambda: self.click_button_new_game(), font=("Courier", 15)).grid(row=4, column=0)

        self._check_word_button = tk.Button(self._bottom_frame, text="check_word", command=lambda: self.click_check_word_button(self.word_letters), font=("Courier", 15)).grid(row=4, column=1)
        self.buttons_frame = tk.Frame(tk_main, bg="grey", highlightbackground="black", highlightthickness=3)
        self.buttons_frame.grid(row=1, column=1)


    def click_button_new_game(self):
        self.SCORE = 0
        self.MASSAGE = "your word:"
        self._start_massage.delete(1.0, "end")
        self._start_massage.insert(1.0, self.MASSAGE)
        self._start_massage.tag_config("center", justify="center")
        self._start_massage.tag_add("center", 1.0, "end")
        self.board = randomize_board()
        self.create_buttons_in_lower_frame(self.board)
        self._words_box.delete(1.0, "end")
        self.cur_word_box.delete(1.0, "end")
        self._score_label = tk.Label(self._top_frame, text=f"score:{self.SCORE}", font=("Courier", 15)).grid(row=0, column=0)


        self.clicked_lst = []
        self.word_letters = []
        timer = tk.StringVar()
        self._time_label = tk.Label(self.main_root, font=("Courier", 15),textvariable=timer)
        self._time_label.grid(row=0, column=1)
        self._new_game = tk.Button(self._bottom_frame, text="check_word", command=lambda: self.click_check_word_button(self.word_letters), font=("Courier", 15)).grid(row=4, column=1)
        self.game_time = 180
        self.round_counter += 1
        if self.round_counter == 1:
            self.update(timer)


    def update(self, timer):
        timer.set(self.game_time)
        if self.game_time > 0:
            self.game_time -= 1
            self.main_root.after(1000, lambda: self.update(timer))
        else:
            self.click_button_new_game()


    def game_over(self):
        self.MASSAGE = "to play again, \nenter the 'start game' button"
        self._start_massage.delete(1.0, "end")
        self._start_massage.insert(1.0, self.MASSAGE)
        self._start_massage.tag_config("center", justify="center")
        self._start_massage.tag_add("center", 1.0, "end")



    def click_button_char(self,clicked_lst, button_char, row, col, word):
        if (clicked_lst == [] or (row, col) in neighbor(4, 4, clicked_lst[-1][0], clicked_lst[-1][1])) and (row, col) not in clicked_lst:
            button = self._buttons_dict[(row, col)]
            button['fg'] = "blue"
            clicked_lst.append((row, col))
            word.append(button_char)
            cur_word = "".join(word)
            self.cur_word_box.delete(1.0, "end")
            self.cur_word_box.insert(1.0, str(cur_word))
            self.cur_word_box.tag_config("center", justify="center")
            self.cur_word_box.tag_add("center", 1.0, "end")


    def return_buttons_normal(self):
        for button in self._buttons_dict.values():
            button["fg"] = "black"

    def click_check_word_button(self, word):
        self.cur_word_box.delete(1.0, "end")
        self.return_buttons_normal()
        word = "".join(word)
        if word in self.all_words and word not in self.right_words:
            self.right_words.append(word)
            self.clicked_lst = []
            self.SCORE += len(word)**2
            self.word_letters = []
            self._words_box.insert(1.0, str(word)+"\n")
            self._words_box.tag_config("center", justify="center")
            self._words_box.tag_add("center", 1.0, "end")
            self._words_box.grid(row=1, column=2)
            self._score_label = tk.Label(self._top_frame, text=f"score:{self.SCORE}", font=("Courier", 15)).grid(row=0, column=0)
            print("good")
        else:
            self.clicked_lst = []
            self.word_letters = []
            print("no")

    def _make_button_char(self, button_char, row, col,
                     rowspan: int = 1, columnspan: int = 1):
        button = tk.Button(self.buttons_frame, text=button_char, command=lambda: self.click_button_char(self.clicked_lst, button_char, row, col, self.all_words), **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tk.NSEW)
        self._buttons_dict[(row, col)] = button
        return button

    def create_buttons_in_lower_frame(self, board):
        for i in range(len(board)):
            tk.Grid.columnconfigure(self.buttons_frame, i, weight=1)
        for i in range(len(board[0])):
            tk.Grid.rowconfigure(self.buttons_frame, i, weight=1)

        for r in range(len(board)):
            for c in range(len(board[0])):
                self.board_dict[(r, c)] = board[r][c]
                self._make_button_char(board[r][c], r, c)


def opener(file_name):
    with open(file_name, "rt") as f:
        text = f.read()
        all_words = text.split()
    return all_words

if __name__ == '__main__':
    tk_main = tk.Tk()
    tk_main.title = "Boggle"
    all_words = "gui_12 (2).py"
    all_words = opener(all_words)
    BoggleGUI(tk_main, all_words)
    tk_main.mainloop()
