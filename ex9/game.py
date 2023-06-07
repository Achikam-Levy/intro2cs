#################################################################
# FILE : game.py
# WRITER : achikam levy , aaa997 , 208764944
# EXERCISE : intro2cs2 ex6 2021
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################
from car import *
from board import *
from helper import *
import sys


class Game:
    """
    class game, unit all the game units to a full game
    """
    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board
        print(self.__board)

    def __single_turn(self):
        """
        Note - this function is here to guide you, and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        move = input("enter your car and direction (e.g Y,l)")
        self.move = move
        move = list(move)

        if move[0] == '!':
            print("you ended the game")
            return False

        if not self.__board.possible_moves():
            print("there is not more possible_moves")

        if len(move) == 3 and (move[1] == ','):
            self.car = str(move[0])
            self.direction = str(move[2])
            if self.car not in 'YGBROW' or self.direction not in 'urld':
                print('the input is not valid')
            if self.car in 'YGBROW' and self.direction in 'urld':
                if self.car not in self.__board.current_cars_dict:
                    print("this car not in the game")
                self.__board.move_car(self.car, self.direction)
                print(self.__board)
        else:
            print('the input is not valid')

        if self.__board.cell_content(self.__board.target_location())\
                is not None:
            print("you won!")
            return False

        return True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while self.__single_turn():
            continue


def initial_board():
    """
    check the parameters to initialize a board
    :return: init board
    """
    parameters = sys.argv
    json_to_open = parameters[1]
    opened_json = load_json(json_to_open)
    oriantions = [0, 1]
    board = Board()

    for name in opened_json:
        values = opened_json[name]
        length = values[0]
        location = values[1]
        oriantion = values[2]
        if name in 'YGBROW' and 1 < length < 5 and oriantion in oriantions:
            car = Car(name, length, location, oriantion)
            board.add_car(car)
            board.current_cars_dict[name] = car

    return board


def main():
    """
    running the game
    :return: None
    """
    board = initial_board()
    game = Game(board)
    game.play()


if __name__ == "__main__":
    main()
