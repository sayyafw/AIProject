from White_Piece import WhitePiece
from Black_Piece import BlackPiece
from math import fabs
from Square import Square
from A_Star import A_Star
import copy

""" Board Class. Reads the board, stores board information
"""
class Board:

    # initiate Board class
    def __init__(self):
        self.board = [] # holds board string
        self.mode = ""
        self.white_pieces = []
        self.black_pieces = []
        self.squares = [] #holds square class for A* search
        self.board_width = 8
        self.board_length = 8

    # Populate board with input string
    def populate_board(self):
        for i in range(0, 8):
            self.board.append(input())
            self.board[i] = self.board[i].split()
        self.mode = input()

    # print board in list form
    def print_board(self):
        for item in self.board:
            print(item)

    # find where the black and white pieces are on the board
    def read_board(self):
        board = self.board
        print("   ")
        self.print_board()

        # Read the rows and columns of the board. Add each square to squares list. If white or black piece, add to
        #requisite list
        for i in range(len(board)):
            for j in range(len(board[i])):
                self.squares.append(Square(i, j, board[j][i]))
                if board[i][j] == "O":
                    self.white_pieces.append(WhitePiece(j, i))

                elif board[i][j] == "@":
                    self.black_pieces.append(BlackPiece(j, i))

    # find possible moves for white and black pieces
    def move(self):
        total_moves_white = 0
        total_moves_black = 0

        for white_item in self.white_pieces:
            total_moves_white += self.check_surroundings(white_item.x, white_item.y)

        print(total_moves_white)

        for black_item in self.black_pieces:
            total_moves_black += self.check_surroundings(black_item.x, black_item.y)

        print(total_moves_black)

    # check surrounding blocks for available moves. For each impossible move found, subtract one possible move
    def check_surroundings(self, x, y):
        board = self.board
        total_moves = 4

        if x == 0 or x == 7:
            total_moves -= 1

        if y == 0 or y == 7:
            total_moves -= 1

        if 1 <= x <= 6:
            if board[y][x + 1] != "-":
                # If this happens, means square cannot be jumped over or moved onto
                if x > 5 or board[y][x + 2] != "-":
                    total_moves -= 1

            if board[y][x - 1] != "-":
                # If this happens, means square cannot be jumped over or moved onto
                if x < 2 or board[y][x - 2] != "-":
                    total_moves -= 1

        if 1 <= y <= 6:

            if board[y + 1][x] != "-":
                # If this happens, means square cannot be jumped over or moved onto
                if y > 5 or board[y + 2][x] != "-":
                    total_moves -= 1

            if board[y - 1][x] != "-":
                # If this happens, means square cannot be jumped over or moved onto
                if y < 2 or board[y - 2][x] != "-":
                    total_moves -= 1

        return total_moves

    #Finds the two closest white pieces to a given coordinate. Smallest possible distance kept at min_dist_1
    def closest_piece(self, x, y):
        white_pieces = self.white_pieces

        if A_Star.manhattan_distance(x, y, white_pieces[0].x, white_pieces[0].y) > \
                A_Star.manhattan_distance(x, y, white_pieces[1].x, white_pieces[1].y):

            min_dist_1 = white_pieces[1]
            min_dist_2 = white_pieces[0]

        else:
            min_dist_1 = white_pieces[0]
            min_dist_2 = white_pieces[1]

        i = 2

        while i < len(self.white_pieces):
            manhattan_dist = A_Star.manhattan_distance(x, y, white_pieces[i].x, white_pieces[i].y)
            if manhattan_dist < A_Star.manhattan_distance(x, y, min_dist_2.x, min_dist_2.y):
                if manhattan_dist < A_Star.manhattan_distance(x, y, min_dist_1.x, min_dist_1.y):
                    min_dist_2 = copy.copy(min_dist_1)
                    min_dist_1 = white_pieces[i]

                else:
                    min_dist_2 = white_pieces[i]
            i += 1

        return min_dist_1, min_dist_2

    #Method for massacre mode
    def massacre(self):

        piece_1, piece_2 = self.closest_piece(self.black_pieces[0].x, self.black_pieces[0].y)
        available_coods = self.check_takeable(self.black_pieces[0])
        x_dir = available_coods[0]
        y_dir = available_coods[1]
        #best_dir = self.choose_best_dir(x_dir, y_dir)

        # initialises A* Search Class
        a_star_algo = A_Star(self.squares, self.board_width, self.board_length)

        # Does A* search
        a_star_algo.search(self.squares[self.black_pieces[0].x*self.board_width + self.black_pieces[0].y+1], self.board,
                    self.squares[piece_2.x * self.board_width + piece_2.y])


    # Check which of the two positions are available for taking the piece
    def check_takeable(self, bp):
        board = self.board
        available_coods = []

        # Check if takeable in x direction
        if 1 <= bp.x <= 6:
            # Check if both spaces in x direction free
            if board[bp.y][bp.x - 1] == "-" and board[bp.y][bp.x + 1] == "-":
                available_coods.append([bp.y, bp.x - 1, bp.y, bp.x + 1])

            elif board[bp.y][bp.x - 1] == "-" and board[bp.y][bp.x + 1] == "O":
                available_coods.append([bp.y, bp.x - 1])

            elif board[bp.y][bp.x - 1] == "O" and board[bp.y][bp.x + 1] == "-":
                available_coods.append([bp.y, bp.x + 1])
            else:
                available_coods.append([])

        # Check if takeable in y direction
        if 1 <= bp.y <= 6:
            # Check if both spaces in y direction free
            if board[bp.y - 1][bp.x] == "-" and board[bp.y + 1][bp.x] == "-":
                available_coods.append([bp.y - 1, bp.x, bp.y + 1, bp.x])

            # Check if one space already covered by white piece and other free
            elif board[bp.y - 1][bp.x] == "-" and board[bp.y + 1][bp.x] == "O":
                available_coods.append([bp.y - 1, bp.x])

            elif board[bp.y - 1][bp.x] == "O" and board[bp.y + 1][bp.x] == "-":
                available_coods.append([bp.y + 1, bp.x])

            else:
                available_coods.append([])

        return available_coods


    def choose_best_dir(self, x_dir, y_dir):

        if not x_dir and not y_dir:
            return None

        elif not x_dir or len(y_dir) < len(x_dir):
            return y_dir

        elif not y_dir or len(x_dir) <= len(y_dir):
            return x_dir

        else:
            return x_dir













