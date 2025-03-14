import random
from copy import deepcopy
from env.agents import Player
from tqdm import tqdm
import env.agents.utility as util

import heapq
import logging
import copy


class ShortestPathAgent(Player):
    evaluation_cache = {} # Dijkstra Cache für kürzeste Pfade damit schon durchsuchte nicht noch einmal berechnet werden

    def __init__(self, board_size: int, max_depth: int = 3):
        super().__init__()
        self.max_depth = max_depth
        self.board_size = board_size
        # ----- LOGGING CONFIG ----- #
        #logging.basicConfig(level=logging.DEBUG)


    def board_hash(self,hex_board):
        """
        Bildet Board als String ab der in evaluation_cache als key verwendet wird
        """
        return ''.join([''.join(row) for row in hex_board])


    def evaluate_board(self, hex_board: [[]]):
        """
        Bewertet den aktuellen Spielzustand. Dabei wird als bewertung ein dijkstra verwendet, um anhand des kürzesten
        weges eine bewertung vorzunehmen (genaueres im dijkstra).
        Für beide Spieler wird eine bewertung vorgenommen, um nicht nur den eigenen Teil des feldes zu berücksichtigen
        """
        board_key = self.board_hash(hex_board)  # Board-Hash als Key für Cache
        if board_key in self.evaluation_cache:
            return self.evaluation_cache[board_key]  # Falls schon berechnet → direkt zurückgeben

        own_value = 100
        opp_value = -100
        own_paths = self.dijkstra(hex_board, self.color.upper())
        opp_paths = self.dijkstra(hex_board, 'BLUE' if self.color == 'RED' else 'RED')
        if len(own_paths) != 0:
            own_value, _ = own_paths[0] # kürzester Pfad
        if len(opp_paths) != 0:
            opp_value, _ = opp_paths[0]

        result = opp_value - own_value
        self.evaluation_cache[board_key] = result
        #logging.debug("Value of board state: "+str(own_value-opp_value)+" / "+"own: "+ str(own_value)+ " -- opp: "+str(opp_value))
        return result  # kleiner gleich besserer


    def dijkstra(self, hex_board: [[]], color: str):
        """
        Berechnet von jedem start zu jedem ende jeweils den kürzesten Weg
        und returned diesen dann in einem Heap mit den jeweiligen Kosten
        """
        start_nodes, end_nodes = util.get_starting_positions(hex_board=hex_board, color=color)
        priority_queue: heapq = []
        paths = []
        distances = {} # started mit kosten unendlich für alle felder
        from_node: dict = {} # dictionary in dem die ausgehenden nodes gespeichert werden

        for start in start_nodes:
            if hex_board[start[1]][start[0]] == color:
                distances[start] = 0 # erstes setzen der Startkosten, wenn feld von selbst besetzt
                heapq.heappush(priority_queue, (0, start))
            else:
                distances[start] = 1 # erstes setzen der Startkosten, wenn feld nicht selbst besetzt
                heapq.heappush(priority_queue, (1, start))

        #logging.debug("Dijkstra Startknoten kosten: " + str(priority_queue))
        visited_nodes = set()  # sodass es keine duplicate geben kann

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            neighbors = util.get_neighbors(node=current_node, size=len(hex_board))

            if current_node in end_nodes: # abbruch kriterium
                shortest_path = []
                while current_node in from_node:
                    shortest_path.append(current_node)
                    current_node = from_node[current_node]
                shortest_path.append(current_node)
                paths.append((current_distance, shortest_path))
                #logging.debug("Selected Path: " + str(paths[::-1]) + " --- with cost: " + str(current_distance))

            if current_node in visited_nodes:
                continue # wenn dann in die nächste while instance
            visited_nodes.add(current_node)

            for neighbor in neighbors:
                if hex_board[neighbor[1]][neighbor[0]] == color:
                    cost = 0 # Wenn schon eigene Farbe
                elif hex_board[neighbor[1]][neighbor[0]] == '.':
                    cost = 1 # Wenn Feld leer ist
                else:
                    continue # ignoriert dann einfach diesen durchgang da nicht möglich

                new_distance = current_distance + cost
                if new_distance < distances.get(neighbor, float('inf')):
                    from_node[neighbor] = current_node
                    distances[neighbor] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor))
        return paths


    def minmax(self, hex_board: [[]], depth: int, alpha: float, beta: float, maximizing: bool, progress_bar=None):
        """
        MiniMax Algorithmus zur bestimmung des besten Zuges mit alpha-beta prunning
        """
        # Abbruchkriterium für die Rekursion
        if depth == 0 or util.is_game_over(hex_board=hex_board, color=self.color.upper()):
            return self.evaluate_board(hex_board=hex_board)

        possible_moves = util.get_possible_moves(hex_board=hex_board)

        # Progressbar initialisierung
        if progress_bar is None and depth == self.max_depth:
            progress_bar = tqdm(total=len(possible_moves), desc=f"MinMax Suche für Tiefe: {self.max_depth}", leave=True)

        # Maximierung des eigenen Zuges wählt die möglichkeit mit höchsten wert (da eigener Zug)
        if maximizing:
            max_evaluation = float('-inf')
            best_move = None
            random.shuffle(possible_moves)

            for move in possible_moves:
                temp_board = deepcopy(hex_board)  # kopieren des aktuellen boards zum Berechnen
                temp_board[move[1]][move[0]] = self.color.upper()
                evaluation = self.minmax(temp_board, depth - 1, alpha, beta, False) # Rekursion aufruf

                if evaluation > max_evaluation: # aktualisiert besten move wenn neuer wert höher ist als bisheriger
                    max_evaluation = evaluation
                    best_move = move

                alpha = max(alpha, evaluation)
                if alpha >= beta:
                    break  # cutoff zur steigerung der effizienz

                if progress_bar is not None:
                    progress_bar.update(1)  # Fortschritt aktualisieren

            if depth == self.max_depth:
                progress_bar.close()  # Schließe die Progress Bar nach der ersten Ebene

            if depth == self.max_depth:
                return best_move # wenn wieder bei oberste Rekursionsebene angekommen
            else:
                return max_evaluation # wenn noch in einer niedrigen Rekursion

        else:
            # Minimierung dieses Zuges (niedrigster wert)
            # da der gegner potenziell immer den schlechtesten Zug für einen selbst wählt
            min_evaluation = float('inf')
            random.shuffle(possible_moves)

            for move in possible_moves:
                temp_board = deepcopy(hex_board)  # kopieren des aktuellen boards zum Berechnen
                temp_board[move[1]][move[0]] = 'BLUE' if self.color.upper() == 'RED' else 'RED'
                evaluation = self.minmax(temp_board, depth - 1, alpha, beta, True) # Rekursion aufruf

                min_evaluation = min(min_evaluation, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break  # cutoff zur steigerung der effizienz

                if progress_bar is not None:
                    progress_bar.update(1)  # Fortschritt aktualisieren

            if depth == self.max_depth:
                progress_bar.close()  # Schließe die Progress Bar nach der ersten Ebene
            return min_evaluation


    def get_move(self, hex_board: [[]]):
        # Zunächst wird getestet, ob man mit dem aktuellen Zug gewinnen kann. Falls wird dieser zug zurückgegeben
        moves = util.get_possible_moves(hex_board)
        for move in moves:
            temp_board = copy.deepcopy(hex_board)
            temp_board[move[1]][move[0]] = self.color.upper()
            if util.is_game_over(hex_board=temp_board, color=self.color.upper()):
                logging.debug("Gewinnzug gefunden: " + str(move))
                return move

        # initialisieren der alpha und beta werte
        alpha = float('-inf')
        beta = float('inf')
        #Aufruf des MiniMax Algorithmus
        best_move = self.minmax(hex_board=hex_board,depth=self.max_depth,alpha=alpha, beta=beta,maximizing=True)
        return best_move