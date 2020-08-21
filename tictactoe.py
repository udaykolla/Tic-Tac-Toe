import random


class PlayerIsUser:
    def __init__(self, field, level, item):
        self.coord = []
        self.field = field
        self.item = item

    def get_coordinates(self):
        """Get coordinates from user input and check it for errors"""
        while True:
            print('Enter the coordinates: ')
            self.coord = input().split()  # coord[0] - row and coord[1] - col
            # check the two coordinates is digits
            if not self.coord[0].isdigit() or not self.coord[1].isdigit():
                print('You should enter numbers!')
                continue
            # check that the two coordinates are there
            if len(self.coord) != 2:
                print('You should enter two numbers of coordinates.')
                continue
            # convert string list to integers list
            self.coord = [int(ui) - 1 for ui in self.coord]
            # check the correct range of numbers
            if not (0 <= self.coord[0] < 3 and 0 <= self.coord[1] < 3):
                print('Coordinates should be from 1 to 3!')
                continue

            # reverse coordinates
            self.coord[1] = 2 - self.coord[1]
            self.coord[0], self.coord[1] = self.coord[1], self.coord[0]

            # check is this cell occupied?
            if self.field[self.coord[0]][self.coord[1]] != ' ':
                print('This cell is occupied! Choose another one!')
                continue
            # if all right exit from here
            break

    def make_move(self):
        """Make user's move according to entered coordinates"""
        self.get_coordinates()
        self.field[self.coord[0]][self.coord[1]] = self.item


class PlayerIsAI:
    def __init__(self, field, level, item):
        self.coord = []
        self.field = field
        self.level = level
        self.item = item
        self.item_opponent = 'O' if item == 'X' else 'X'

    # ---=== EASY LEVEL ===---
    # At this level the AI will takes random coordinates
    def get_ai_coord_for_easy(self):
        """Get coordinates for AI move for easy level"""
        # get the list of coordinates of empty cells
        empty_cells = [[row, col] for row in range(len(self.field))
                       for col in range(len(self.field[row]))
                       if self.field[row][col] == ' ']
        # take the coordinates of a random empty cell
        self.coord = random.choice(empty_cells)

    # ---=== MEDIUM LEVEL ===---
    # 1. if it can win in one move (if it has two in a row), it places a third to get three in a row and win.
    # 2. if the opponent can win in one move, it plays the third itself to block the opponent to win.
    # 3. otherwise, it makes a random move.
    def get_priority_cell(self, item):
        """Get priority cell, return True if get it otherwise False"""
        # check for horizontal items in a row as two item and empty one
        for row in range(len(self.field)):
            if self.field[row].count(item) == 2 and self.field[row].count(' ') == 1:
                self.coord = [row, self.field[row].index(' ')]
                return True
        # check for vertical items in a row as two item and empty one
        for col in range(len(self.field[0])):
            column = [self.field[row][col] for row in range(len(self.field))]
            if column.count(item) == 2 and column.count(' ') == 1:
                self.coord = [column.index(' '), col]
                return True
        # check the elements in a row diagonally from the upper left corner
        diag = [self.field[i][i] for i in range(len(self.field))]
        if diag.count(item) == 2 and diag.count(' ') == 1:
            idx = diag.index(' ')
            self.coord = [idx, idx]
            return True
        # check the elements in a row diagonally from the lower left corner
        diag = [self.field[i][len(self.field) - 1 - i] for i in range(len(self.field))]
        if diag.count(item) == 2 and diag.count(' ') == 1:
            idx = diag.index(' ')
            self.coord = [idx, len(self.field) - 1 - idx]
            return True
        return False

    def get_ai_coord_for_medium(self):
        """Get coordinates for AI move for medium level"""
        # 1. if it can win in one move (if it has two in a row), it places a third to get three in a row and win.
        if self.get_priority_cell(self.item):
            return
        # 2. if the opponent can win in one move, it plays the third itself to block the opponent to win.
        if self.get_priority_cell(self.item_opponent):
            return
        # 3. otherwise, it makes a random move.
        empty_cells = [[row, col] for row in range(len(self.field))
                       for col in range(len(self.field[row]))
                       if self.field[row][col] == ' ']
        # take the coordinates of a random empty cell
        self.coord = random.choice(empty_cells)

    # ---=== HARD LEVEL ===---
    # Based on MiniMax Algorithm in Game Theory
    # https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/

    # Player 'O' is max
    def max(self):
        # Possible values for maxv are: -1 - loss, 0 - a tie, 1 - win
        maxv = -2  # We're initially setting it to -2 as worse than the worst case
        x = None
        y = None
        result = TicTacToe.check_game_status(self)

        # If the game came to an end, the function needs to return the evaluation function of the end.
        # That can be: -1 - loss, 0 - a tie, 1  - win
        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result is True:
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.field[i][j] == ' ':
                    # On the empty field player 'O' makes a move and calls Min
                    # That's one branch of the game tree.
                    self.field[i][j] = 'O'
                    m, min_i, min_j = self.min()
                    # Fixing the maxv value if needed
                    if m > maxv:
                        maxv = m
                        x = i
                        y = j
                    # Setting back the field to empty
                    self.field[i][j] = ' '
        return maxv, x, y

    # Player 'X' is min
    def min(self):
        # Possible values for minv are: -1 - win, 0 - a tie, 1 - loss
        minv = 2  # We're initially setting it to 2 as worse than the worst case
        x = None
        y = None
        result = TicTacToe.check_game_status(self)

        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result is True:
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.field[i][j] == ' ':
                    self.field[i][j] = 'X'
                    m, max_i, max_j = self.max()
                    if m < minv:
                        minv = m
                        x = i
                        y = j
                    self.field[i][j] = ' '
        return minv, x, y

    def get_ai_coord_for_hard(self):
        """Get coordinates for AI move for hard level"""
        # If it's X player
        if self.item == 'X':
            m, row, col = self.min()
            self.coord = [row, col]
        # If it's O player
        else:
            m, row, col = self.max()
            self.coord = [row, col]

    def make_move(self):
        """Make AI's move in accordance with the selected level and rules"""
        if self.level == 'easy':
            self.get_ai_coord_for_easy()
            print('Making move level "easy"')
        elif self.level == 'medium':
            self.get_ai_coord_for_medium()
            print('Making move level "medium"')
        else:
            self.get_ai_coord_for_hard()
            print('Making move level "hard"')
        self.field[self.coord[0]][self.coord[1]] = self.item


