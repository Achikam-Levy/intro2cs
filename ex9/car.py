#################################################################
# FILE : car.py
# WRITER : achikam levy , aaa997 , 208764944
# EXERCISE : intro2cs2 ex6 2021
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################
class Car:
    """
    class car define all the car object methods
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name:A string representing the car's name
        :param length:A positive int representing the car's length.
        :param location:A tuple representing the car's head (row, col) location
        :param orientation:One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        lst = []

        if self.orientation == 1 and self.length > 0:
            cell = self.location
            for i in range(self.length):
                lst.append((cell[0], cell[1] + i))

        if self.orientation == 0 and self.length > 0:
            cell = self.location
            for i in range(self.length):
                lst.append((cell[0] + i, cell[1]))

        return lst

    def possible_moves(self):
        """
        :return: A dictionary of strings describing
        possible movements permitted by this car.
        """
        moves_dict = {}

        if self.orientation == 0 and self.length > 0:
            moves_dict = {'u': 'moves car up',
                          'd': 'moves car down'}
            return moves_dict

        if self.orientation == 1 and self.length > 0:
            moves_dict = {'r': 'moves car right',
                          'l': 'moves car left'}
            return moves_dict

        else:
            return moves_dict

    def movement_requirements(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty
        in order for this move to be legal.
        """
        empty_cell = []

        if self.orientation == 0 and self.length > 0:

            if movekey == 'd':
                cells = self.car_coordinates()
                cell = cells[len(cells) - 1]
                empty_cell = [(cell[0] + 1, cell[1])]
            if movekey == 'u':
                cells = self.car_coordinates()
                cell = cells[0]
                empty_cell = [(cell[0] - 1, cell[1])]

        if self.orientation == 1 and self.length > 0:

            if movekey == 'r':
                cells = self.car_coordinates()
                cell = cells[len(cells) - 1]
                empty_cell = [(cell[0], cell[1] + 1)]
            if movekey == 'l':
                cells = self.car_coordinates()
                cell = cells[0]
                empty_cell = [(cell[0], cell[1] - 1)]

        return empty_cell

    def move(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        possible_moves = self.possible_moves()

        if movekey in possible_moves and self.length > 0:
            if movekey == 'r':
                self.location = (self.location[0], self.location[1] + 1)
            if movekey == 'l':
                self.location = (self.location[0], self.location[1] - 1)
            if movekey == 'd':
                self.location = (self.location[0] + 1, self.location[1])
            if movekey == 'u':
                self.location = (self.location[0] - 1, self.location[1])
            return True

        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
