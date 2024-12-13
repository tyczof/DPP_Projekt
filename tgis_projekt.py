import random
import matplotlib.pyplot as plt
import numpy as np

TILE_EMPTY = 0
TILE_CRATE = 1


def _create_grid_with_cells(width, height):
    """ Create a grid with empty cells on odd row/column combinations. """
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            # Empty cells at odd row/column positions
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(TILE_EMPTY)
            # Walls at the borders
            elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
                grid[row].append(TILE_CRATE)
            # Walls everywhere else
            else:
                grid[row].append(TILE_CRATE)
    return grid


def make_maze_depth_first(maze_width, maze_height):
    """ Generate a maze using the Depth-First Search algorithm. """
    maze = _create_grid_with_cells(maze_width, maze_height)

    w = (len(maze[0]) - 1) // 2  # Width of logical cells
    h = (len(maze) - 1) // 2    # Height of logical cells

    # Visited tracker for logical cells
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x: int, y: int):
        """ Recursively carve out passages in the maze. """
        vis[y][x] = 1  # Mark current cell as visited

        # Generate shuffled list of directions (up, down, left, right)
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            # Remove walls between current cell and next cell
            if xx == x:
                maze[max(y, yy) * 2][x * 2 + 1] = TILE_EMPTY
            if yy == y:
                maze[y * 2 + 1][max(x, xx) * 2] = TILE_EMPTY

            walk(xx, yy)

    # Start carving from a random cell
    walk(random.randrange(w), random.randrange(h))

    return maze


def dfs(maze, start, end):
    """ Find a path in the maze using Depth-First Search. """
    rows, cols = len(maze), len(maze[0])
    stack = [(start, [start])]  # Stack for DFS: (current position, path)
    visited = set()

    def get_neighbors(pos):
        """ Get valid neighboring cells. """
        x, y = pos
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                neighbors.append((nx, ny))
        return neighbors

    while stack:
        (current_pos, path) = stack.pop()

        if current_pos == end:
            return path  # Path found

        if current_pos not in visited:
            visited.add(current_pos)
            for neighbor in get_neighbors(current_pos):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return None  # No path found


def print_maze_with_path(maze, path):
    """ Print the maze with the path highlighted. """
    maze_copy = [row[:] for row in maze]
    for x, y in path:
        maze_copy[x][y] = 2  # Mark the path with a distinct value
    for row in maze_copy:
        print(" ".join(str(cell) for cell in row))


def draw_maze(maze, path=None):
    """ Visualize the maze with the path drawn in multiple colors. """
    rows, cols = len(maze), len(maze[0])

    # Create a binary maze image for visualization
    maze_image = np.array(maze)

    fig, ax = plt.subplots()
    ax.imshow(maze_image, cmap='binary', origin='upper')

    if path:
        # Draw path
        path_x, path_y = zip(*path)
        ax.plot(path_y, path_x, color='g', linewidth=0, marker='o', linestyle='')

    # Add gridlines to visualize the maze structure
    ax.set_xticks(np.arange(-.5, cols, 1))
    ax.set_yticks(np.arange(-.5, rows, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(color='gray', linestyle='-', linewidth=1)

    plt.show()


if __name__ == "__main__":
    # Maze must have an ODD number of rows and columns.
    # Walls go on EVEN rows/columns.
    # Openings go on ODD rows/columns
    MAZE_HEIGHT = 71
    MAZE_WIDTH = 71

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

    # Define start and end points for pathfinding
    start = (1, 1)  # Start in top left corner
    end = (len(maze[0]) - 2, len(maze) - 2)  # End in bottom right corner

    result = dfs(maze, start, end)

    if result:
        print(f"Path found: {result}")
    else:
        print("No path found.")

    if result:
        print_maze_with_path(maze, result)
        draw_maze(maze, result)
