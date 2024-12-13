# -*- coding: utf-8 -*-
"""TGIS_Projekt

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Gfr4_Il1jC1ymErzzeMz6j158YQv7lXk
"""

pip install arcade

# https://api.arcade.academy/en/latest/examples/maze_depth_first.html#maze-depth-first
# pip install arcade

import random
import arcade
import timeit
import os

NATIVE_SPRITE_SIZE = 128
SPRITE_SCALING = 0.25
SPRITE_SIZE = int(NATIVE_SPRITE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Maze Depth First Example"

MOVEMENT_SPEED = 8

TILE_EMPTY = 0
TILE_CRATE = 1

# Maze must have an ODD number of rows and columns.
# Walls go on EVEN rows/columns.
# Openings go on ODD rows/columns
MAZE_HEIGHT = 71
MAZE_WIDTH = 71

MERGE_SPRITES = True

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200


def _create_grid_with_cells(width, height):
    """ Create a grid with empty cells on odd row/column combinations. """
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(TILE_EMPTY)
            elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
                grid[row].append(TILE_CRATE)
            else:
                grid[row].append(TILE_CRATE)
    return grid


def make_maze_depth_first(maze_width, maze_height):
    maze = _create_grid_with_cells(maze_width, maze_height)

    w = (len(maze[0]) - 1) // 2
    h = (len(maze) - 1) // 2
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x: int, y: int):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                maze[max(y, yy) * 2][x * 2 + 1] = TILE_EMPTY
            if yy == y:
                maze[y * 2 + 1][max(x, xx) * 2] = TILE_EMPTY

            walk(xx, yy)

    walk(random.randrange(w), random.randrange(h))

    return maze

maze = make_maze_depth_first(MAZE_WIDTH, MAZE_HEIGHT)

# Labirynt - 1 to ściana, 0 to przechodnia ścieżka
# maze = [
#     [0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 0],
#     [0, 0, 0, 1, 0],
#     [0, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0]
# ]

# maze = [
#     [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
#     [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
#     [0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]

# maze = [
#     [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
#     [0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
#     [1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]

start = (1, 1)  # Start w lewym górnym rogu
end = (69, 69)    # Meta w prawym dolnym rogu

def dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    stack = [(start, [start])]  # Stos przechowujący aktualną pozycję i ścieżkę
    visited = set()  # Zbiór odwiedzonych węzłów

    def get_neighbors(pos):
        x, y = pos
        neighbors = []
        # Przemieszczenie w czterech kierunkach (góra, dół, lewo, prawo)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                neighbors.append((nx, ny))
        return neighbors

    while stack:
        (current_pos, path) = stack.pop()

        if current_pos == end:
            return path  # Znaleziono ścieżkę

        if current_pos not in visited:
            visited.add(current_pos)
            for neighbor in get_neighbors(current_pos):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return None  # Brak ścieżki

result = dfs(maze, start, end)

if result:
    print(f"Znaleziono ścieżkę: {result}")
else:
    print("Brak dostępnej ścieżki")

def print_maze_with_path(maze, path):
    maze_copy = [row[:] for row in maze]
    for x, y in path:
        maze_copy[x][y] = 2
    for row in maze_copy:
        print(" ".join(str(cell) for cell in row))

if result:
    print_maze_with_path(maze, result)

import matplotlib.pyplot as plt
import numpy as np
import itertools

# Funkcja do rysowania labiryntu z Matplotlib
def draw_maze(maze, path=None):
    rows, cols = len(maze), len(maze[0])

    # Utwórz obrazek z labiryntem (wartości 1 to czarne komórki, 0 to białe)
    maze_image = np.array(maze)

    # Rysowanie labiryntu
    fig, ax = plt.subplots()
    ax.imshow(maze_image, cmap='binary', origin='upper')

    colors = itertools.cycle(('g', 'r', 'b', 'c', 'k'))

    # Rysowanie ścieżki na czerwono (o ile istnieje)
    if path:
        path_x, path_y = zip(*path)
        ax.plot(path_y, path_x, color=next(colors), linewidth=0, marker='o', linestyle='')

    # Dodanie linii siatki dla lepszej widoczności komórek
    ax.set_xticks(np.arange(-.5, cols, 1))
    ax.set_yticks(np.arange(-.5, rows, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(color='gray', linestyle='-', linewidth=1)

    plt.show()

# Rysowanie labiryntu i ścieżki
draw_maze(maze, result)

def dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    stack = [(start, [start])]  # Stos przechowujący aktualną pozycję i ścieżkę
    visited = set()  # Zbiór odwiedzonych węzłów

    def get_neighbors(pos):
        x, y = pos
        neighbors = []
        # Przemieszczenie w czterech kierunkach (góra, dół, lewo, prawo)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                neighbors.append((nx, ny))
        return neighbors

    while stack:
        (current_pos, path) = stack.pop()

        if current_pos == end:
            return path  # Znaleziono ścieżkę

        if current_pos not in visited:
            visited.add(current_pos)
            for neighbor in get_neighbors(current_pos):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return None  # Brak ścieżki