######################################
# File : apple.py
# WRITER : yotam_suliman yotamsu26 206922205
# EXERCISE intro2cs1 ex10 2021
# Students I spoke to about the exercise: none
# Web pages I used : none
######################################
import game_parameters


class Apple:
    """
    This class makes an object from type apple. with relevant information.
    """
    def __init__(self):
        x, y, score = game_parameters.get_random_apple_data()
        self.location = (x, y)  # Apple coordinates.
        self.score = score  # The score that the apple equal to.


