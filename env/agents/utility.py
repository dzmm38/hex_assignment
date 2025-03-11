from collections import deque

def get_starting_positions(hex_board: [[]], color: str):
    """
    TESTED.
    Erstellt und liefert 2 Listen von Tupeln die Nodes eines hex spiels darstellen.
    Diese beschreiben dann jeweils die Start- und Ziel-möglichkeiten eines Spielers
    Hinweis: Bereits belegte Felder von der andern Farbe werden nicht in die Liste aufgenommen
    """
    size = len(hex_board)
    start_nodes: list[tuple[int, int]] = []
    end_nodes: list[tuple[int, int]] = []

    if color == 'RED':
        # Vertikale
        for x in range(size):
            # Hier wird überprüft, ob die Felder bereits mit RED belegt sind oder noch leer sind
            # Falls ja dann zu start und end hinzufügen
            if hex_board[0][x] == 'RED' or hex_board[0][x] == '.':
                start_nodes.append((x, 0))
            if hex_board[size - 1][x] == 'RED' or hex_board[size - 1][x] == '.':
                end_nodes.append((x, size - 1))
    else:
        # Horizontale
        for y in range(size):
            # Hier wird überprüft, ob die Felder bereits mit BLUE belegt sind oder noch leer sind
            # Falls ja dann zu start und end hinzufügen
            if hex_board[y][0] == 'BLUE' or hex_board[y][0] == '.':
                start_nodes.append((0, y))
            if hex_board[y][size - 1] == 'BLUE' or hex_board[y][0] == '.':
                end_nodes.append((size - 1, y))

    # logging.debug("Possible start Nodes for " + color + ": " + str(start_nodes))
    # logging.debug("Possible end Nodes for " + color + ": " + str(end_nodes))
    return start_nodes, end_nodes


def get_possible_moves(hex_board: [[]]):
    """
    TESTED.
    Berechnen aller möglichen Züge (Felder die Leer sind → '.').
    Liefert eine Liste von Nodes die alle möglichen Züge beinhaltet
    """
    size = len(hex_board)

    possible_moves: list[tuple[int, int]] = []
    for x in range(size):
        for y in range(size):
            if hex_board[y][x] == '.':  # only possible and valid move if the tile is free -> '.'
                possible_moves.append((x, y))

    #logging.debug("Number of possible moves: " + str(len(possible_moves)))
    #logging.debug("Possible moves : " + str(possible_moves))
    return possible_moves


def is_game_over(hex_board: [[]], color: str) -> bool:
    """
    TESTED. (ist 8x schneller als wenn man dies mit Dijkstra überprüft).
    Überprüft ob, es einen Pfad gibt der Start und Ziel Nodes miteinander verbindet anhand einer Breitensuche.
    Falls ja, ist das Spiel vorbei bzw. ein überprüfter Zug kann gewinnen.
    Liefert dann einen Bool, ob das spiel vorbei ist oder nicht
    """
    size = len(hex_board)
    visited = set() # Gewinnpfad der während der Funktion gefüllt wird
    queue = deque() # deck (Liste in der vorne und hinten herausgenommen und hinzugefügt werden kann)

    starting_nodes, _ = get_starting_positions(hex_board=hex_board, color=color)
    goal = size - 1

    # Fügt die Startknoten der queue hinzu, wenn diese die Farbe des Spielers hat
    # (sonst kann es keinen Gewinner gegeben)
    for x,y in starting_nodes:
        if hex_board[y][x] == color:
            queue.append((x,y))
            visited.add((x,y))

    while queue:
        x,y = queue.popleft() # nimmt ersten Eintrag aus dem deck

        # eigentliche Gewinn-überprüfung
        if (color == 'RED' and y == goal) or (color == 'BLUE' and x == goal):
            #logging.debug("Spieler " + str(color) + " hat gewonnen (Game Over)")
            return True

        # Überprüft nun alle nachbarn nach Verbindungen
        for nx, ny in get_neighbors((x, y), size):
            if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in visited and \
                    hex_board[ny][nx] == color:
                queue.append((nx, ny))
                visited.add((nx, ny))

    #logging.debug("Prüfung für Game Over... kein Gewinner !!")
    return False


def get_neighbors(node: tuple, size: int):
    """
    TESTED.
    Erstellt und liefert eine Liste von Tupeln x & y die Nachbarn der übergebenen Node sind
    """
    x,y = node
    # beschreibt, die schritte um zu allen nachbarn zu gelangen
    neighbor_definition = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y + 1), (x + 1, y - 1)]
    neighbors: list[tuple[int, int]] = []

    for nx, ny in neighbor_definition:
        # sollte eine node x oder y negativ sein wird diese ignoriert da es diese dann nicht gibt
        if 0 <= nx < size and 0 <= ny < size:
            neighbors.append((nx, ny))

    #logging.debug("Neighbors for node " + str(node) + ": " + str(neighbors))
    return neighbors