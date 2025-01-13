# Wizualizacja Labiryntu

Labirynt oraz ścieżka są wizualizowane za pomocą biblioteki `Matplotlib`. Dzięki tej bibliotece można przedstawić strukturę labiryntu oraz wyróżnić na nim ścieżkę rozwiązania. W wizualizacji labiryntu ściany są przedstawiane w kolorze czarnym, a przestrzenie w białym. Dodatkowo, jeśli istnieje rozwiązanie, ścieżka jest zaznaczona na zielono, co pozwala na łatwe śledzenie przejścia od punktu startowego do punktu końcowego.

## Funkcja `draw_maze`

Funkcja `draw_maze` odpowiada za rysowanie labiryntu w formie obrazu. Używa ona funkcji `imshow` z biblioteki `Matplotlib`, aby przedstawić labirynt w postaci obrazka. Ściany są rysowane na czarno, a ścieżki są białe. Opcjonalnie, jeżeli podana jest lista ścieżki, to zostaje ona zaznaczona na zielono.

### Opis

Funkcja `draw_maze` wykonuje następujące kroki:

1. Zamienia dwuwymiarową listę reprezentującą labirynt (`maze`) na obiekt typu `numpy.array`.
2. Używa funkcji `imshow` z `Matplotlib` do wyświetlenia labiryntu. Ustawia mapę kolorów na `'binary'`, co oznacza, że ściany będą czarne, a przestrzeń wewnętrzna biała.
3. Jeżeli dostarczona zostanie ścieżka (parametr `path`), funkcja narysuje ją na zielono, wykorzystując funkcję `plot` z `Matplotlib`, aby podświetlić wszystkie punkty ścieżki.

### Kod funkcji

```python
def draw_maze(maze, path=None):
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
```