class TicTacToe:
    def __init__(self):
        self.player_1 = None
        self.player_2 = None
        self.command = ['easy', 'medium', 'hard', 'user']
        self.field = [[' ', ' ', ' '],  # (1, 3) (2, 3) (3, 3)
                      [' ', ' ', ' '],  # (1, 2) (2, 2) (3, 2)
                      [' ', ' ', ' ']]  # (1, 1) (2, 1) (3, 1)
        self.game_logic()

    def print_field(self):
        """Output the 3x3 field with cells"""
        print('---------')
        for i in range(3):
            out = '| '
            for j in range(3):
                out += self.field[i][j] + ' '
            out += '|'
            print(out)
        print('---------')

    def check_game_status(self):
        """Check the state of the game, return who is won,
        if status draw it return True, if game not end return False"""
        # check for horizontal items in a row
        for i in range(0, 3):
            if self.field[i] == ['X', 'X', 'X']:
                return 'X'
            elif self.field[i] == ['O', 'O', 'O']:
                return 'O'
        # check for vertical items in a row
        for i in range(0, 3):
            if (self.field[0][i] != ' ' and
                    self.field[0][i] == self.field[1][i] and
                    self.field[1][i] == self.field[2][i]):
                return self.field[0][i]
        # check the same elements in a row diagonally from the upper left corner
        if (self.field[0][0] != ' ' and
                self.field[0][0] == self.field[1][1] and
                self.field[0][0] == self.field[2][2]):
            return self.field[0][0]
        # check the same elements in a row diagonally from the lower left corner
        if (self.field[0][2] != ' ' and
                self.field[0][2] == self.field[1][1] and
                self.field[0][2] == self.field[2][0]):
            return self.field[0][2]
        # check if game has status draw
        for row in self.field:
            if ' ' in row:  # if we have an empty cell, then continue the game
                return False
        # it's draw
        return True

    def command_handler(self):
        """Handles user command input, if an exit command is entered it returns false, otherwise true"""
        while True:
            print('Input command:')
            user_input = input().split()
            if user_input[0] == 'exit':
                return False
            # check the correct input of the command
            if len(user_input) != 3 or user_input[0] != 'start':
                print('Bad parameters!')
                continue
            for i in range(1, 2):
                if not any(user_input[i] == command for command in self.command):
                    print('Bad parameters!')
                    continue
            # determine who will play for the first player
            if user_input[1] == 'user':
                self.player_1 = PlayerIsUser(self.field, user_input[1], 'X')
            else:
                self.player_1 = PlayerIsAI(self.field, user_input[1], 'X')
            # determine who will play for the second player
            if user_input[2] == 'user':
                self.player_2 = PlayerIsUser(self.field, user_input[2], 'O')
            else:
                self.player_2 = PlayerIsAI(self.field, user_input[2], 'O')
            return True

    def game_logic(self):
        """Performs the main sequence of actions of the game in accordance with the selected level and rules"""
        # When starting the program, an empty field should be displayed
        # and the first to start the game should be the user as X.
        # Next the computer should make its move as O.
        # And so on until someone will win or there will be a draw.
        if self.command_handler():
            self.print_field()
            whose_turn = 1  # whose turn is it to make a move? 1-player_1, 2-player_2
            while True:
                if whose_turn == 1:
                    # to make a move player_1
                    self.player_1.make_move()
                    self.print_field()
                    whose_turn = 2
                else:
                    # to make a move player_2
                    self.player_2.make_move()
                    self.print_field()
                    whose_turn = 1

                winner = self.check_game_status()
                if winner is True:
                    print('Draw')
                    break
                if winner == 'X' or winner == 'O':
                    print(winner, 'wins')
                    break


tic = TicTacToe()