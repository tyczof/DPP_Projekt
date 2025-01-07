# Generator Labiryntu

Labirynt jest generowany przy użyciu algorytmu Depth-First Search (DFS). Algorytm ten tworzy ścieżki między komórkami, zaczynając od losowej komórki.

## Funkcja `_create_grid_with_cells`

Funkcja `_create_grid_with_cells` generuje siatkę, która będzie podstawą do tworzenia labiryntu. W siatce znajdują się zarówno ściany, jak i przestrzenie przejściowe.

### Argumenty

- `width` (int): Szerokość siatki (liczba kolumn).
- `height` (int): Wysokość siatki (liczba wierszy).

### Zwracana wartość

Zwraca 2D listę, gdzie:
- `1` oznacza ścianę (reprezentowaną przez `TILE_CRATE`),
- `0` oznacza pustą przestrzeń (reprezentowaną przez `TILE_EMPTY`).

### Kod funkcji
```python
TILE_EMPTY = 0
TILE_CRATE = 1

def _create_grid_with_cells(width, height):
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
    
```


