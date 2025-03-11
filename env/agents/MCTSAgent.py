from env.agents import Player
from tqdm import tqdm
from env.agents.MCTSNode import MCTSNode
import env.agents.utility as util
from copy import deepcopy

class MCTSAgent(Player):
    """
    Der eigentliche MCTS-KI-Agent der die Klasse MCTSNode für die Baumstruktur und funktionen nutzt
    Ausführung der MCTS Logik
    """

    # iterations = höher gleich besser (d.h. Algorithmus hat mehr informationen für die Auswahl des besten Zuges)
    def __init__(self, iterations=1000, exploration_weight: float = 1):
        super().__init__()
        self.iterations = iterations
        self.exploration_weight = exploration_weight


    def select_node(self, node):
        """
        Phase 1 des MCTS: Selektiert die node von der aus ausgehen weiter der Algorithmus angewendet werden soll.
        Dabei muss die node eine Leaf node sein.
        """
        while node.children and node.is_fully_expanded(): # ist gegebene node schon ein leaf wird diese verwendet
            node = node.best_children(exploration_weight=self.exploration_weight) # sucht nun die beste node für den MCTS aus mit einer gewissen exploration
        return node


    def get_move(self, hex_board: [[]]):
        """
        Implementierung der abstrakten Methode von Player.
        Returns a move (hoffentlich einen guten)
        """
        moves = util.get_possible_moves(hex_board)
        for move in moves:
            temp_board = deepcopy(hex_board)
            temp_board[move[1]][move[0]] = self.color
            if util.is_game_over(hex_board=temp_board, color=self.color):
                print("Gewinnzug gefunden: " + str(move))
                return move

        root = MCTSNode(hex_board=hex_board, color=self.color) # creates first note in tree (root-node)

        # Führt 'x' (iterations) mal nun den MCTS-Zyklus aus (select,expand,simulate,backpropagate)

        #TODO hier noch tqdm einbauen um den Fortschritt zu beachten !
        for _ in tqdm(range(self.iterations)):
            node = self.select_node(root) # Phase 1: select
            if not node.is_fully_expanded():
                node.expand(self.color) # Phase 2: expand
            result = node.simulate(self.color) # Phase 3: simulate
            node.backpropagate(result) # Phase 4: backpropagate

        # returns den besten zug (exploration_weight hier 0) da man nur den besten zug auswählen will
        return root.best_children(exploration_weight=0).move


### - - - - - - - - - - - - - - - - - - - - - - - - ###
### --------------- DEBUG & TESTING --------------- ###
### - - - - - - - - - - - - - - - - - - - - - - - - ###
"""test_board = [
    ['RED', '.', '.', 'RED', 'BLUE', '.', '.'],
    ['RED', '.', 'BLUE', 'RED', 'BLUE', 'RED', '.'],
    ['RED', '.', '.', 'RED', '.', '.', '.'],
    ['RED', '.', 'BLUE', 'BLUE', 'RED', 'BLUE', 'BLUE'],
    ['BLUE', 'RED', 'BLUE', 'BLUE', 'BLUE', 'RED', 'BLUE'],
    ['BLUE', 'RED', '.', '.', '.', '.', '.'],
    ['BLUE', 'BLUE', '.', '.', '.', '.', '.']
 ]

agent = MCTSAgent(iterations=10000)
agent.set_player_color("RED")
print("Gewählter Move: " + str(agent.get_move(test_board)))"""