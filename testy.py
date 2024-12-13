import unittest
from tgis_projekt import make_maze_depth_first, dfs, print_maze_with_path

class TestMazeFunctions(unittest.TestCase):

    def test_maze_generation(self):
        """Testuje, czy labirynt jest poprawnie generowany."""
        width, height = 11, 11  # Rozmiary muszą być nieparzyste
        maze = make_maze_depth_first(width, height)

        # Sprawdzamy, czy labirynt ma odpowiednie wymiary
        self.assertEqual(len(maze), height)
        self.assertEqual(len(maze[0]), width)

        # Sprawdzamy, czy brzegi labiryntu są ścianami (1)
        for i in range(height):
            self.assertEqual(maze[i][0], 1)
            self.assertEqual(maze[i][width - 1], 1)
        for j in range(width):
            self.assertEqual(maze[0][j], 1)
            self.assertEqual(maze[height - 1][j], 1)

    def test_dfs_pathfinding(self):
        """Testuje, czy DFS znajduje poprawną ścieżkę w prostym labiryncie."""
        maze = [
            [0, 1, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 0, 1],
            [1, 1, 0, 0]
        ]
        start = (0, 0)
        end = (3, 3)

        path = dfs(maze, start, end)

        # Sprawdzamy, czy DFS znalazł ścieżkę
        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], end)

        # Sprawdzamy, czy ścieżka przechodzi tylko przez przechodnie komórki (0)
        for x, y in path:
            self.assertEqual(maze[x][y], 0)

    def test_no_path(self):
        """Testuje sytuację, gdy nie ma dostępnej ścieżki."""
        maze = [
            [0, 1, 1],
            [1, 1, 1],
            [1, 1, 0]
        ]
        start = (0, 0)
        end = (2, 2)

        path = dfs(maze, start, end)
        self.assertIsNone(path)  # Oczekujemy braku ścieżki

    def test_print_maze_with_path(self):
        """Testuje, czy ścieżka jest poprawnie wizualizowana na labiryncie."""
        maze = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]

        # Sprawdzamy, czy funkcja działa bez błędów
        try:
            print_maze_with_path(maze, path)
        except Exception as e:
            self.fail(f"print_maze_with_path rzucił wyjątek: {e}")

if __name__ == "__main__":
    unittest.main()
