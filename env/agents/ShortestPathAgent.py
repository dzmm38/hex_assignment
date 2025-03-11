from env.agents import Player
from tqdm import tqdm
import env.agents.utility as util

import heapq
import logging
import copy


class ShortestPathAgent(Player):
    def __init__(self, board_size: int, max_depth: int = 3):
        super().__init__()
        self.max_depth = max_depth
        self.board_size = board_size
        # ----- LOGGING CONFIG ----- #
        logging.basicConfig(level=logging.DEBUG)


    def evaluate_board(self, hex_board: [[]]):
        """
        TESTED.
        Bewertet den aktuellen Spielzustand. Dabei wird als bewertung ein dijkstra verwendet, um anhand des kürzesten
        weges eine bewertung vorzunehmen (genaueres im dijkstra).
        Für beide Spieler wird eine bewertung vorgenommen, um nicht nur den eigenen Teil des feldes zu berücksichtigen

        Vorschlag: hier können zusätzlich weitere bewertungskriterien eingebracht werden die dann zusammen den value
        des boards bestimmen
        """
        own_value = float('inf')
        opp_value = float('-inf')

        own_paths = self.dijkstra(hex_board, self.color)
        opp_paths = self.dijkstra(hex_board, 'BLUE' if self.color == 'RED' else 'RED')

        if len(own_paths) != 0:
            # mit heappop wird der Pfad mit den geringsten Kosten ausgewählt → kürzester Pfad
            own_value, _ = heapq.heappop(own_paths)
        if len(opp_paths) != 0:
            opp_value, _ = heapq.heappop(opp_paths)

        #logging.debug("Value of board state: "+str(own_value-opp_value)+" / "+"own: "+ str(own_value)+ " -- opp: "+str(opp_value))
        return own_value - opp_value  # kleiner gleich besserer


    def dijkstra(self, hex_board: [[]], color: str):
        """
        Berechnet von jedem start zu jedem ende jeweils den kürzesten Weg
        und returned diesen dann in einem Heap mit den jeweiligen Kosten
        """
        start_nodes, end_nodes = util.get_starting_positions(hex_board=hex_board, color=color)
        priority_queue: heapq = []
        paths: heapq = []

        distances = {start: float('inf') for start in start_nodes} # started mit kosten unendlich für alle felder
        from_node: dict = {} # dictionary in dem die ausgehenden nodes gespeichert werden

        # TODO Kann ggf. vereinfacht werden
        # überprüft die startpunkte ob diese leer oder bereits vom spieler belegt sind, demnach dann die ausgangskosten
        for start in start_nodes:
            if hex_board[start[1]][start[0]] == color:
                distances[start] = 1 # erstes setzen der Startkosten, wenn feld von selbst besetzt
                heapq.heappush(priority_queue, (1, start))
            else:
                distances[start] = 3 # erstes setzen der Startkosten, wenn feld nicht selbst besetzt
                heapq.heappush(priority_queue, (3, start))

        #logging.debug("Dijkstra Startknoten kosten: " + str(priority_queue))

        visited_nodes = set()  # sodass es keine duplicate geben kann

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            neighbors = util.get_neighbors(node=current_node, size=len(hex_board))

            if current_node in end_nodes:
                shortest_path = []
                while current_node in from_node:
                    shortest_path.append(current_node)
                    current_node = from_node[current_node]
                shortest_path.append(current_node)
                heapq.heappush(paths, (current_distance, shortest_path))
                # --- DEBUG --- #
                # print("Selected Path: " + str(path[::-1]) + " --- with cost: " + str(current_distance))
                # --- DEBUG --- #
                #logging.debug("Selected Path: " + str(paths[::-1]) + " --- with cost: " + str(current_distance))

            if current_node in visited_nodes:
                continue# TODO macht continue einfach nächste instanz in while und überspringt rest ?

            visited_nodes.add(current_node)

            for neighbor in neighbors:
                if hex_board[neighbor[1]][neighbor[0]] == color:
                    cost = 1
                elif hex_board[neighbor[1]][neighbor[0]] == '.':
                    cost = 3
                else:
                    # Hier wird ja nur geschaut nach nachbarn also generell wenn nachbar kein weg
                    # scheinbar doch machbar
                    cost = float('inf')

                new_distance = current_distance + cost

                if new_distance < distances.get(neighbor, float('inf')):
                    from_node[neighbor] = current_node
                    distances[neighbor] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        return paths

    def minmax(self, hex_board: [[]], depth: int, alpha: float, beta: float, maximizing: bool, progress_bar=None):
        # TODO irgendwas stimmt hier mit dem return von maximizing nicht da der fehler eigentlich nie auftreten soltle
        if depth == 0 or util.is_game_over(hex_board=hex_board, color=self.color):
            return self.evaluate_board(hex_board=hex_board)

        possible_moves = util.get_possible_moves(hex_board=hex_board)

        if progress_bar is None and depth == self.max_depth:
            progress_bar = tqdm(total=len(possible_moves), desc=f"MinMax Suche für Tiefe: {self.max_depth}", leave=True)

        if maximizing:
            max_evaluation = float('-inf')
            best_move = None

            for move in possible_moves:
                temp_board = [row[:] for row in hex_board]  # kopieren des aktuellen boards zum Berechnen ## TODO durch deepcopy erstzen
                x, y = move
                temp_board[y][x] = self.color.upper()
                evaluation = self.minmax(temp_board, depth - 1, alpha, beta, False)

                if evaluation > max_evaluation:
                    max_evaluation = evaluation
                    best_move = move

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break  # cutoff zur steigerung der effizienz

                if progress_bar is not None:
                    progress_bar.update(1)  # Fortschritt aktualisieren

            if depth == self.max_depth:
                progress_bar.close()  # Schließe die Progress Bar nach der ersten Ebene
            # return max_evaluation if depth > 1 else best_move
            return best_move if depth == self.max_depth else max_evaluation


        else:
            min_evaluation = float('inf')
            for move in possible_moves:
                temp_board = [row[:] for row in hex_board]  # kopieren des aktuellen boards zum Berechnen
                x, y = move
                temp_board[y][x] = 'BLUE' if self.color.upper() == 'RED' else 'RED'
                evaluation = self.minmax(temp_board, depth - 1, alpha, beta, True)

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
            temp_board[move[1]][move[0]] = self.color
            if util.is_game_over(hex_board=temp_board, color=self.color):
                logging.debug("Gewinnzug gefunden: " + str(move))
                return move

        alpha = float('-inf')
        beta = float('inf')
        best_move = self.minmax(hex_board=hex_board,depth=self.max_depth,alpha=alpha, beta=beta,maximizing=True)
        return best_move