import pygame
import colors

class SpotNode:
    def __init__(self, row, col, width, total_rows):
        self.neighbors = []
        self.row = row
        self.col = col
        self.x_value = row * width
        self.y_value = col * width
        self.color = colors.WHITE
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == colors.TURQUOISE

    def is_open(self):
        return self.color == colors.DARK_BLUE

    def is_wall(self):
        return self.color == colors.BLACK

    def is_start(self):
        return self.color == colors.YELLOW

    def is_end(self):
        return self.color == colors.RED

    def reset(self):
        self.color = colors.WHITE
        return self.color

    def make_closed(self):
        self.color = colors.TURQUOISE

    def make_open(self):
        self.color = colors.DARK_BLUE

    def make_wall(self):
        self.color = colors.BLACK

    def make_start(self):
        self.color = colors.YELLOW

    def make_end(self):
        self.color = colors.RED

    def make_path(self):
        self.color = colors.PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x_value, self.y_value, self.width, self.width))

    def update_neighbors(self, grid):

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False
