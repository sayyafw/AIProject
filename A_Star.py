import heapq
from math import fabs
import copy
from Square import Square

board_width = 8
board_length = 8

class AStarSearch:

    def __init__(self, squares, board_width, board_length):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = []
        self.squares = squares

    @staticmethod
    def manhattan_distance(x1, y1, x2, y2):
        dist_x = fabs(x1 - x2)
        dist_y = fabs(y1 - y2)
        return dist_x + dist_y

    def get_square(self, x, y):
        return self.squares[x * board_width + y]

    # Gives a list of squares adjacent to current
    def get_adjacent_squares(self, square):

        list_of_squares = []

        if square.x > 0:
            list_of_squares.append(self.get_square(square.x - 1, square.y))

        if square.y > 0:
            list_of_squares.append(self.get_square(square.x, square.y - 1))

        if square.x < board_width - 1:
            list_of_squares.append(self.get_square(square.x + 1, square.y))

        if square.y < board_length - 1 :
            list_of_squares.append(self.get_square(square.x, square.y + 1))

        return list_of_squares

    # Prints the path
    def print_moves(self, square, start_goal):

        current_square = square
        path = []

        while current_square.x != start_goal.x or current_square.y != start_goal.y:
            coods = (current_square.x, current_square.y)
            parent_square = current_square.parent
            parent_coods = (parent_square.x, parent_square.y)
            current_square = current_square.parent
            path.append(str(parent_coods) + " -> " + str(coods))
            #print(str(coods) + " " + str(parent_coods))

        i = len(path) - 1

        while i >= 0:
            print(path[i])
            i -= 1

    # Updates position when move is to an adjacent element
    def update_position_adjacent(self, current_square, adjacent_square, goal_square):

        adjacent_square.g = current_square.g + 1
        adjacent_square.h = self.manhattan_distance(adjacent_square.x, adjacent_square.y, goal_square.x, goal_square.y)
        adjacent_square.f = adjacent_square.h + adjacent_square.g
        adjacent_square.parent = current_square

    # Updates position when move is a jump
    def update_position_jump(self, current_square, jump_square, goal_square):

        jump_square.g = current_square.g + 2
        jump_square.h = self.manhattan_distance(jump_square.x, jump_square.y, goal_square.x, goal_square.y)
        jump_square.f = jump_square.h + jump_square.g
        jump_square.parent = current_square


    #Performs the actual A* Search
    def search(self, goal_square, current_square):

        end_square = None
        # Pushes the heap for the first element
        heapq.heappush(self.opened, (current_square.f, current_square))

        # keeps a copy of the start square
        start_square = copy.copy(current_square)

        while len(self.opened):

            # Get first element from heap
            f, square = heapq.heappop(self.opened)
            # Show that this element has been visited
            self.closed.append(square)

            # Check for goal state
            if self.state(square, goal_square):
                self.print_moves(square, start_square)
                self.update_board(self.squares, square, start_square)
                end_square = square
                break

            # Gets list of adjacent squares to current
            adjacent_squares = self.get_adjacent_squares(square)

            # Checks each of the adjacent squares for the best move
            for i in range(len(adjacent_squares)):
                item = adjacent_squares[i]
                if not self.blocked(item, self.squares) and item not in self.closed:
                    if (item.f, item) in self.opened:

                        # If adj cell is open, check if current
                        # path is better than
                        # previously recorded path for this cell
                        if item.g > square.g + 1:
                            self.update_position_adjacent(square, item,  goal_square)

                    else:
                        self.update_position_adjacent(square, item, goal_square)
                        heapq.heappush(self.opened, (item.f, item))
        return self.squares, end_square

    # Check if current square is blocked

    def update_board(self, squares, end_square, start_square):

        self.squares[end_square.x * board_width + end_square.y].set_value("O")
        self.squares[start_square.x * board_width + start_square.y].set_value("-")


    @staticmethod
    def blocked(square, board):

        if square.value!= "-":

            return True
        return False

    # Check for goal state
    @staticmethod
    def state(current_square, goal_square):

        if current_square.x == goal_square.x and \
                current_square.y == goal_square.y:
            return True

        return False

    # Check if jump is possible
    @staticmethod
    def check_jump(square, board, direction):

        if (square.x > 6 or square.x < 1) and (square.y > 6 or square.y < 1):
            return False

        if direction == 0:
            if square.x > 0 and board[square.y][square.x - 1] == "-":
                return True

        if direction == 1:
            if square.y > 0 and board[square.y - 1][square.x] == "-":
                print(True)
                return True

        if direction == 2:
            if square.x < 7 and board[square.y][square.x + 1] == "-":
                return True

        if direction == 3:
            if square.y < 7 and board[square.y + 1][square.x] == "-":
                return True
        return False

