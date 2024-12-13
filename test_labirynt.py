import pytest
from tgis_projekt import _create_grid_with_cells, make_maze_depth_first, dfs

def test_create_grid_with_cells():
    width, height = 5, 5
    grid = _create_grid_with_cells(width, height)
    assert len(grid) == height
    assert all(len(row) == width for row in grid)
    assert grid[1][1] == 0  # Wolne pole
    assert grid[0][0] == 1  # Ściana

def test_make_maze_depth_first():
    maze = make_maze_depth_first(5, 5)
    assert len(maze) == 5
    assert all(len(row) == 5 for row in maze)
    assert any(0 in row for row in maze)  # Wolne pola istnieją
    assert any(1 in row for row in maze)  # Ściany istnieją

def test_dfs():
    maze = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    start = (0, 0)
    end = (2, 2)
    path = dfs(maze, start, end)
    assert path == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]

def test_dfs_no_path():
    maze = [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    start = (0, 0)
    end = (1, 2)
    path = dfs(maze, start, end)
    assert path is None
