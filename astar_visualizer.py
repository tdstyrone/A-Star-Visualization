import pygame
from spotnode import SpotNode
import colors
from queue import PriorityQueue

""" 

Sets up the display window
Dimensions(WIDTH and HEIGHT) of window can be adjusted here
Number of Rows on grid can be adjusted here (ROWS)
"""

ROWS = 50
WIDTH = 800
HEIGHT = 800
WIN_SIZE = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Algorithm Visualizer")


def heuristic(point_1, point_2):
    """Calculates the manhattan distance between points and returns an integer"""

    x1, y1 = point_1
    x2, y2 = point_2
    man_dist = abs(x1 - x2) + abs(y1 - y2)
    return man_dist


def construct_path(parent_node, current, draw_board):
    """Draws path by retracing previously visited nodes"""

    while current in parent_node:
        current = parent_node[current]
        current.make_path()
        draw_board()


def astar_algorithm(draw_board, grid, start, end):
    """Implements the A* Algorithm and returns an boolean"""

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    parent_node = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_position(), end.get_position())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            construct_path(parent_node, end, draw_board)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                parent_node[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw_board()

        if current != start:
            current.make_closed()
    return False


def generate_grid(rows, width):
    """Creates squares to form grid and returns an SpotNode array"""

    grid = []
    spot_width = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = SpotNode(i, j, spot_width, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win_size, rows, width):
    """Draws the lines to form graph"""

    spot_width = width // rows

    for i in range(rows):
        pygame.draw.line(win_size, colors.GREY, (0, i * spot_width), (width, i * spot_width))
        pygame.draw.line(win_size, colors.GREY, (i * spot_width, 0), (i * spot_width, width))


def draw(win_size, grid, rows, width):
    """Draws the entire grid and fills each square white"""
    win_size.fill(colors.WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win_size)

    draw_grid(win_size, rows, width)
    pygame.display.update()


def get_pos_clicked(pos, rows, width):
    """Calculates the row and column value of point on screen clicked and returns a Integer tuple"""

    spot_width = width // rows
    y, x = pos

    row = y // spot_width
    col = x // spot_width

    return row, col


def main(win_size, width, rows):
    """Runs the entire program"""

    grid = generate_grid(rows, width)

    start = None
    end = None

    run = True
    while run:
        draw(win_size, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left-Click
                pos = pygame.mouse.get_pos()
                row, col = get_pos_clicked(pos, rows, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_wall()

            elif pygame.mouse.get_pressed()[2]:  # Right-CLick
                pos = pygame.mouse.get_pos()
                row, col = get_pos_clicked(pos, rows, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    astar_algorithm(lambda: draw(win_size, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = generate_grid(rows, width)
    pygame.quit()


if __name__ == "__main__":
    main(WIN_SIZE, WIDTH, ROWS)
