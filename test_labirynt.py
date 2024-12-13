import pytest
from tgis_projekt import _create_grid_with_cells, make_maze_depth_first, dfs

# Test to verify the creation of a grid with the specified dimensions and structure
def test_create_grid_with_cells():
    width, height = 5, 5
    grid = _create_grid_with_cells(width, height)
    # Ensure the grid has the correct dimensions
    assert len(grid) == height
    assert all(len(row) == width for row in grid)
    # Verify that a cell at an odd position is empty
    assert grid[1][1] == 0
    # Verify that a corner cell is a wall
    assert grid[0][0] == 1

# Test to check the maze generation using the depth-first algorithm
def test_make_maze_depth_first():
    maze = make_maze_depth_first(5, 5)
    # Ensure the maze dimensions are as expected
    assert len(maze) == 5
    assert all(len(row) == 5 for row in maze)
    # Verify that the maze contains both empty cells and walls
    assert any(0 in row for row in maze)  # At least one empty cell
    assert any(1 in row for row in maze)  # At least one wall

# Test to ensure the DFS algorithm finds a valid path in a simple maze
def test_dfs():
    maze = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    start = (0, 0)  # Starting point of the maze
    end = (2, 2)    # Target point of the maze
    path = dfs(maze, start, end)
    # Verify that the path found matches the expected result
    assert path == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]

# Test to confirm DFS handles cases where no path exists
def test_dfs_no_path():
    maze = [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    start = (0, 0)  # Starting point
    end = (1, 2)    # Target point with no path
    path = dfs(maze, start, end)
    # Ensure the returned path is None, indicating no solution
    assert path is None
