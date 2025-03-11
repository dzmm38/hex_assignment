import random
import math
import env.agents.utility as util
from copy import deepcopy

class MCTSNode:
    """
    Baum Knoten der für die MonteCarlo Tree Search verwendet wird.
    Bildet Basisstruktur für den Aufbau eines Trees
    """
    def __init__(self, hex_board: [[]], color:str, move: tuple[int,int] = None, parent = None):
        self.hex_board = hex_board # Das aktuelle hex board das bei er erstellung der Node übergeben wurde
        self.parent = parent # Abstammungsknoten (für den root Knoten ist dieser None da es keiner davor gibt)
        self.move = move # der Zug der zu diesem Knoten führt → von dem vorherigen Knoten aus
        self.color = color

        self.children: [] = [] # Kinder des aktuellen Knoten (verfügbare moves)
        self.visits: int = 0 # wert der angibt wie oft dieser Knoten bei der MCTS besucht wurde
        self.wins: int = 0 # wert der angibt wie oft, ausgehend von leaf Knoten bis hierhin gewonnen werden konnte


    def is_fully_expanded(self) -> bool:
        """
        liefert einen bool Wert, ob die node fully expanded ist. Das heißt das ausgehend von diesem Knoten alle
        möglichen züge versucht wurden und als kinder bei dieser Node registriert sind
        """
        # wenn Anzahl Kinder gleich Anzahl an möglichen moves dann komplett expanded
        if len(self.children) == len(util.get_possible_moves(self.hex_board)):
            return True
        else:
            return False


    def best_children(self, exploration_weight: float = 1):
        """
        Verwendet den UCT → Upper Confidence Bound for Trees, um den besten Kinds-knoten des Baumes auszuwählen
        UCT = (Wi / Ni) + C * Wurzel((ln*Np) / (Ni + 1))
        UCT sucht damit eine sinnvoll anteil von
            Exploitation (Beste aktuelle Möglichkeit) und
            Exploration (erkunden neuer Möglichkeiten)
            damit ggf. DIE beste Möglichkeit nicht übersehen wird

        Formel Beschreibung:
            Wi / Ni → Anteil der gewonnenen Spiele (Wi) basieren auf allen visits (Ni)
            C → Exploration Weight
            Np → Ausgehend vom Elternknoten i gespielten Simulationen (visits)
            Ni → gespielte Simulationen ausgehen vom knoten
        """
        best_child = None
        best_utc_value = float('-inf')

        for child in self.children:
            exploitation = (child.wins / child.visits) if child.visits > 0 else 0  # verhindert das durch 0 geteilt wird
            exploration = exploration_weight * math.sqrt(
                math.log(self.visits) / (child.visits + 1))  # +1 damit nicht durch 0 geteilt wird

            utc_value = exploitation + exploration # zusammensetzen zu utc wert

            # Hier dann den maximalen wert und damit das beste Kind aussuchen
            if utc_value > best_utc_value:
                best_utc_value = utc_value
                best_child = child

            # TODO old code noch entfernen
            """return max(self.children, key=lambda child:
                        (child.wins / child.visits if child.visits > 0 else 0) +
                        exploration_weight * math.sqrt(math.log(self.visits) / (child.visits + 1)))"""

        return best_child


    def expand(self, color: str):
        """
        Phase 2 des MCTS: erstellen neuer Knoten des Baumes.
        liefert zusätzlich den neuen Knoten als return wert (wird jedoch aktuell nicht verwendet)
        """
        available_moves = util.get_possible_moves(self.hex_board)
        move = random.choice(available_moves) # aus allen moves wird ein zufälliger ausgewählt der erweitert werden soll
        temp_board = deepcopy(self.hex_board) # erstellt 1 zu 1 kopie des aktuellen boards
        temp_board[move[1]][move[0]] = color    # makes the move (x und y hier wieder vertauscht)
        child_node = MCTSNode(hex_board=temp_board, parent=self, move=move, color=color)
        self.children.append(child_node) # hinzufügen der neuen node zu aktueller node (als children)
        #return child_node


    def simulate(self, color: str):
        """
        Phase 3 des MCTS: ausspielen einer Partie mit aktuell zufällig gewählten zügen. Anschließendes auswerten

        Hinweis: anstatt züge zufällig zu wählen, könnte hier dann auch heuristiken angewendet werden, um züge nicht
        komplett zufällig zu tätigen
        """
        temp_board = deepcopy(self.hex_board) # erstellt 1 zu 1 kopie des aktuellen boards
        moves = util.get_possible_moves(temp_board)
        random.shuffle(moves)
        current_player = color
        winner = None
        for move in moves:
            temp_board[move[1]][move[0]] = current_player # makes the move (x und y hier wieder vertauscht)

            if util.is_game_over(temp_board, current_player):
                winner = current_player
                break   # bricht die simulation ab, sobald ein spieler gewonnen hat da weitere züge keinen sinn machen

            # nach jedem zug wird dann hier der spieler getauscht und der nächste zug gemacht
            current_player = 'RED' if current_player == 'BLUE' else 'BLUE'

        return winner # Spieler zurückgeben der gewonnen hat, sofern es einen gibt, ansonsten None


    def backpropagate(self, result):
        """
        Phase 4 des MCTS: Ergebnis des Spieles nach einer simulation den Baum nach oben mitteilen und dann werte
        wie visits und wins aktualisieren, damit dann bestimmte teile des baumes priorisiert werden können und sinnvolle
        Züge getätigt werden können
        """
        self.visits += 1
        if result == self.color:    # result beinhaltet einen String mit dem Gewinner, falls vorhanden
            self.wins += 1
        if self.parent: # wenn ein parent vorhanden ist, dann weiter nach oben propagieren → nur bei 'root'-node nicht
            self.parent.backpropagate(result)