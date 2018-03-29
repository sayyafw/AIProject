from White_Piece import WhitePiece
from Black_Piece import BlackPiece
from Square import Square
from A_Star import AStarSearch
import copy

""" Board Class. Reads the board, stores board information
"""
board_width = 8
board_length = 8


class Board:
    # initiate Board class
    def __init__(self):
        self.board = []  # holds board string
        self.mode = ""
        self.white_pieces = []
        self.black_pieces = []
        self.squares = []  # holds square class for A* search

    # Populate board with input string
    def populate_board(self):
        for i in range(0, 8):
            #for each row is split into and array
            self.board.append(input())
            self.board[i] = self.board[i].split()
        self.mode = input()

    # print board in readable form
    def print_board(self):
        for item in self.board:
            print(item)

    # find where the black and white pieces are on the board
    def read_board(self):
        board = self.board
        #print an "empty" line for formatting 
        print("   ")
        self.print_board()

        #for each row on the board
        for i in range(len(board)):
            #for each column in the row
            for j in range(len(board[i])):
                #add this to the list of squares
                self.squares.append(Square(i, j, board[j][i]))
                #and add an piece corresponded to its' colour
                if board[i][j] == "O":
                    self.white_pieces.append(WhitePiece(j, i))

                elif board[i][j] == "@":
                    self.black_pieces.append(BlackPiece(j, i))

    # find amount of possible moves for white and black pieces
    def move(self):
        total_moves_white = 0
        total_moves_black = 0

        for white_item in self.white_pieces:
            total_moves_white += self.surrounding(white_item.x, white_item.y)

        print(total_moves_white)

        for black_item in self.black_pieces:
            total_moves_black += self.surrounding(black_item.x, black_item.y)

        print(total_moves_black)

    # check surrounding blocks and count available moves
    def surrounding(self, x, y):
        board = self.board
        #maximum 4 possible moves, substract for each impossible move
        total_moves = 4

        #check if x, y is on the edge of the board.
        if x == 0 or x == 7:
            total_moves -= 1

        if y == 0 or y == 7:
            total_moves -= 1

        #if x is within boundary of the board.
        if 1 <= x <= 6:
            #if to the right is not empty
            if board[y][x + 1] != "-":
                #then check if it can be jumped over
                if x > 5 or board[y][x + 2] != "-":
                    #cannot be jumped over, found an impossible move
                    total_moves -= 1
            #same as above, but for a different axis
            if board[y][x - 1] != "-":
                if x < 2 or board[y][x - 2] != "-":
                    total_moves -= 1

        if 1 <= y <= 6:
            #same as above, but for a different axis
            if board[y + 1][x] != "-":
                if y > 5 or board[y + 2][x] != "-":
                    total_moves -= 1
            #same as above, but for a different axis
            if board[y - 1][x] != "-":
                if y < 2 or board[y - 2][x] != "-":
                    total_moves -= 1

        return total_moves

    # Finds the two closest white pieces to a given coordinate.
    def closest_piece(self, x, y):
        white_pieces = self.white_pieces

        if AStarSearch.manhattan_distance(x, y, white_pieces[0].x, 
            white_pieces[0].y) > AStarSearch.manhattan_distance(x, y, 
            white_pieces[1].x, white_pieces[1].y):

            min_dist_1 = white_pieces[1]
            min_dist_2 = white_pieces[0]

        else:
            min_dist_1 = white_pieces[0]
            min_dist_2 = white_pieces[1]

        i = 2

        while i < len(self.white_pieces):
            manhattan_dist = AStarSearch.manhattan_distance(x, y, 
                white_pieces[i].x, white_pieces[i].y)
            if manhattan_dist < AStarSearch.manhattan_distance(x, y, 
                min_dist_2.x, min_dist_2.y):
                if manhattan_dist < AStarSearch.manhattan_distance(x, y, 
                    min_dist_1.x, min_dist_1.y):
                    min_dist_2 = copy.copy(min_dist_1)
                    min_dist_1 = white_pieces[i]

                else:
                    min_dist_2 = white_pieces[i]
            i += 1

        return min_dist_1, min_dist_2

    # Method for massacre mode
    def massacre(self):
        #iterate through every black piece on the board
        for item in self.black_pieces:
            #find the positions that can eat this piece
            available_coords = self.check_takeable(item)
            #------------------------------------------------------------------------------
            if available_coords == [[], []]:
                continue
            #get the 2 pair of positions
            x_dir = available_coords[0]
            y_dir = available_coords[1]

            #determine which 2 positions takes less move to eat the black piece
            best_dir, piece_1, piece_2 = self.choose_best_dir(x_dir, y_dir)
            # initialises A* Search Class
            a_star_algo = AStarSearch(board_width, board_length)
            # keeps copy of current pieces original location
            old_x, old_y = piece_1.x, piece_1.y

            # Does A* search
            new_location = a_star_algo.search(self.squares[best_dir[1] * \
                board_width + best_dir[0]], self.squares[piece_1.x * \
                board_width + piece_1.y], self.squares)
            # Updates board
            self.update_pieces(new_location, old_x, old_y)
            # keeps copy of current pieces original location
            old_x, old_y = piece_2.x, piece_2.y

            # Do another A* search
            new_location = a_star_algo.search(self.squares[best_dir[3] * \
                board_width + best_dir[2]], self.squares[piece_2.x * \
                board_width + piece_2.y], self.squares)
            #-------------------------------------------------------------------------------
            if new_location is None:
                self.squares[item.x * board_width + item.y].value = "-"
                continue

            #update the pieces after each set of moves
            self.update_pieces(new_location, old_x, old_y)
            # removes dead black piece

    def update_pieces(self, new_location, old_x, old_y):
        #the new location now is marked with "O"
        self.squares[new_location.x * board_width + new_location.y].value = "O"
        #iterate through all the white pieces
        for item in self.white_pieces:
            #if the piece's co-ord is the same as the old location, update it
            if item.x == old_x and item.y == old_y:
                item.x = new_location.x
                item.y = new_location.y
        #---------------------------------------------------------------------------------
        if old_x != new_location.x and old_x != new_location.x:
            self.squares[old_x * board_width + old_y].value = "-"

    # Check which of the two positions are available for taking the piece
    def check_takeable(self, bp):
        squares = self.squares
        available_coords = [[], []]

        # Check if takeable in x direction
        if 1 <= bp.x <= 6:
            # Check if both spaces in x direction free
            if squares[(bp.x-1) * board_width + bp.y].value == "-" and \
                    squares[(bp.x + 1) * board_width + bp.y].value == "-":
                available_coords[0] = [bp.y, bp.x - 1, bp.y, bp.x + 1]

            #Check if either space in x direction is free.
            elif squares[(bp.x-1) * board_width + bp.y].value == "O" and \
                    squares[(bp.x + 1) * board_width + bp.y].value == "-":
                available_coords[0] = [bp.y, bp.x - 1, bp.y, bp.x + 1]

            elif squares[(bp.x-1) * board_width + bp.y].value == "-" and \
                    squares[(bp.x + 1) * board_width + bp.y].value == "O":
                available_coords[0] = [bp.y, bp.x - 1, bp.y, bp.x + 1]

        # Check if takeable in y direction
        if 1 <= bp.y <= 6:
            # Check if both spaces in y direction free
            if squares[bp.x * board_width + (bp.y - 1)].value == "-" and \
                    squares[bp.x * board_width + (bp.y + 1)].value == "-":
                available_coords[1] = [bp.y - 1, bp.x, bp.y + 1, bp.x]

            # Check if eithr space in y direction is free
            elif squares[bp.x * board_width + (bp.y - 1)].value == "O" and \
                    squares[bp.x * board_width + (bp.y + 1)].value == "-":
                available_coords[1] = [bp.y - 1, bp.x, bp.y + 1, bp.x]

            elif squares[bp.x * board_width + (bp.y - 1)].value == "-" and \
                    squares[bp.x * board_width + (bp.y + 1)].value == "O":
                available_coords[1] = [bp.y - 1, bp.x, bp.y + 1, bp.x]

        return available_coords

    #given 2 pairs of squares, return the one with least movements.
    def choose_best_dir(self, x_dir, y_dir):

        #if neither are present.
        if not x_dir and not y_dir:
            return None

        #if x_dir is non-existant.
        elif not x_dir:
            piece3, piece4 = self.closest_piece(y_dir[1], y_dir[0])
            return y_dir, piece3, piece4

        #if y_dir is non-existant
        elif not y_dir:
            piece1, piece2 = self.closest_piece(x_dir[1], x_dir[0])
            return x_dir, piece1, piece2

        #---------------------------------------------------------------------------------
        piece1, piece2 = self.closest_piece(x_dir[1], x_dir[0])

        #calculate the distances of each piece to a destination
        x_dist_1 = AStarSearch.manhattan_distance(x_dir[1], piece1.x, 
            x_dir[0], piece1.y)
        x_dist_2 = AStarSearch.manhattan_distance(x_dir[3], piece2.x, 
            x_dir[2], piece2.y)

        #-----------------------------------------------------------------------------------
        piece3, piece4 = self.closest_piece(y_dir[1], y_dir[0])

        #calculate the distance of each piece to a destination
        y_dist_1 = AStarSearch.manhattan_distance(y_dir[1], piece3.x, 
            y_dir[0], piece3.y)
        y_dist_2 = AStarSearch.manhattan_distance(y_dir[3], piece4.x, 
            y_dir[2], piece4.y)

        #return the better value.
        if x_dist_1 + x_dist_2 <= y_dist_1 + y_dist_2:
            return x_dir, piece1, piece2

        else:
            return y_dir, piece3, piece4














