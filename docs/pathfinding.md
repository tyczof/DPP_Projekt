# Algorytm DFS do znajdowania ścieżki

Algorytm **DFS** (Depth-First Search) jest popularną metodą wyszukiwania, która służy do znajdowania ścieżek w labiryncie, od punktu startowego do punktu końcowego. Algorytm działa na zasadzie głębokiej eksploracji, odwiedzając wszystkie możliwe ścieżki, zapamiętując odwiedzone komórki w stosie i przechodząc do najgłębszych ścieżek przed powrotem do wcześniejszych.

Algorytm DFS jest idealny do zastosowań, w których nie jest wymagane znalezienie najkrótszej ścieżki, a raczej po prostu jakiejkolwiek ścieżki.

### Działanie algorytmu DFS

DFS działa poprzez rekurencyjne lub iteracyjne przeszukiwanie labiryntu. Rozpoczyna od punktu startowego i odwiedza każdą komórkę, eksplorując możliwe ścieżki. W tym algorytmie stos (stack) jest używany do zapamiętywania kolejnych kroków, a zbiór `visited` śledzi komórki, które zostały już odwiedzone.

1. Zaczynamy od punktu startowego.
2. Przechodzimy do sąsiednich komórek.
3. Jeśli komórka jest drogą (pusta przestrzeń), dodajemy ją do stosu i kontynuujemy eksplorację.
4. Jeśli dotrzemy do punktu końcowego, zwracamy ścieżkę.
5. Jeśli napotkamy martwy punkt (wszystkie możliwe ścieżki zostały już sprawdzone), wracamy do poprzedniej komórki, aby kontynuować eksplorację innych ścieżek.

### Funkcja `dfs`

Funkcja `dfs` implementuje algorytm DFS w celu znalezienia ścieżki w labiryncie od punktu startowego do końcowego.


### Kod funkcji
```python
def dfs(maze, start, end):
    stack = [(start, [start])] 
    visited = set() 
    
    def get_neighbors(pos):
        x, y = pos
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == TILE_EMPTY:
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
```