import random
import matplotlib.pyplot as plt
import numpy as np

TILE_EMPTY = 0
TILE_CRATE = 1


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
    maze = _create_grid_with_cells(maze_width, maze_height)

    w = (len(maze[0]) - 1) // 2  # Logical width of the maze (excluding walls)
    h = (len(maze) - 1) // 2    # Logical height of the maze (excluding walls)

    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x, y):
        """
        Recursively carve out passages between cells in the maze.

        Args:
            x (int): The current x-coordinate in logical grid space.
            y (int): The current y-coordinate in logical grid space.
        """
        vis[y][x] = 1
        directions = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(directions)
        for xx, yy in directions:
            if vis[yy][xx]:
                continue
            if xx == x:
                maze[max(y, yy) * 2][x * 2 + 1] = TILE_EMPTY
            if yy == y:
                maze[y * 2 + 1][max(x, xx) * 2] = TILE_EMPTY
            walk(xx, yy)

    walk(random.randrange(w), random.randrange(h))
    return maze


def dfs(maze, start, end):
    """
    Find a path from the start to the end in a maze using the Depth-First Search algorithm.

    Args:
        maze (list): A 2D list representing the maze.
        start (tuple): The starting position as (row, column).
        end (tuple): The ending position as (row, column).

    Returns:
        list: A list of coordinates representing the path, or None if no path exists.
    """
    rows, cols = len(maze), len(maze[0])
    stack = [(start, [start])]
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
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == TILE_EMPTY:
                neighbors.append((nx, ny))
        return neighbors

    while stack:
        current_pos, path = stack.pop()
        if current_pos == end:
            return path
        if current_pos not in visited:
            visited.add(current_pos)
            for neighbor in get_neighbors(current_pos):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None


def print_maze_with_path(maze, path):
    """
    Print the maze with a path highlighted.

    Args:
        maze (list): A 2D list representing the maze.
        path (list): A list of coordinates representing the path.

    Returns:
        None
    """
    maze_copy = [row[:] for row in maze]
    for x, y in path:
        maze_copy[x][y] = 2
    for row in maze_copy:
        print(" ".join(str(cell) for cell in row))


def draw_maze(maze, path=None):
    """
    Visualize the maze and an optional path using Matplotlib.

    Args:
        maze (list): A 2D list representing the maze.
        path (list, optional): A list of coordinates representing the path.

    Returns:
        None
    """
    rows, cols = len(maze), len(maze[0])
    maze_image = np.array(maze)

    fig, ax = plt.subplots()
    ax.imshow(maze_image, cmap='binary', origin='upper')

    if path:
        path_x, path_y = zip(*path)
        ax.plot(path_y, path_x, color='g', linewidth=0, marker='o', linestyle='')

    ax.set_xticks(np.arange(-.5, cols, 1))
    ax.set_yticks(np.arange(-.5, rows, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(color='gray', linestyle='-', linewidth=1)

    plt.show()


if __name__ == "__main__":
    MAZE_HEIGHT = 71
    MAZE_WIDTH = 71

    maze = make_maze_depth_first(MAZE_WIDTH, MAZE_HEIGHT)
    start = (1, 1)
    end = (MAZE_HEIGHT - 2, MAZE_WIDTH - 2)

    result = dfs(maze, start, end)

    if result:
        print("Path found:")
        print_maze_with_path(maze, result)
        draw_maze(maze, result)
    else:
        print("No path found.")
        draw_maze(maze)
