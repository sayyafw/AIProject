import heapq
from math import fabs
import copy

class AStarSearch:

    def __init__(self, board_width, board_length):
        self.board_width = board_width
        self.board_length = board_length

    #calculate the manhattan distance between 2 co-ords
    @staticmethod
    def manhattan_distance(x1, y1, x2, y2):
        dist_x = fabs(x1 - x2)
        dist_y = fabs(y1 - y2)
        return dist_x + dist_y

    #get the targetted square object
    def get_square(self, x, y, squares):
        return squares[x * self.board_width + y]

    # Gives a list of squares adjacent to current
    def get_adjacent_squares(self, square, squares):

        list_of_squares = []

        #if the square is not on the edge
        if square.x > 0:
            #get the square on the left of this square
            adj_left = self.get_square(square.x - 1, square.y, squares)
            #if the square on the left isn't blocked, take it.
            if not self.blocked(adj_left, squares):
                list_of_squares.append(adj_left)
            #elsewise, check if it can be jumped over
            elif 1 < square.x < 6 and not self.blocked(self.get_square\
                (square.x - 2, square.y, squares), squares):
                #it can be jumped over, take this square
                list_of_squares.append(self.get_square(square.x - 2, square.y, 
                    squares))

        #repetiton of the above, but for the up side.
        if square.y > 0:
            adj_up = self.get_square(square.x, square.y - 1, squares)
            if not self.blocked(adj_up, squares):
                list_of_squares.append(adj_up)

            elif 1 < square.y < 6 and not self.blocked(self.get_square(square.x,
             square.y - 2, squares), squares):
                list_of_squares.append(self.get_square(square.x, square.y - 2, 
                    squares))

        #repetition of the above, but for the rigt side.
        if square.x < self.board_width - 1:
            adj_right = self.get_square(square.x + 1, square.y, squares)
            if not self.blocked(adj_right, squares):
                list_of_squares.append(adj_right)

            elif 1 < square.x < 6 and not self.blocked(self.get_square \
                (square.x + 2, square.y, squares), squares):
                list_of_squares.append(self.get_square(square.x + 2, square.y, 
                    squares))

        #repitition of the above, but for the down side.
        if square.y < self.board_width - 1:
            adj_down = self.get_square(square.x, square.y + 1, squares)
            if not self.blocked(adj_down, squares):
                list_of_squares.append(adj_down)

            elif 1 < square.x < 6 and not self.blocked(self.get_square\
                (square.x, square.y + 2, squares),squares):
                list_of_squares.append(self.get_square(square.x, square.y + 2,
                 squares))

        return list_of_squares

    # Prints the path
    def print_moves(self, square, start_goal):

        current_square = square
        path = []

        #while there are path to be print
        while current_square.x != start_goal.x or \
        current_square.y != start_goal.y:
            #get both co-ords, and print from parent node to child.
            coords = (current_square.x, current_square.y)
            parent_square = current_square.parent
            parent_coords = (parent_square.x, parent_square.y)
            current_square = current_square.parent
            #append the path to an array 
            path.append(str(parent_coords) + " -> " + str(coords))

        i = len(path) - 1

        #now print it out in reverse order.
        while i >= 0:
            print(path[i])
            i -= 1

    # Updates position when move is to an adjacent element
    def update_position_adjacent(self, current_square, \
        adjacent_square, goal_square):

        #-------------------------------------------------------------------------------
        adjacent_square.g = current_square.g + 1
        adjacent_square.h = self.manhattan_distance(adjacent_square.x, 
            adjacent_square.y, goal_square.x, goal_square.y)
        adjacent_square.f = adjacent_square.h + adjacent_square.g
        adjacent_square.parent = current_square

    #Performs the actual A* Search
    def search(self, goal_square, current_square, squares):

        unvisited = []
        visited = []

        end_square = None
        # Pushes the heap for the first element
        heapq.heappush(unvisited, (current_square.f, current_square))

        # keeps a copy of the start square
        start_square = copy.copy(current_square)

        #while there are unvisited nodes.
        while len(unvisited):
            # Get first element from heap
            f, square = heapq.heappop(unvisited)
            # Show that this element has been visited
            visited.append(square)

            # Check if we're already at the goal
            if self.state(square, goal_square):
                end_square = square
                self.print_moves(square, start_square)
                break

            # Gets list of adjacent squares to current
            adjacent_squares = self.get_adjacent_squares(square, squares)

            # Checks each of the adjacent squares for the best move
            for i in range(len(adjacent_squares)):
                #for each of the adjacent tiles
                item = adjacent_squares[i]
                #if tile is not visited and not blocked
                if item not in visited and  not self.blocked(item, squares):
                    #if ---------------------------------------------------------------
                    if (item.f, item) in unvisited:
                        #check if current path is better than the previous one
                        if item.g < square.g + 1:
                            self.update_position_adjacent(square, item, 
                                goal_square)
                    else:
                        #update the adjacent positions
                        self.update_position_adjacent(square, item, goal_square)
                        #------------------------------------------------------------
                        heapq.heappush(unvisited, (item.f, item))

        return end_square

    #check if given tile is blocked
    def blocked(self, square, squares):
        #if the tile is not empty, it's blocked
        if squares[square.x * self.board_width + square.y].value != "-":
            return True
        return False

    #Check if the 2 squares are the same
    @staticmethod
    def state(current_square, goal_square):
        #if they're the same, return true
        if current_square.x == goal_square.x and \
                current_square.y == goal_square.y:
            return True

        return False

    # Check if jump is possible
    @staticmethod
    def check_jump(square, board, direction):

        #check for edges
        if (square.x > 6 or square.x < 1) and (square.y > 6 or square.y < 1):
            return False

        #check for every direction, True if  ---------------------------------------------
        if direction == 0:
            if square.x > 0 and board[square.y][square.x - 1] == "-":
                return True
        if direction == 1:
            if square.y > 0 and board[square.y - 1][square.x] == "-":
                return True
        if direction == 2:
            if square.x < 7 and board[square.y][square.x + 1] == "-":
                return True
        if direction == 3:
            if square.y < 7 and board[square.y + 1][square.x] == "-":
                return True
        return False

