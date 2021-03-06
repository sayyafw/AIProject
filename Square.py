class Square:

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.parent = None
        self.f = 0
        self.g = 0
        self.h = 0

    def __lt__(self, other):  # comparison method for priority queue
        return self.f > other.f

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_value(self, value):
        self.value = value

