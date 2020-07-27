import pygame
from spotnode import SpotNode
import colors
import math
from queue import PriorityQueue

WIDTH = 800
WIN_SIZE = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm Visualizer")


def heuristic(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    man_dist = abs(x1 - x2) + abs(y1-y2)
    return man_dist

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
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
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False


def generate_grid(rows, width):
    grid = []
    spot_width = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = SpotNode(i, j, spot_width, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win_size, rows, width):
    spot_width = width // rows
    
    for i in range(rows):
        pygame.draw.line(win_size, colors.GREY, (0, i * spot_width), (width, i * spot_width))
        for j in range(rows):
            pygame.draw.line(win_size, colors.GREY, (j * spot_width, 0), (j * spot_width, width))


def draw(win_size, grid, rows, width):
    win_size.fill(colors.WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win_size)
    
    draw_grid(win_size, rows, width)
    pygame.display.update()


def get_pos_clicked(pos, rows, width):
    spot_width = width // rows
    y, x = pos

    row = y // spot_width
    col = x // spot_width
    
    return row, col


def main(win_size, width):
    ROWS = 50
    grid = generate_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win_size, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_pos_clicked(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_wall()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_pos_clicked(pos, ROWS, width)
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
                    algorithm(lambda: draw(win_size, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = generate_grid(ROWS, width)

    pygame.quit()

main(WIN_SIZE, WIDTH)
