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

BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": "DarkOrange3",
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


ALL_WORDS = opener("boggle_dict.txt")


class BoggleGUI:
    """
    The class that runs the game, including all functions.
    the object Boggle its a game that you need to find to correct word.
    you have a certain time to get the highest score.
    """
    # constants of the class.
    MASSAGE = "Start Play"
    SCORE = 0
    WORDS = ""
    ROUND_COUNTER = 0
    WORD_LETTERS = []
    BOARD_DICT = {}
    BUTTON_DICT = {}
    CLICKED_LIST = []
    RIGHT_WORDS = []
    CUR_WORD_LIST = []
    CUR_WORD_STRING = ""

    def __init__(self, all_words):
        """
        :param all_words: gets all the words for the game.
        building the initial object that including the photo and a start button.
        """
        self.__tk_main = tk.Tk()
        self.__tk_main.title = "Boggle"
        self.all_words = all_words

        img = Image.open("picture.png")  # the root to the picture.
        resize_image = img.resize((500, 500), Image.ANTIALIAS)
        my_img = ImageTk.PhotoImage(resize_image)
        self.label_img = tk.Canvas(self.__tk_main, width=500, height=500)
        self.label_img.grid()
        self.label_img.create_image(250, 250, image=my_img)

        self.start_button = tk.Button(self.__tk_main, text="Start",
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
        self.timer = 180
        self.GAME_TIME = ""
        self.root = tk.Tk()
        self.root.resizable(True, True)
        self.root.config(bg="SkyBlue3")
        self.buttons()  # create the relevant buttons for the game.
        self.boxes()  # create all the relevant text boxes.
        self.root.title = "Boggle"

        self.create_buttons_in_lower_frame(
            self.BOARD)  # create the board buttons.
        self._score_label = tk.Label(self.root, text=f"SCORE:{self.SCORE}",
                                     font=("Courier", 15), bg="SkyBlue3").grid(
            row=0, column=0, sticky="n")
        self._time_label = tk.Label(self.root, font=("Courier", 15),
                                    text=self.GAME_TIME, bg="SkyBlue3")
        self._time_label.grid(row=0, column=1)
        self._words_label = tk.Label(self.root, text="WORDS:",
                                     font=("Courier", 15, "italic"),
                                     bg="SkyBlue3").grid(row=0, column=2)
        self._massage = tk.Label(self.root, text=f"{self.MASSAGE}",
                                 font=("Courier", 15, "italic"), bg="SkyBlue3")
        self._massage.grid(row=2, column=1)
        # create all the labels
        self.ROUND_COUNTER += 1
        if self.ROUND_COUNTER == 1:
            self.update()

    def initial(self):
        """
        restarts all the class variables.
        """
        self.timer = 180
        self.GAME_TIME = ""
        self.SCORE = 0
        self.WORDS = ""
        self.WORD_LETTERS = []
        self.BOARD_DICT = {}
        self.BOARD_DICT = {}
        self.CLICKED_LIST = []
        self.RIGHT_WORDS = []
        self.CUR_WORD_LIST = []
        self.CUR_WORD_STRING = ""
        self.MASSAGE = "Your Word:"

    def _click_renew_game(self):
        """
        make the board new again after the user clicked on the renew button.
        """
        if self.ROUND_COUNTER == 1:
            self.ROUND_COUNTER = 2
        if self.ROUND_COUNTER == 0:
            self.ROUND_COUNTER = 1
        self.cur_word_box.config(state="normal")
        self._words_box.config(state="normal")
        self.cur_word_box.delete(1.0, "end")
        self._words_box.delete(1.0, "end")
        self.initial()

        self.BOARD = randomize_board()
        self.create_buttons_in_lower_frame(self.BOARD)
        self._score_label = tk.Label(self.root, text=f"SCORE:{self.SCORE}",
                                     font=("Courier", 15), bg="SkyBlue3").grid(
            row=0,
            column=0)
        self._time_label.config(text=self.GAME_TIME)
        self._time_label.grid(row=0, column=1)
        self.cur_word_box.config(state="disabled")
        self._words_box.config(state="disabled")
        if self.ROUND_COUNTER == 1:
            self.update()

    def stop_button(self):
        """
        stops the game and hide all the letters.
        """
        if self.ROUND_COUNTER == 0:
            self.ROUND_COUNTER = 2
            self.update()
            self.create_buttons_in_lower_frame(self.BOARD)
            self._check_word_button.config(command=lambda: self.click_check_word_button(self.WORD_LETTERS))

            for click in self.CLICKED_LIST:
                r = click[0]
                c = click[1]
                button = self.BUTTON_DICT[(r, c)]

                def button_hover(e):
                    button["fg"] = "blue"

                def not_button_hover(e):
                    button["fg"] = "blue"

                button.bind("<Enter>", button_hover)
                button.bind("<Leave>", not_button_hover)
                button["fg"] = "blue"
            return
        if self.ROUND_COUNTER >= 1:
            self.ROUND_COUNTER = 0
            self._check_word_button.config(command=lambda: None)
            for button in self.BUTTON_DICT.values():
                button["command"] = lambda: None
                button["text"] = ""

    def update(self):
        """
        update the timer after every iteration.
        """
        if self.ROUND_COUNTER >= 1:
            if self.timer > 0:
                mins, secs = divmod(int(self.timer), 60)
                self.GAME_TIME = '{:02d}:{:02d}'.format(mins, secs)
                if 15 > self.timer > 0:
                    if self.timer % 2 == 0:
                        self._time_label.config(text=self.GAME_TIME, fg="red")
                    else:
                        self._time_label.config(text=self.GAME_TIME,
                                                fg="white")
                self._time_label.config(text=self.GAME_TIME, )
                self.root.after(1000, lambda: self.update())
                self.timer -= 1
            else:
                self.__int__game_over()

    def buttons(self):
        """
        create the frame for the buttons.
        """
        self.buttons_frame = tk.Frame(self.root, bg="SkyBlue3",
                                      highlightbackground="black",
                                      highlightthickness=3, )
        self.buttons_frame.grid(row=1, column=1, sticky="nsew")

        self._stop_button = tk.Button(self.root, text="STOP", fg="white",
                                      background="DarkOrange1",
                                      command=lambda: self.stop_button(),
                                      font=("Courier", 15))

        def button_hover(e):
            self._stop_button["fg"] = "red"

        def not_button_hover(e):
            self._stop_button["fg"] = "black"

        self._stop_button.grid(row=1, column=0, sticky="w")

        self._stop_button.bind("<Enter>", button_hover)
        self._stop_button.bind("<Leave>", not_button_hover)
        self._leave_game = tk.Button(self.root, text="QUIT", fg="black",
                                     background="SkyBlue3",
                                     command=lambda: quit(),
                                     font=("Courier", 15))

        def button_hover(e):
            self._leave_game["fg"] = "red"

        def not_button_hover(e):
            self._leave_game["fg"] = "black"

        self._leave_game.bind("<Enter>", button_hover)
        self._leave_game.bind("<Leave>", not_button_hover)
        self._leave_game.grid(row=4, column=2, sticky="se")

        self.click_renew_game = tk.Button(self.root, text="new Game",
                                          command=lambda: self._click_renew_game(),
                                          font=("Courier", 15), bg="SkyBlue3")

        def button_hover(e):
            self.click_renew_game["fg"] = "blue"

        def not_button_hover(e):
            self.click_renew_game["fg"] = "black"

        self.click_renew_game.bind("<Enter>", button_hover)
        self.click_renew_game.bind("<Leave>", not_button_hover)
        self.click_renew_game.grid(row=4, column=0)
        self._check_word_button = tk.Button(self.root, text="Check Word",
                                            command=lambda: self.click_check_word_button(
                                                self.WORD_LETTERS),
                                            font=("Courier", 15),
                                            bg="SkyBlue3")

        def button_hover(e):
            self._check_word_button["fg"] = "blue"

        def not_button_hover(e):
            self._check_word_button["fg"] = "black"

        self._check_word_button.bind("<Enter>", button_hover)
        self._check_word_button.bind("<Leave>", not_button_hover)
        self._check_word_button.grid(row=4, column=1)

    def boxes(self):
        """
        create all the relevant text boxes.
        """
        self.cur_word_box = tk.Text(self.root, bg="LightSkyBlue1", fg="black",
                                    width=28, height=2)
        self.cur_word_box.config(state="disabled")
        self.cur_word_box.grid(row=3, column=1)

        self._words_box = tk.Text(self.root, bg="LightSkyBlue1", fg="black",
                                  width=17, height=13)
        self._words_box.config(state="disabled")
        self._words_box.grid(row=1, column=2)

    def __int__game_over(self):
        """
        Create the game over screen after the ran out.
        """
        self.end_game = tk.Tk()
        f_img = Image.open("gameover.png")
        temp_image = f_img.resize((250, 250), Image.ANTIALIAS)
        end_img = ImageTk.PhotoImage(temp_image)
        self.finish_img = tk.Label(self.end_game, image=end_img)
        self.finish_img.image = end_img
        self.finish_img.grid(row=4, column=0, columnspan=2)
        self.start_button = tk.Button(self.end_game, text="Try Again",
                                      command=lambda: [
                                          self.__int__click_new_game(),
                                          self.end_game.destroy()])
        self.start_button.grid(row=5, column=1)
        self.finish_game = tk.Button(self.end_game, text="QUIT", fg="black",
                                     command=lambda: quit())
        self.finish_game.grid(row=5, column=0)
        self.finish_score = tk.Label(self.end_game,
                                     text="Your Final Score :" + str(
                                         self.SCORE),
                                     font=("Courier", 20, "italic"))
        self.finish_score.grid(row=0, column=0, columnspan=2)
        self.ROUND_COUNTER = 0
        self.root.destroy()

    def click_button_char(self, clicked_lst, button_char, row, col, all_words,
                          CUR_WORD):
        """
        :param clicked_lst: all the buttons that clicked.
        :param button_char: the current char of the button.
        :param row: the row of the button on board.
        :param col: the col of the button on board.
        :param all_words: all the game words.
        :param CUR_WORD: the path to the current word.
        color the future clicked char and adds it to the the current path.
        """
        if (clicked_lst == [] or (row, col) in neighbor(4, 4,
                                                        clicked_lst[-1][0],
                                                        clicked_lst[-1][
                                                            1])) and (
                row, col) not in clicked_lst:
            button = self.BUTTON_DICT[(row, col)]
            button["fg"] = "blue"

            def not_button_hover(e):
                button["fg"] = "blue"

            button.bind("<Leave>", not_button_hover)
            clicked_lst.append((row, col))
            CUR_WORD.append(button_char)
            self.cur_word_box.config(state="normal")
            self.CUR_WORD_STRING = "".join(CUR_WORD)
            self.cur_word_box.delete(1.0, "end")
            self.cur_word_box.insert(1.0, str(self.CUR_WORD_STRING))
            self.cur_word_box.tag_config("center", justify="center")
            self.cur_word_box.tag_add("center", 1.0, "end")
            self.cur_word_box.config(state="disabled")

    def return_buttons_normal(self):
        """
        return the button to his normal color.
        """
        for button in self.BUTTON_DICT.values():
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
        self.CUR_WORD_LIST = []
        word = "".join(word)
        if self.CUR_WORD_STRING in self.all_words and self.CUR_WORD_STRING not in self.RIGHT_WORDS:
            self.RIGHT_WORDS.append(self.CUR_WORD_STRING)
            self.CLICKED_LIST = []
            self.SCORE += len(self.CUR_WORD_STRING) ** 2
            self.WORD_LETTERS = []
            self._words_box.insert(1.0, str(self.CUR_WORD_STRING) + "\n")
            self._words_box.tag_config("center", justify="center")
            self._words_box.tag_add("center", 1.0, "end")
            self._words_box.grid(row=1, column=2)
            self._score_label = tk.Label(self.root,
                                         text=f"SCORE:{self.SCORE}",
                                         font=("Courier", 15),
                                         bg="SkyBlue3").grid(row=0,
                                                             column=0)
        else:
            self.CLICKED_LIST = []
            self.WORD_LETTERS = []
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
                               self.CLICKED_LIST, button_char, row, col,
                               self.all_words, self.CUR_WORD_LIST)],
                           **BUTTON_STYLE)

        def not_button_hover(e):
            button["fg"] = "black"

        button.bind("<Leave>", not_button_hover)

        def button_hover(e):
            if (self.CLICKED_LIST == [] or (row, col) in neighbor(4, 4,
                                                                  self.CLICKED_LIST[
                                                                      -1][0],
                                                                  self.CLICKED_LIST[
                                                                      -1][1])) \
                    and (row, col) not in self.CLICKED_LIST:
                button["fg"] = "lightblue"

        button.bind("<Enter>", button_hover)
        button.grid(row=row, column=col, rowspan=rowspan,
                    columnspan=columnspan, sticky=tk.NSEW)
        self.BUTTON_DICT[(row, col)] = button

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
                self.BOARD_DICT[(r, c)] = board[r][c]
                self._make_button_char(board[r][c], r, c)


if __name__ == '__main__':
    tk_main = BoggleGUI(ALL_WORDS)
