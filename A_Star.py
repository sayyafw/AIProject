import heapq
from math import fabs
import copy


class A_Star:

    def __init__(self, squares, board_width, board_length):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = []
        self.squares = squares
        self.board_width = board_width
        self.board_length = board_length

    @staticmethod
    def manhattan_distance(x1, y1, x2, y2):
        dist_x = fabs(x1 - x2)
        dist_y = fabs(y1 - y2)
        return dist_x + dist_y


    def get_square(self, x, y):
        return self.squares[x * self.board_width + y]

    def get_adjacent_squares(self, square):

        list_of_squares = []

        if square.x > 0:
            list_of_squares.append(self.get_square(square.x - 1, square.y))

        if square.y > 0:
            list_of_squares.append(self.get_square(square.x, square.y - 1))

        if square.x < self.board_width - 1:
            list_of_squares.append(self.get_square(square.x + 1, square.y))

        if square.y < self.board_length - 1 :
            list_of_squares.append(self.get_square(square.x, square.y + 1))

        return list_of_squares


    def print_moves(self, square, start_goal):

        current_square = square
        print((current_square.x, start_goal.x))
        while current_square.x != start_goal.x or current_square.y != start_goal.y:
            coods = (current_square.x, current_square.y)
            parent_square = current_square.parent
            parent_coods = (parent_square.x, parent_square.y)
            print(str(parent_coods))
            print(" -> ")
            print(str(coods))
            current_square = current_square.parent

    def update_position_adjacent(self, current_square, adjacent_square, goal_square):

        adjacent_square.g = current_square.g + 1
        adjacent_square.h = self.manhattan_distance(adjacent_square.x, adjacent_square.y, goal_square.x, goal_square.y)
        adjacent_square.f = adjacent_square.h + adjacent_square.g
        adjacent_square.parent = current_square

    def update_position_jump(self, current_square, jump_square, goal_square):

        jump_square.g = current_square.g + 2
        jump_square.h = self.manhattan_distance(jump_square.x, jump_square.y, goal_square.x, goal_square.y)
        jump_square.f = jump_square.h + jump_square.g
        jump_square.parent = current_square

    def search(self, goal_square, board, current_square):
        heapq.heappush(self.opened, (current_square.f, current_square))
        start_square = copy.copy(current_square)
        while len(self.opened):
            f, square = heapq.heappop(self.opened)
            self.closed.append(square)

            if self.state(square, goal_square):
                self.print_moves(square, start_square)

            adjacent_squares = self.get_adjacent_squares(square)

            for item in adjacent_squares:
                if item is not self.blocked(item, board) and item not in self.closed:
                    if (item.f, item) in self.opened:

                        if item.g > square.g + 1:
                            self.update_position_adjacent(square, item,  goal_square)

                    else:
                        self.update_position_adjacent(square, item, goal_square)
                        heapq.heappush(self.opened, (item.f, item))


    def blocked(self, square, board):

        if board[square.y][square.x] != "-":
            return True

    def state(self, current_square, goal_square):

        if current_square.x == goal_square.x and \
                current_square.y == goal_square.y:
            print("HELLO " + str((goal_square.x, goal_square.y, current_square.x, current_square.y)))
            return True

        return False



