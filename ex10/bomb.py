######################################
# File : bomb.py
# WRITER : yotam_suliman yotamsu26 206922205
# EXERCISE intro2cs1 ex10 2021
# Students I spoke to about the exercise: none
# Web pages I used : none
######################################
import game_parameters


class Bomb:
    """
    This class makes a object from type bomb. with relevant information.
    """
    def __init__(self):
        x, y, radius, time = game_parameters.get_random_bomb_data()
        self.location = (x, y)  # Bomb coordinates.
        self.radius = radius  # Bomb radius.
        self.time = time  # Bomb timer.


