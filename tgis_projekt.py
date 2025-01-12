"""
Maze generation and Depth-First Search (DFS) implementation.

This module includes:
- A function to generate a grid structure for the maze with walls and empty cells.
- A maze generator using the Depth-First Search algorithm.
- A pathfinding algorithm using DFS.
- Visualization tools for the maze and its paths.
"""

import random
import matplotlib.pyplot as plt
import numpy as np
from flagsmith import Flagsmith

TILE_EMPTY = 0
TILE_CRATE = 1

# Initialize Flagsmith client
flagsmith = Flagsmith(environment_key="ABzTK3EXG73CPLX7yFTTfg")

# Fetch feature flags from Flagsmith
flags = flagsmith.get_environment_flags()

# Feature flags with defaults
enable_draw_maze = flags.is_feature_enabled("enable_draw_maze")
enable_print_path = flags.is_feature_enabled("enable_print_path")

def _create_grid_with_cells(width, height):
    """
    Create a grid structure for the maze with walls and empty cells.

    Walls (1) are placed at even rows and columns, and empty cells (0)
    are placed at odd rows and columns.

    Args:
        width (int): The width of the grid.
        height (int): The height of the grid.

    Returns:
        list: A 2D list representing the grid with walls and empty cells.
    """
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
    """
    Generate a maze using the Depth-First Search (DFS) algorithm.

    The maze is built by carving paths between cells recursively, starting
    from a random cell.

    Args:
        maze_width (int): The width of the maze (must be odd).
        maze_height (int): The height of the maze (must be odd).

    Returns:
        list: A 2D list representing the generated maze with walls (1) and paths (0).
    """
    local_maze = _create_grid_with_cells(maze_width, maze_height)
    logical_width = (len(local_maze[0]) - 1) // 2
    logical_height = (len(local_maze) - 1) // 2
    visited = (
        [[0] * logical_width + [1] for _ in range(logical_height)]
        + [[1] * (logical_width + 1)]
    )

    def walk(x, y):
        """
        Recursively carve out passages between cells in the maze.

        Args:
            x (int): The current x-coordinate in logical grid space.
            y (int): The current y-coordinate in logical grid space.
        """
        visited[y][x] = 1
        directions = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(directions)
        for xx, yy in directions:
            if visited[yy][xx]:
                continue
            if xx == x:
                local_maze[max(y, yy) * 2][x * 2 + 1] = TILE_EMPTY
            if yy == y:
                local_maze[y * 2 + 1][max(x, xx) * 2] = TILE_EMPTY
            walk(xx, yy)

    walk(random.randrange(logical_width), random.randrange(logical_height))
    return local_maze

def dfs(maze_data, start_point, end_point):
    """
    Find a path from the start to the end in a maze using the Depth-First Search algorithm.

    Args:
        maze_data (list): A 2D list representing the maze.
        start_point (tuple): The starting position as (row, column).
        end_point (tuple): The ending position as (row, column).

    Returns:
        list: A list of coordinates representing the path, or None if no path exists.
    """
    rows, cols = len(maze_data), len(maze_data[0])
    stack = [(start_point, [start_point])]
    visited = set()

    def get_neighbors(pos):
        """
        Get valid neighbors for the current position in the maze.

        Args:
            pos (tuple): The current position as (row, column).

        Returns:
            list: A list of valid neighboring positions.
        """
        x, y = pos
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze_data[nx][ny] == TILE_EMPTY:
                neighbors.append((nx, ny))
        return neighbors

    while stack:
        current_pos, path = stack.pop()
        if current_pos == end_point:
            return path
        if current_pos not in visited:
            visited.add(current_pos)
            for neighbor in get_neighbors(current_pos):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None

def print_maze_with_path(maze_data, path):
    """
    Print the maze with a path highlighted.

    Args:
        maze_data (list): A 2D list representing the maze.
        path (list): A list of coordinates representing the path.
    """
    if enable_print_path:
        maze_copy = [row[:] for row in maze_data]
        for x, y in path:
            maze_copy[x][y] = 2
        for row in maze_copy:
            print(" ".join(str(cell) for cell in row))
    else:
        print("Path printing is disabled by feature flag.")

def draw_maze(maze_data, path=None):
    """
    Visualize the maze and an optional path using Matplotlib.

    Args:
        maze_data (list): A 2D list representing the maze.
        path (list, optional): A list of coordinates representing the path.
    """
    if enable_draw_maze:
        rows, cols = len(maze_data), len(maze_data[0])
        maze_image = np.array(maze_data)
        _, ax = plt.subplots()
        ax.imshow(maze_image, cmap='binary', origin='upper')

        if path:
            path_x, path_y = zip(*path)
            ax.plot(path_y, path_x, color='g', linewidth=2, marker='o', linestyle='')

        ax.set_xticks(np.arange(-.5, cols, 1))
        ax.set_yticks(np.arange(-.5, rows, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(color='gray', linestyle='-', linewidth=1)

        plt.show()
    else:
        print("Maze drawing is disabled by feature flag.")

if __name__ == "__main__":
    MAZE_HEIGHT = 71
    MAZE_WIDTH = 71

    maze_result = make_maze_depth_first(MAZE_WIDTH, MAZE_HEIGHT)
    start_pos = (1, 1)
    end_pos = (MAZE_HEIGHT - 2, MAZE_WIDTH - 2)

    result_path = dfs(maze_result, start_pos, end_pos)

    if result_path:
        print("Path found:")
        print_maze_with_path(maze_result, result_path)
        draw_maze(maze_result, result_path)
    else:
        print("No path found.")
        draw_maze(maze_result)
