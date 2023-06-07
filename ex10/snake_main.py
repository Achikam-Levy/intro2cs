######################################
# File : snake_main.py
# WRITER : yotam_suliman yotamsu26 206922205,
# EXERCISE intro2cs1 ex10 2021
# Students I spoke to about the exercise: none
# Web pages I used : none
######################################
from game_display import GameDisplay
from game import *

COLORS = {"snake": "black", "bomb": "red", "apple": "green",
          "radius": "orange"}


def main_loop(gd: GameDisplay):
    """
    Running and manging the game.
    """
    score = 0
    game = Game()
    direction = "Up"
    bomb_counter = game.bomb_list[0].time
    radius = game.bomb_list[0].radius
    b_loc = game.bomb_list[0].location
    apple_counter = 0

    game.end_loop(score, gd)
    while True:  # Running one iteration every time until the game stops

        key_clicked = gd.get_key_clicked()
        if key_clicked in game.s.possible_moves():  # get the direction
            # from the user.
            direction = key_clicked
        game.s.add_snake_coordinates(direction)
        if apple_counter == 0:
            game.s.remove_snake_coordinates(direction)

        if game.snake_board():  # checks if the snake is inside the board.
            game.end_loop(score, gd)
            break

        if game.snake_in_snake():  # checks if the snake is not crash
            # in himself.
            game.end_loop(score, gd)
            break

        if game.snake_and_bomb():  # checks if the snake didn't crash a bomb.
            game.end_loop(score, gd)
            break

        if apple_counter > 0:
            apple_counter -= 1

        if game.eat_apple():  # checks if the snake eat an apple.
            apple_counter = 3
            score += game.eat_apple().score
            if not game.apple_eaten(game.eat_apple(),
                                    game.eat_apple().score, game.s):
                game.end_loop(score, gd)
                break

        if bomb_counter == 1:  # checks if the bomb exploded.
            game.bomb_remove(game.bomb_list[0])

        if bomb_counter <= 1:
            if abs(bomb_counter) == radius:
                game.bomb_list.append(game.generate_bomb(game.s))
                bomb_counter = game.bomb_list[0].time
                radius = game.bomb_list[0].radius
                b_loc = game.bomb_list[0].location
            else:
                game.drew_cell(game.radius_bomb(abs(bomb_counter - 1), b_loc),
                               "orange", gd)
                game.bomb_apple_explode(game.radius_bomb(abs(bomb_counter - 1),
                                                         b_loc), game.s)
                if game.snake_and_radius(game.radius_bomb(abs(bomb_counter
                                                              - 1), b_loc)):
                    game.second_end_loop(score, abs(bomb_counter - 1), b_loc,
                                         gd)
                    break
        bomb_counter -= 1
        game.end_loop(score, gd)  # shows the game board.


