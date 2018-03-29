from White_Piece import WhitePiece
from Black_Piece import BlackPiece
from Square import Square
from A_Star import AStarSearch
import copy

""" Board Class. Reads the board, stores board information
"""
board_width = 8
board_length = 8
#after a while, the boundries shrink, this is used to keep track
boundry = 0

class Board:
    # initiate Board class
    def __init__(self):
        self.board = [] # holds board string
        self.mode = ""
        self.white_pieces = []
        self.black_pieces = []
        self.squares = [] # holds square class for A* search

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

        #print "empty" line for formatting
        print("   ")
        self.print_board()

        # Read the rows and columns of the board. Add each square to squares list.
        # Add pieces to their corresponding list
        for i in range(len(board)):
            for j in range(len(board[i])):
                #register the location into Square
                self.squares.append(Square(i, j, board[j][i]))

                if board[i][j] == "O":
                    self.white_pieces.append(WhitePiece(j, i))

                elif board[i][j] == "@":
                    self.black_pieces.append(BlackPiece(j, i))

    # find possible moves for white and black pieces
    def move(self):
        total_moves_white = 0
        total_moves_black = 0

        #for every white and black pieces, check it's possible moves
        for white_item in self.white_pieces:
            total_moves_white += self.check_surroundings(white_item.x, white_item.y)

        print(total_moves_white)

        for black_item in self.black_pieces:
            total_moves_black += self.check_surroundings(black_item.x, black_item.y)

        print(total_moves_black)

    # check surrounding blocks for available moves.
    def check_surroundings(self, x, y):
        board = self.board
        # For each impossible move found, subtract one possible move
        total_moves = 4

        #check if the x axis is on the edge
        if x == 0+boundry or x == 7-boundry:
            total_moves -= 1

        #check if the y axis is on the edge
        if y == 0+boundry or y == 7-boundry:
            total_moves -= 1

        #check for each boundaries, if it fails, substract a possible move
        if 1 <= x <= 6:
            if board[y][x + 1] != "-":
                if x > 5 or board[y][x + 2] != "-":
                    total_moves -= 1

            if board[y][x - 1] != "-":
                if x < 2 or board[y][x - 2] != "-":
                    total_moves -= 1

        if 1 <= y <= 6:

            if board[y + 1][x] != "-":
                if y > 5 or board[y + 2][x] != "-":
                    total_moves -= 1

            if board[y - 1][x] != "-":
                if y < 2 or board[y - 2][x] != "-":
                    total_moves -= 1

        return total_moves

    # Finds the two closest white pieces to a given coordinate.
    def closest_piece(self, x, y):
        white_pieces = self.white_pieces

        #search for the first 2 closes pieces, and order them
        if AStarSearch.manhattan_distance(x, y, white_pieces[0].x, white_pieces[0].y) > \
                AStarSearch.manhattan_distance(x, y, white_pieces[1].x, white_pieces[1].y):

            min_dist_1 = white_pieces[1]
            min_dist_2 = white_pieces[0]

        else:
            min_dist_1 = white_pieces[0]
            min_dist_2 = white_pieces[1]

        #start going through all the white pieces.
        i = 2
        while i < len(self.white_pieces):
            manhattan_dist = AStarSearch.manhattan_distance(x, y, white_pieces[i].x, white_pieces[i].y)
            #if the distance is smaller than the 2nd smallest
            if manhattan_dist < AStarSearch.manhattan_distance(x, y, min_dist_2.x, min_dist_2.y):
                #check if it is also smaller than the smallest
                if manhattan_dist < AStarSearch.manhattan_distance(x, y, min_dist_1.x, min_dist_1.y):
                    #if so, move it in
                    min_dist_2 = copy.copy(min_dist_1)
                    min_dist_1 = white_pieces[i]
                #elsewise, replace2nd smallest only
                else:
                    min_dist_2 = white_pieces[i]
            i += 1

        return min_dist_1, min_dist_2

    # Method for massacre mode
    def massacre(self):
        #check for every single black pieces.
        for item in self.black_pieces:
            #coords*
            #find the coords that can takeaway this black piece
            available_coods = self.check_takeable(item)
            x_dir = available_coods[0]
            y_dir = available_coods[1]
            best_dir, piece_1, piece_2 = self.choose_best_dir(x_dir, y_dir)

            # initialises A* Search Class
            a_star_algo_1 = AStarSearch(self.squares, board_width, board_length)

            # Does A* search
            self.squares, new_location = a_star_algo_1.search(self.squares[best_dir[1] * board_width + best_dir[0]],
                                                self.squares[piece_1.x * board_width + piece_1.y])

            self.update_pieces(new_location, piece_1)
            self.squares, new_location = a_star_algo_1.search(self.squares[best_dir[3] * board_width + best_dir[2]],
                                                self.squares[piece_2.x * board_width + piece_2.y])
            self.update_pieces(new_location, piece_2)

    def update_pieces(self, new_location, piece):

        if new_location.value == "O":
            self.squares[new_location.x * board_width + new_location.y].value = "O"

            for item in self.white_pieces:
                if item.x == piece.x and item.y == piece.y:
                    item.x = new_location.x
                    item.y = new_location.y

            self.squares[piece.x * board_width + new_location.y].value = "-"

    # Check which of the two positions are available for taking the piece
    def check_takeable(self, bp):
        squares = self.squares
        available_coods = []

        # Check if takeable in x direction
        if 1 <= bp.x <= 6:
            # Check if both spaces in x direction free
            # first check if both squares are empty.
            if squares[(bp.x-1) * board_width + bp.y].value == "-" and \
                    squares[(bp.x + 1) * board_width + bp.y].value == "-":
                available_coods.append([bp.y, bp.x - 1, bp.y, bp.x + 1])
            # check if either is a white piece
            elif squares[(bp.x-1) * board_width + bp.y].value == "O" and \
                    squares[(bp.x + 1) * board_width + bp.y].value =="-":
                available_coods.append([bp.y, bp.x - 1, bp.y, bp.x + 1])

            elif squares[(bp.x-1) * board_width + bp.y].value == "-" and \
                    squares[(bp.x + 1) * board_width + bp.y].value =="O":
                available_coods.append([bp.y, bp.x - 1, bp.y, bp.x + 1])
            #elsewise append empty list to indicate x cannot pincer 
            else:
                available_coods.append([])

        # Check if takeable in y direction
        if 1 <= bp.y <= 6:
            # Check if both spaces in y direction free
            if squares[bp.x * board_width + (bp.y - 1)].value == "-" and \
                    squares[bp.x * board_width + (bp.y + 1)].value =="-":
                available_coods.append([bp.y - 1, bp.x, bp.y + 1, bp.x])

            # Check if one space already covered by white piece and other free
            elif squares[bp.x * board_width + (bp.y - 1)].value == "O" and \
                    squares[bp.x * board_width + (bp.y + 1)].value =="-":
                available_coods.append([bp.y - 1, bp.x, bp.y + 1, bp.x])

            elif squares[bp.x * board_width + (bp.y - 1)].value == "-" and \
                    squares[bp.x * board_width + (bp.y + 1)].value =="O":
                available_coods.append([bp.y - 1, bp.x, bp.y + 1, bp.x])

            else:
                available_coods.append([])

        return available_coods

    #
    def choose_best_dir(self, x_dir, y_dir):

        #if untakeable
        if not x_dir and not y_dir:
            return None
        #if x pincer untakeable, but can be pincered via y
        elif not x_dir:
            piece3, piece4 = self.closest_piece(y_dir[1], y_dir[0])
            return y_dir, piece3, piece4

        elif not y_dir:
            piece1, piece2 = self.closest_piece(x_dir[1], x_dir[0])
            return x_dir, piece1, piece2

        piece1, piece2 = self.closest_piece(x_dir[1], x_dir[0])

        print(x_dir, y_dir)
        #calculate the manhattan distance for the steps to pincer
        x_dist_1 = AStarSearch.manhattan_distance(x_dir[1], piece1.x, x_dir[0], piece1.y)
        x_dist_2 = AStarSearch.manhattan_distance(x_dir[3], piece2.x, x_dir[2], piece2.y)
        print(x_dist_1, x_dist_2)

        piece3, piece4 = self.closest_piece(y_dir[1], y_dir[0])

        y_dist_1 = AStarSearch.manhattan_distance(y_dir[1], piece3.x, y_dir[0], piece3.y)
        y_dist_2 = AStarSearch.manhattan_distance(y_dir[3], piece4.x, y_dir[2], piece4.y)
        print(y_dist_1, y_dist_2)

        #based on which total distance is shorter, move the corresponded pieces
        if x_dist_1 + x_dist_2 <= y_dist_1 + y_dist_2:

            return x_dir, piece1, piece2

        else:
            return y_dir, piece3, piece4