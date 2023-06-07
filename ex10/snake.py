######################################
# File : snake.py
# WRITER : yotam_suliman yotamsu26 206922205
# EXERCISE intro2cs1 ex10 2021
# Students I spoke to about the exercise: none
# Web pages I used : none
######################################
LENGTH = 3
HEAD_COOR = (10, 10)
START_COOR = [(10, 8), (10, 9), (10, 10)]


class Snake:
    """
    This class makes a object from snake type. with relevant information.
    the class includes function to check the move ability.
    """
    def __init__(self):
        self.length = LENGTH  # The length of the snake.
        self.location = HEAD_COOR  # The coordinate of the snake head.
        self.coordinates = START_COOR  # The coordinates of the all snake.

    def possible_moves(self):
        """
        This function checks what directions the snake is able to move.
        :return: list of all the possible directions.
        """
        directions = ["Right", "Left", "Up", "Down"]
        if (self.location[0] - 1, self.location[1]) == self.coordinates[-2]:
            directions.remove("Left")
        if (self.location[0] + 1, self.location[1]) == self.coordinates[-2]:
            directions.remove("Right")
        if (self.location[0], self.location[1] - 1) == self.coordinates[-2]:
            directions.remove("Down")
        if (self.location[0], self.location[1] + 1) == self.coordinates[-2]:
            directions.remove("Up")
        return directions

    def add_snake_coordinates(self, movekey):
        """
        if the move is possible the function change the coordinates of the
        head of the snake.
        :param movekey: direction for the next move of the snake.
        :return: True if the move was possible and done, and False if not.
        """
        if movekey in self.possible_moves():
            if movekey == "Right":
                self.coordinates.append \
                    ((self.location[0] + 1, self.location[1]))
                self.location = (self.location[0] + 1, self.location[1])
            if movekey == "Left":
                self.coordinates.append \
                    ((self.location[0] - 1, self.location[1]))
                self.location = (self.location[0] - 1, self.location[1])
            if movekey == "Up":
                self.coordinates.append \
                    ((self.location[0], self.location[1] + 1))
                self.location = (self.location[0], self.location[1] + 1)
            if movekey == "Down":
                self.coordinates.append \
                    ((self.location[0], self.location[1] - 1))
                self.location = (self.location[0], self.location[1] - 1)
            return True
        return False


    def remove_snake_coordinates(self, movekey):
        """
        this function remove the last coordinates of the snake. "the tail".
        :param movekey: direction for the next move of the snake.
        :return: True if the move was possible and done, and False if not.
        """
        directions = ["Right", "Left", "Up", "Down"]
        if movekey not in directions:
            return False
        else:
            self.coordinates = self.coordinates[1:]
            return True
