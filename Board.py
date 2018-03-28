from White_Piece import WhitePiece
from Black_Piece import BlackPiece
from math import fabs


class Board:

    #initiate Board class
    def __init__(self):
        self.board = []
        self.mode = ""
        self.white_pieces = []
        self.black_pieces = []

    #Populate board with input string
    def populate_board(self):
        for i in range(0, 8):
            self.board.append(input())
            self.board[i] = self.board[i].split()

        self.mode = input()

    #print board in list form
    def print_board(self):
        for item in self.board:
            print(item)

    #find where the black and white pieces are on the board
    def read_board(self):
        board = self.board
        print( "   ")
        self.print_board()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == "O":
                    self.white_pieces.append(WhitePiece(j, i))

                elif board[i][j] == "@":
                    self.black_pieces.append(BlackPiece(j, i))


    def move(self):

        total_moves_black = 0
        total_moves_white = 0

        for wp in self.white_pieecs:

            total_moves_white += self.check_moves(wp)

        print(total_moves_white)

        for bp in self.black_pieces:
            total_moves_black == self.check_moves(bp)

        print(total_moves_black)


    def check_moves(self, piece):

        availables_moves = 0

        if self.check_move(piece, piece.y_coordinate - 1, piece.x_coordinate) > 0:
            availables_moves  += 1

        if self.check_move(piece, piece.y_coordinate + 1, piece.x_coordinate) > 0:
            availables_moves += 1

        if self.check_move(piece,piece.y_coordinate, piece.x_coordinate - 1) > 0:
            availables_moves += 1

        if self.check_move(piece, piece.y_coordinate + 1, piece.x_coordinate + 1) > 0:
            availables_moves += 1

        return availables_moves

    def check_move(self, piece, y, x):
        

    """"#find possible moves for white pieces
    def move(self):
        total_moves_white = 0
        total_moves_black = 0

        for item in self.white_pieces:
            total_moves_white += self.check_surroundings(item.x_coordinate, item.y_coordinate)

        print(total_moves_white)

        for black_item in self.black_pieces:
            total_moves_black += self.check_surroundings(item.x_coordinate, item.y_coordinate)

        print(total_moves_black)

    #check surrounding blocks for available moves
    def check_surroundings(self, x_coordinate, y_coordinate):
        board = self.board
        total_moves = 4
        if x_coordinate ==0 or x_coordinate == 7:
            total_moves-=1

        if y_coordinate == 0 or y_coordinate == 7:
            total_moves -= 1

        if 1 <= x_coordinate <= 6:
            if board[y_coordinate][x_coordinate + 1] != "-":
                if board[y_coordinate][x_coordinate + 2] != "-":
                    total_moves -= 1

            if board[y_coordinate][x_coordinate - 1] != "-":
                if  board[y_coordinate][x_coordinate - 2] != "-":
                    total_moves -= 1

        if 1 <= y_coordinate <= 6:

            if board[y_coordinate + 1][x_coordinate] != "-":
                if board[y_coordinate + 2][x_coordinate] != "-":
                    total_moves -= 1

            if board[y_coordinate - 1][x_coordinate] != "-":
                if board[y_coordinate - 2][x_coordinate] != "-":
                    total_moves -= 1

        return total_moves

    #def massacre(self):


    def manhattan_distance(self, black_piece, white_piece):

        dist_x = fabs((black_piece.x_coordinate - white_piece.x_coordinate))
        dist_y = fabs((black_piece.y_coordinate - white_piece.y_coordinate))
        return dist_x + dist_y

    # make piece 1 piece 2

    def closest_piece(self, piece):

        white_pieces = self.white_pieces

        if self.manhattan_distance(piece, white_pieces[0]) > self.manhattan_distance(piece, white_pieces[1]):

            min_dist_1 = white_pieces[1]
            min_dist_2 = white_pieces[0]

        else:
            min_dist_1 = white_pieces[1]
            min_dist_2 = white_pieces[0]

        i = 2

        while i < len(self.white_pieces):
            manhattan_dist = self.manhattan_distance(piece, white_pieces[i])
            if manhattan_dist < self.manhattan_distance(piece, min_dist_2):
                if manhattan_dist <  self.manhattan_distance(piece, min_dist_1):
                    min_dist_2 = min_dist_1
                    min_dist_1 = white_pieces[i]

                else:
                    min_dist_2 = white_pieces[i]
            i += 1

        return piece.x_coordinate, piece.y_coordinate, min_dist_1.x_coordinate, min_dist_1.y_coordinate, min_dist_2.x_coordinate, min_dist_2.y_coordinate



    def check_takeable(self, bp):

        board = self.board

        if board[bp.y_coordinates + 1][bp.x_coordinates] != "-":

        """















