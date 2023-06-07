#################################################################
# FILE : snake_board.py
# WRITER : achikam levy , aaa997 , 208764944
# EXERCISE : intro2cs2 ex6 2021
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################
class Board:
    """
    class board, define all the board object methods
    """
    def __init__(self):
        self.__size = 7
        self.exit = (3, 7)
        self.current_board = self.empty_board()
        self.current_cars_dict = {}

    def empty_board(self):
        """
        initialize an empty board list
        :return: empty board
        """
        board = []

        for r in range(self.__size):
            row = []
            for c in range(self.__size + 1):
                if c < 7:
                    row.append('_')
                if c == 7:
                    row.append('*')
            board.append(row)
        board[3][7] = '_'

        return board

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        board_print = ""

        for row in range(len(self.current_board)):
            board_print += '\n'
            for col in range(len(self.current_board) + 1):
                board_print += self.current_board[row][col] + '    '

        return board_print

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        board = []

        for r in range(self.__size):
            board.append((r, 0))
            for c in range(1, self.__size):
                board.append((r, c))
                if r == 3 and c == 6:
                    board.append((3, 7))

        return board

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description)
                 representing legal moves
        """
        lst = []

        for car in self.current_cars_dict.values():
            if car.get_name() in self.current_cars_dict.keys():
                length = car.length
                orientation = car.orientation
                name = car.get_name()
                coordination = car.car_coordinates()

                if orientation == 1:
                    dest_r = (coordination[length - 1][0],
                              coordination[length - 1][1] + 1)
                    dest_l = (coordination[0][0], coordination[0][1] - 1)
                    if self.cell_content(
                            dest_r) is None and dest_r in self.cell_list():
                        lst.append((name, 'r', "move right is legal"))
                    if self.cell_content(
                            dest_l) is None and dest_l in self.cell_list():
                        lst.append((name, 'l', "move left is legal"))

                if orientation == 0:
                    dest_d = (coordination[length - 1][0] + 1,
                              coordination[length - 1][1])
                    dest_u = (coordination[0][0] - 1, coordination[0][1])
                    if self.cell_content(
                            dest_u) is None and dest_u in self.cell_list():
                        lst.append((name, 'u', "move up is legal"))
                    if self.cell_content(
                            dest_d) is None and dest_d in self.cell_list():
                        lst.append((name, 'd', "move down is legal"))
        return lst

    def target_location(self):
        """
        This function returns the coordinates of the
        location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return self.exit

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        coordinate = list(coordinate)
        row = coordinate[0]
        col = coordinate[1]

        if (0 <= row < 7 and 0 <= col < 7) or coordinate == [3, 7]:
            if self.current_board[row][col] != '_':
                return self.current_board[row][col]
            return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        name = car.get_name()
        orientation = [0, 1]
        coordination = car.car_coordinates()
        add = True

        for coordinate in coordination:
            if (car.length < 1 or car.length > 7
                    or car.orientation not in orientation
                    or coordinate not in self.cell_list()
                    or name in self.current_cars_dict.keys()
                    or self.cell_content(
                        (coordinate[0], coordinate[1])) is not None):
                return False

        if add:
            for coordinate in coordination:
                self.current_board[coordinate[0]][coordinate[1]] = name
                self.current_cars_dict[name] = car
            return add

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        new_coordination = []
        move = False
        direction = movekey
        car = self.current_cars_dict.get(name)

        if name in self.current_cars_dict:
            for tuple_move in self.possible_moves():
                if name in tuple_move and direction in tuple_move:
                    coordination = car.car_coordinates()
                    move = True

                    if direction == 'r':
                        self.current_board[coordination[0][0]][
                            coordination[0][1]] = '_'
                        for coordinate in coordination:
                            coordinate = (coordinate[0], coordinate[1] + 1)
                            new_coordination.append(coordinate)

                    if direction == 'l':
                        self.current_board[coordination[-1][0]][
                            coordination[-1][1]] = '_'
                        for coordinate in coordination:
                            coordinate = (coordinate[0], coordinate[1] - 1)
                            new_coordination.append(coordinate)

                    if direction == 'd':
                        self.current_board[coordination[0][0]][
                            coordination[0][1]] = '_'
                        for coordinate in coordination:
                            coordinate = (coordinate[0] + 1, coordinate[1])
                            new_coordination.append(coordinate)

                    if direction == 'u':
                        self.current_board[coordination[-1][0]][
                            coordination[-1][1]] = '_'
                        for coordinate in coordination:
                            coordinate = (coordinate[0] - 1, coordinate[1])
                            new_coordination.append(coordinate)

                    car.location = new_coordination[0]

        if move:
            for coordinate in new_coordination:
                self.current_board[coordinate[0]][coordinate[1]] = name

        return move
