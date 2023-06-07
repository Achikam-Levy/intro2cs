######################################
# File : apple.py
# WRITER : yotam_suliman yotamsu26 206922205,aaa997 208764944
# EXERCISE intro2cs1 ex10 2021
# Students I spoke to about the exercise: none
# Web pages I used : none
######################################

import tkinter as tk
from PIL import ImageTk, Image
from ex12_utils import *
from boggle_board_randomizer import randomize_board

BUTTON_STYLE = {"font": ("Comic Sans MS", 25, "bold"),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": "blue",
                "activebackground": "slateblue"}


def opener(file_name):
    """
    :param file_name: the name of the file to open.
    :return: all the words from the file.
    """
    with open(file_name, "rt") as f:
        text = f.read()
        all_words = text.split()
    return all_words


ALL_WORDS = set(opener("boggle_dict.txt"))


class BoggleGUI:
    """
    The class that runs the game, including all functions.
    the object Boggle its a game that you need to find to correct word.
    you have a certain time to get the highest score.
    """
    # constants of the class.
    _MASSAGE = "Start Play"
    _SCORE = 0
    _WORDS = ""
    _ROUND_COUNTER = 0
    _WORD_LETTERS = []
    _BOARD_DICT = {}
    _BUTTON_DICT = {}
    _CLICKED_LIST = []
    _RIGHT_WORDS = []
    _CUR_WORD_LIST = []
    _CUR_WORD_STRING = ""

    def __init__(self, all_words):
        """
        :param all_words: gets all the words for the game.
        building the initial object that including the photo and a start button.
        """
        self.__tk_main = tk.Tk()
        self.__tk_main.title = "Boggle"
        self.all_words = all_words

        start_image = Image.open("png-clipart-computer-icons-button-start-blue-computer-network.png")
        start_image = start_image.resize((190, 70), Image.ANTIALIAS)
        start_image = ImageTk.PhotoImage(start_image)

        open_img = Image.open("picture.png")  # the root to the picture.
        resize_image = open_img.resize((500, 450), Image.ANTIALIAS)
        my_img = ImageTk.PhotoImage(resize_image)

        self.label_img = tk.Canvas(self.__tk_main, width=500, height=460)
        self.label_img.grid()
        self.label_img.create_image(250, 250, image=my_img)

        self.start_button = tk.Button(self.__tk_main, image=start_image,
                                      borderwidth=0,
                                      command=lambda: [
                                          self.__int__click_new_game(),
                                          self.__tk_main.destroy()])
        # the start button, calls to the init of a new game.
        self.start_button.grid()
        self.__tk_main.mainloop()

    def __int__click_new_game(self):
        """
        building a game board and all the relevant buttons for the game.
        restart all the relevant variables.
        """
        self.initial()
        self.BOARD = randomize_board()
        self._timer = 180
        self._GAME_TIME = ""
        self.root = tk.Tk()
        self.root.resizable(True, True)
        self.root.config(bg="SkyBlue3")
        self.buttons()  # create the relevant buttons for the game.
        self.boxes()  # create all the relevant text boxes.
        self.root.title = "Boggle"

        self.create_buttons_in_lower_frame(
            self.BOARD)  # create the board buttons.
        self._score_label = tk.Label(self.root, text=f"SCORE:{self._SCORE}",
                                     font=("Courier", 20, "bold"),
                                     bg="SkyBlue3")
        self._score_label.grid(row=0, column=0)
        self._time_label = tk.Label(self.root, font=("Courier", 20, "bold",),
                                    text=self._GAME_TIME, bg="SkyBlue3")
        self._time_label.grid(row=0, column=1)
        self._words_label = tk.Label(self.root, text="WORDS:",
                                     font=("Courier", 25, "bold"),
                                     bg="SkyBlue3").grid(row=0, column=2)
        self._massage_label = tk.Label(self.root, text=f"{self._MASSAGE}",
                                       font=("Courier", 25, "bold"),
                                       bg="SkyBlue3")
        self._massage_label.grid(row=2, column=1)
        # create all the labels
        self._ROUND_COUNTER += 1
        if self._ROUND_COUNTER == 1:
            self.update()

    def initial(self):
        """
        restarts all the class variables.
        """
        self._timer = 180
        self._GAME_TIME = ""
        self._SCORE = 0
        self._WORDS = ""
        self._WORD_LETTERS = []
        self._BOARD_DICT = {}
        self._CLICKED_LIST = []
        self._RIGHT_WORDS = []
        self._CUR_WORD_LIST = []
        self._CUR_WORD_STRING = ""
        self._MASSAGE = "Your Word:"

    def _click_renew_game(self):
        """
        make the board new again after the user clicked on the renew button.
        """
        if self._ROUND_COUNTER == 1:
            self._ROUND_COUNTER = 2
        if self._ROUND_COUNTER == 0:
            self._ROUND_COUNTER = 1
        self.cur_word_box.config(state="normal")
        self._words_box.config(state="normal")
        self.cur_word_box.delete(1.0, "end")
        self._words_box.delete(1.0, "end")
        self.initial()
        self.BOARD = randomize_board()
        self.create_buttons_in_lower_frame(self.BOARD)
        self._score_label.config(text=f"SCORE:{self._SCORE}")
        self._time_label.config(text=self._GAME_TIME)
        self._time_label.grid(row=0, column=1)
        self.cur_word_box.config(state="disabled")
        self._words_box.config(state="disabled")
        if self._ROUND_COUNTER == 1:
            self.update()

    def stop_button(self):
        """
        stops the game and hide all the letters.
        """
        if self._ROUND_COUNTER == 0:
            self._ROUND_COUNTER = 2
            self.update()
            self.create_buttons_in_lower_frame(self.BOARD)
            self.check_word_button.config(
                command=lambda: self.click_check_word_button(
                    self._WORD_LETTERS))

            for click in self._CLICKED_LIST:
                r = click[0]
                c = click[1]
                button = self._BUTTON_DICT[(r, c)]

                def button_hover(e):
                    button["fg"] = "blue"

                def not_button_hover(e):
                    button["fg"] = "blue"

                button.bind("<Enter>", button_hover)
                button.bind("<Leave>", not_button_hover)
                button["fg"] = "blue"
            return
        if self._ROUND_COUNTER >= 1:
            self._ROUND_COUNTER = 0
            self.check_word_button.config(command=lambda: None)
            for button in self._BUTTON_DICT.values():
                button["command"] = lambda: None
                button["text"] = ""

    def right_word(self, r):
        """
        doing some effects for choosing right word
        :param r: rounds counter for the effects
        :return: none
        """
        if r == 0:
            self._massage_label.config(text=f"{self._MASSAGE}",
                                       font=("Courier", 20, "bold"),
                                       fg="black")

        if r > 0:
            self._massage_label.config(text="WELL DONE!", fg="white",
                                       font=("Courier", 50, "bold",))

            if self.root["bg"] == "SkyBlue3":
                self._massage_label.config(fg="SkyBlue3")
                self.root.config(bg="red")
                self._words_box.config(bg="red")

            elif self.root["bg"] == "red":
                self._massage_label.config(fg="red")
                self.root.config(bg="SkyBlue3")
                self._words_box.config(bg="SkyBlue3")

            self.root.after(90, lambda: self.right_word(r - 1))

    def update(self):
        """
        update the timer after every iteration.
        """
        if self._ROUND_COUNTER >= 1:
            if self._timer > 0:
                mins, secs = divmod(int(self._timer), 60)
                self._GAME_TIME = '{:02d}:{:02d}'.format(mins, secs)
                if 15 > self._timer > 0:
                    if self._timer % 2 == 0:
                        self._time_label.config(text=self._GAME_TIME,
                                                fg="red", )
                    else:
                        self._time_label.config(text=self._GAME_TIME,
                                                fg="white")
                self._time_label.config(text=self._GAME_TIME, )
                self.root.after(1000, lambda: self.update())
                self._timer -= 1
            else:
                self.__int__game_over()

    def buttons(self):
        """
        create the frame for the buttons.
        """
        self.buttons_frame = tk.Frame(self.root, bg="blue",
                                      highlightbackground="black",
                                      highlightthickness=3, )
        self.buttons_frame.grid(row=1, column=1, sticky="nsew")

        self._stop_button = tk.Button(self.root, text="STOP", fg="white",
                                      background="DarkOrange1",
                                      command=lambda: self.stop_button(),
                                      font=("Helvetica", 26, "bold"))

        def button_hover(e):
            self._stop_button["fg"] = "red"

        def not_button_hover(e):
            self._stop_button["fg"] = "black"

        self._stop_button.grid(row=1, column=0)

        self._stop_button.bind("<Enter>", button_hover)
        self._stop_button.bind("<Leave>", not_button_hover)
        self._leave_game_button = tk.Button(self.root, text="QUIT", fg="black",
                                            background="SkyBlue3",
                                            command=lambda: quit(),
                                            font=("Courier", 20, "bold",))

        def button_hover(e):
            self._leave_game_button["fg"] = "red"

        def not_button_hover(e):
            self._leave_game_button["fg"] = "black"

        self._leave_game_button.bind("<Enter>", button_hover)
        self._leave_game_button.bind("<Leave>", not_button_hover)
        self._leave_game_button.grid(row=4, column=2)

        self.new_game_button = tk.Button(self.root, text="new Game",
                                         command=lambda: self._click_renew_game(),
                                         font=("Courier", 20), bg="SkyBlue3")

        def button_hover(e):
            self.new_game_button["fg"] = "blue"

        def not_button_hover(e):
            self.new_game_button["fg"] = "black"

        self.new_game_button.bind("<Enter>", button_hover)
        self.new_game_button.bind("<Leave>", not_button_hover)
        self.new_game_button.grid(row=4, column=0)
        self.check_word_button = tk.Button(self.root, text="Check Word",
                                           command=lambda: self.click_check_word_button(
                                               self._WORD_LETTERS),
                                           font=("Courier", 20),
                                           bg="SkyBlue3")

        def button_hover(e):
            self.check_word_button["fg"] = "blue"

        def not_button_hover(e):
            self.check_word_button["fg"] = "black"

        self.check_word_button.bind("<Enter>", button_hover)
        self.check_word_button.bind("<Leave>", not_button_hover)
        self.check_word_button.grid(row=4, column=1)

    def boxes(self):
        """
        create all the relevant text boxes.
        """
        self.cur_word_box = tk.Text(self.root, bg="LightSkyBlue1", fg="black",
                                    font=("Comic Sans MS", 15, "bold"),
                                    width=28, height=2)
        self.cur_word_box.config(state="disabled")
        self.cur_word_box.grid(row=3, column=1)

        self._words_box = tk.Text(self.root, bg="LightSkyBlue1", fg="black",
                                  font=("Comic Sans MS", 13, "bold"),
                                  width=17, height=13)
        self._words_box.config(state="disabled")
        self._words_box.grid(row=1, column=2)

    def __int__game_over(self):
        """
        Create the game over screen after the ran out.
        """
        self.end_game = tk.Tk()
        f_img = Image.open("gameover.png")
        temp_image = f_img.resize((500, 500), Image.ANTIALIAS)
        end_img = ImageTk.PhotoImage(temp_image)
        self.finish_img = tk.Label(self.end_game, image=end_img)
        self.finish_img.image = end_img
        self.finish_img.grid(row=4, column=0, columnspan=2)
        self.start_button = tk.Button(self.end_game, text="Try Again",
                                      bg="green", fg="white",
                                      font=("Comic Sans MS", 19, "bold"),
                                      command=lambda: [
                                          self.__int__click_new_game(),
                                          self.end_game.destroy()])
        self.start_button.grid(row=5, column=1)
        self.finish_game = tk.Button(self.end_game, text="Quit", bg="red",
                                     fg="black", font=("Comic Sans MS", 20
                                                       , "bold"),
                                     command=lambda: quit())
        self.finish_game.grid(row=5, column=0)
        self.finish_score_label = tk.Label(self.end_game,
                                           text="Your Final SCORE :" + str(
                                               self._SCORE),
                                           font=("Courier", 20, "bold"))
        self.finish_score_label.grid(row=0, column=0, columnspan=2)
        self._ROUND_COUNTER = 0
        self.root.destroy()

    def click_button_char(self, clicked_lst, button_char, row, col, all_words,
                          cur_word):
        """
        :param clicked_lst: all the buttons that clicked.
        :param button_char: the current char of the button.
        :param row: the row of the button on board.
        :param col: the col of the button on board.
        :param all_words: all the game words.
        :param cur_word: the path to the current word.
        color the future clicked char and adds it to the the current path.
        """
        if (clicked_lst == [] or (row, col) in neighbor(4, 4,
                                                        clicked_lst[-1][0],
                                                        clicked_lst[-1][
                                                            1])) and (
                row, col) not in clicked_lst:
            button = self._BUTTON_DICT[(row, col)]
            button["fg"] = "blue"

            def not_button_hover(e):
                button["fg"] = "blue"

            button.bind("<Leave>", not_button_hover)
            clicked_lst.append((row, col))
            cur_word.append(button_char)
            self.cur_word_box.config(state="normal")
            self._CUR_WORD_STRING = "".join(cur_word)
            self.cur_word_box.delete(1.0, "end")
            self.cur_word_box.insert(1.0, str(self._CUR_WORD_STRING))
            self.cur_word_box.tag_config("center", justify="center")
            self.cur_word_box.tag_add("center", 1.0, "end")
            self.cur_word_box.config(state="disabled")

    def return_buttons_normal(self):
        """
        return the button to his normal color.
        """
        for button in self._BUTTON_DICT.values():
            button["fg"] = "black"

    def click_check_word_button(self, word):
        """
        :param word: the final word.
        checks if the word is correct and if it is it's put it in the word box.
        """
        self._words_box.config(state="normal")
        self.cur_word_box.config(state="normal")
        self.cur_word_box.delete(1.0, "end")
        self.create_buttons_in_lower_frame(self.BOARD)
        self._CUR_WORD_LIST = []
        if self._CUR_WORD_STRING in self.all_words and self._CUR_WORD_STRING not in self._RIGHT_WORDS:
            self.right_word(
                6)  # active right word effects, int: number of effects
            self._RIGHT_WORDS.append(self._CUR_WORD_STRING)
            self._CLICKED_LIST = []
            self._SCORE += len(self._CUR_WORD_STRING) ** 2
            self._WORD_LETTERS = []
            self._words_box.insert(1.0, str(self._CUR_WORD_STRING) + "\n")
            self._words_box.tag_config("center", justify="center")
            self._words_box.tag_add("center", 1.0, "end")
            self._words_box.grid(row=1, column=2)
            self._score_label.config(text=f"SCORE:{self._SCORE}")
        else:
            self._CLICKED_LIST = []
            self._WORD_LETTERS = []
        self._words_box.config(state="disabled")
        self.cur_word_box.config(state="disabled")

    def _make_button_char(self, button_char, row, col,
                          rowspan: int = 1, columnspan: int = 1):
        """
        :param button_char: the current char of the board.
        :param row: the row of the board.
        :param col: the col of the board.
        :param rowspan: the height of the row.
        :param columnspan: the width of the col.
        building the random board letters on the screen.
        """
        button = tk.Button(self.buttons_frame, text=button_char,
                           command=lambda: [self.click_button_char(
                               self._CLICKED_LIST, button_char, row, col,
                               self.all_words, self._CUR_WORD_LIST)],
                           **BUTTON_STYLE)

        def not_button_hover(e):
            button["fg"] = "black"

        button.bind("<Leave>", not_button_hover)

        def button_hover(e):
            if (self._CLICKED_LIST == [] or (row, col) in neighbor(4, 4,
                                                                   self._CLICKED_LIST[
                                                                       -1][0],
                                                                   self._CLICKED_LIST[
                                                                       -1][1])) \
                    and (row, col) not in self._CLICKED_LIST:
                button["fg"] = "lightblue"

        button.bind("<Enter>", button_hover)
        button.grid(row=row, column=col, rowspan=rowspan,
                    columnspan=columnspan, sticky=tk.NSEW, )
        self._BUTTON_DICT[(row, col)] = button

        return button

    def create_buttons_in_lower_frame(self, board):
        """
        :param board: the randomize board.
        creates all the buttons of the board.
        """
        for i in range(len(board)):
            tk.Grid.columnconfigure(self.buttons_frame, i, weight=1)
        for i in range(len(board[0])):
            tk.Grid.rowconfigure(self.buttons_frame, i, weight=1)

        for r in range(len(board)):
            for c in range(len(board[0])):
                self._BOARD_DICT[(r, c)] = board[r][c]
                self._make_button_char(board[r][c], r, c)


if __name__ == '__main__':
    tk_main = BoggleGUI(ALL_WORDS)
