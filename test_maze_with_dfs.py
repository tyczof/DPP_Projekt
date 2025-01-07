from tgis_projekt import _create_grid_with_cells, make_maze_depth_first, dfs


def test_create_grid_with_cells():
    """
    Test the creation of a grid with walls and empty cells.

    Verifies that:
    - The grid has the specified dimensions.
    - Odd positions contain empty cells (0).
    - Border positions contain walls (1).
    """
    width, height = 5, 5
    grid = _create_grid_with_cells(width, height)
    assert len(grid) == height
    assert all(len(row) == width for row in grid)
    assert grid[1][1] == 0  # Odd position should be empty
    assert grid[0][0] == 1  # Corner position should be a wall


def test_make_maze_depth_first():
    """
    Test the maze generation using the Depth-First Search algorithm.

    Verifies that:
    - The generated maze has the correct dimensions.
    - The maze contains both empty paths (0) and walls (1).
    """
    maze = make_maze_depth_first(5, 5)
    assert len(maze) == 5
    assert all(len(row) == 5 for row in maze)
    assert any(0 in row for row in maze)  # Ensure at least one empty cell
    assert any(1 in row for row in maze)  # Ensure walls exist


def test_dfs():
    """
    Test the DFS algorithm on a simple maze.

    Verifies that:
    - The algorithm finds a valid path from the start to the target.
    - The path matches the expected solution.
    """
    maze = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    start = (0, 0)
    end = (2, 2)
    path = dfs(maze, start, end)
    expected_path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    assert path == expected_path


def test_dfs_no_path():
    """
    Test the DFS algorithm when no path exists.

    Verifies that:
    - The algorithm correctly identifies there is no solution.
    - The returned value is None.
    """
    maze = [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    start = (0, 0)
    end = (1, 2)
    path = dfs(maze, start, end)
    assert path is None
