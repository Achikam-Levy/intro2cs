######################################
# File : game.py
# WRITER : yotam_suliman yotamsu26 206922205
# EXERCISE intro2cs1 ex10 2021
# Students I spoke to about the exercise: none
# Web pages I used : none
######################################
from snake import *
from bomb import *
from apple import *


class Game:
    """
    This class make an object of game type. and uses functions
     that relevant to the game.
    """
    def __init__(self):
        self.s = Snake()  # build a object from snake type.
        self.list_locations = []
        b = self.generate_bomb(self.s)
        a1 = self.generate_apple(self.s)  # build a object from apple type.
        a2 = self.generate_apple(self.s)  # build a object from apple type.
        a3 = self.generate_apple(self.s)  # build a object from apple type.
        self.bomb_list = [b]  # list with the bomb.
        self.apple_list = [a1, a2, a3]  # list with the three apples.
        self.COLORS = {"snake": "black", "bomb": "red", "apple": "green",
                       "radius": "orange"}  # dict with all the relevant colors
        # and with keys of the types.

    def drew_cell(self, coordinates, color, gd):
        """
        :param coordinates: coordinates of the relevant parameters to drew.
        :param color: the name of the color the will be drew.
        :param gd: the game API.
        :return: None.
        after use this function all the relevant coordinates
        will be with the relevant color.
        """
        if coordinates:
            for c in coordinates:
                if 0 <= c[0] <= game_parameters.WIDTH - 1 and 0 <= c[1] <= \
                        game_parameters.HEIGHT - 1:
                    gd.draw_cell(c[0], c[1], color)

    def drew_board(self, gd):
        """
        :param gd: the game API.
        :return: None.
        """
        self.drew_cell(self.s.coordinates, self.COLORS["snake"], gd)
        for bomb in self.bomb_list:
            self.drew_cell([bomb.location], self.COLORS["bomb"], gd)
        for apple in self.apple_list:
            self.drew_cell([apple.location], self.COLORS["apple"], gd)

    def eat_apple(self):
        """
        This function checks if the apple location match to the snake
        locations.
        if yes its returns the apple and if not False.
        """
        for apple in self.apple_list:
            if apple.location == self.s.location:
                return apple
        return False

    def generate_apple(self, snake):
        """
        :param snake: object from type snake.
        :return: False if theres no place in the game.
        and the relevant apple object if there is a place.
        """
        if len(self.list_locations) + len(snake.coordinates) == \
                game_parameters.HEIGHT * game_parameters.WIDTH:
            return False
        while True:
            apple = Apple()
            if apple.location not in self.list_locations and apple.location \
                    not in snake.coordinates:
                self.list_locations.append(apple.location)
                return apple

    def generate_bomb(self, snake):
        """
        :param snake: object from type snake.
        :return: object from type bomb.
        generate a new bomb and appends it to the list of the locations.
        """
        while True:
            bomb = Bomb()
            if bomb.location not in self.list_locations and bomb.location \
                    not in snake.coordinates:
                self.list_locations.append(bomb.location)
                return bomb

    def apple_eaten(self, apple, score, snake):
        """
        :param apple: object from type apple.
        :param score: the score of the player.
        :param snake: object from type snake.
        :return: updating the total score.
        """
        score += apple.score
        self.apple_list.remove(apple)
        self.list_locations.remove(apple.location)
        temp_apple = self.generate_apple(snake)
        if not temp_apple:
            return False
        self.apple_list.append(temp_apple)
        return score

    def bomb_remove(self, bomb):
        """
        :param bomb: object from type bomb.
        """
        self.list_locations.remove(bomb.location)
        self.bomb_list = []

    def bomb_apple_explode(self, coordinates, snake):
        """
        :param coordinates: list of the coordinates of the explosion.
        :param snake: object from type snake.
        checks if the apple is in the radius of the explosion anf if it is,
        its make new one.
        """
        for apple in self.apple_list:
            if not self.bomb_list:
                if apple.location in coordinates:
                    self.apple_list.remove(apple)
                    self.apple_list.append(self.generate_apple(snake))

    def radius_bomb(self, radius, coordinates):
        """
        :param radius: the correct radius of the bomb.
        :param coordinates: the coordinates of the center of the bomb.
        :return: all the relevant coordinates that feel the explosion.
        """
        y, x = coordinates[0], coordinates[1]
        bomb_coord = set()
        index = radius
        if radius == 0:
            bomb_coord.add(coordinates)
            return bomb_coord
        else:
            for i in range(radius + 1):
                for j in range(index + 1):
                    if (abs(x - x + i) + abs(x - x + j)) == radius:
                        bomb_coord.add((y + i, x + j))
                    if (abs(x - x + i) + abs(x - x - j)) == radius:
                        bomb_coord.add((y + i, x - j))
                index -= 1
            index = radius
            for i in range(radius + 1):
                for j in range(index + 1):
                    if (abs(y - y - i) + abs(x - x + j)) == radius:
                        bomb_coord.add((y - i, x + j))
                    if (abs(y - y - i) + abs(x - x - j)) == radius:
                        bomb_coord.add((y - i, x - j))
                index -= 1
        return bomb_coord

    def snake_in_snake(self):
        """
        :return: checks if the snake crash in himself and return True if it is.
        """
        if self.s.location in self.s.coordinates[:-1]:
            return True

    def snake_and_bomb(self):
        """
        :return: checks if the snake crash in bomb and return True if it is.
        """
        if self.bomb_list:
            if self.s.location == self.bomb_list[0].location:
                return True

    def snake_board(self):
        """
        :return: True if the snake is outside of the board.
        """
        if not (0 <= self.s.location[0] <= game_parameters.WIDTH - 1) or not \
                (0 <= self.s.location[1] <= game_parameters.HEIGHT - 1):
            return True

    def snake_and_radius(self, coordinates):
        """
        :param coordinates: list of the explosion coordinates.
        :return: True if the snake in the range of the explosion.
        """
        for coor in self.s.coordinates:
            if not self.bomb_list:
                if coor in coordinates:
                    return True

    def end_loop(self, score, gd):
        """
        :param score: the total score of the game.
        :param gd: the game API.
        make the operation of drawing the board.
        """
        gd.show_score(score)
        self.drew_board(gd)
        gd.end_round()

    def second_end_loop(self, score, radius, b_loc, gd):
        """
        :param score: the total score of the game.
        :param radius: the radius of the explosion.
        :param b_loc: the center location of the bomb.
        :param gd: the game API.
        make the operation of drawing the board.
        """
        gd.show_score(score)
        self.drew_cell(self.s.coordinates, self.COLORS["snake"],
                       gd)
        self.drew_cell(self.radius_bomb(radius, b_loc),
                       self.COLORS["radius"], gd)
        for apple in self.apple_list:
            self.drew_cell([apple.location], self.COLORS["apple"], gd)
        gd.end_round()
