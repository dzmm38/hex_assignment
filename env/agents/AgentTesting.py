from MCTSAgent import MCTSAgent
from ShortestPathAgent import ShortestPathAgent
import env.agents.utility as util

test_board = [
    ['RED', 'RED', '.', 'RED', 'BLUE', '.', '.'],
    ['RED', 'RED', 'BLUE', 'RED', 'BLUE', 'RED', '.'],
    ['RED', 'RED', '.', 'RED', '.', '.', '.'],
    ['RED', 'RED', 'BLUE', 'BLUE', 'RED', 'BLUE', 'BLUE'],
    ['BLUE', 'RED', 'BLUE', 'BLUE', 'BLUE', 'RED', 'BLUE'],
    ['BLUE', 'RED', 'RED', '.', '.', '.', '.'],
    ['BLUE', 'BLUE', 'RED', '.', '.', '.', '.']
 ]

"""agent = MCTSAgent(iterations=10000)
agent.set_player_color("RED")
print("Gewählter Move: " + str(agent.get_move(test_board)))"""

print("RED WINDS: " + str(util.is_game_over(hex_board=test_board, color="RED")))
print("BLUE WINDS: " + str(util.is_game_over(hex_board=test_board, color="BLUE")))
agent = ShortestPathAgent(len(test_board), 5)
agent.set_player_color("RED")
print("Gewählter Move: " + str(agent.get_move(test_board)))