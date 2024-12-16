# Maze Generation and Pathfinding Project

This project implements a maze generation algorithm and pathfinding using Depth-First Search (DFS). It includes tests for the grid generation, maze creation, and DFS pathfinding. The project also features a CI/CD pipeline using GitHub Actions.

## Features

- **Maze Generation**: Uses the Depth-First Search algorithm to generate a maze.
- **Pathfinding**: Implements DFS to find a path through the maze.
- **Visualization**: Includes tools to print and visualize the maze and the discovered path using Matplotlib.
- **Testing**: Contains unit tests for all key functionalities using `pytest`.
- **CI/CD Pipeline**: Automated pipelines for testing, linting, and releasing the project.

## File Structure

```plaintext
.
├── test_maze_with_dfs.py      # Tests for grid creation, maze generation, and pathfinding
├── tgis_projekt.py            # Maze generation and pathfinding logic
├── requirements.txt           # Python dependencies
├── .github/
│   ├── workflows/
│   │   ├── ci.yml             # Continuous Integration pipeline
│   │   ├── cd.yml             # Continuous Deployment pipeline
```

# Usage

## Generate and Visualize a Maze
Run the following command to generate and visualize a maze with a path:

```bash
python tgis_projekt.py
```

# Running Tests

To execute the tests, run:

```bash
pytest
```

# Installation

## Clone the repository:
```bash
git clone https://github.com/tyczof/DPP_Projekt
cd DPP_Projekt
```

## Install dependencies:
```bash
pip install -r requirements.txt
```

# CI/CD Pipelines

## CI Pipeline
The **Continuous Integration** pipeline (`.github/workflows/ci.yml`) performs the following:
- Runs unit tests with code coverage.
- Lints the Python code using Flake8.

## CD Pipeline
The **Continuous Deployment** pipeline (`.github/workflows/cd.yml`) is triggered on new Git tags matching `v*`. It:
- Packages the application.
- Creates a GitHub release and uploads the release artifacts.

# Dependencies

The project uses the following Python libraries:

- `pytest`: For testing.
- `pytest-cov`: For code coverage reporting.
- `flake8`: For linting.
- `matplotlib`: For visualizing the maze.
- `numpy`: For numerical computations.

# License

This project is licensed under the [MIT License](LICENSE).
