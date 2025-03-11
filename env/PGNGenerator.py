from datetime import datetime
from agents import Player


class PGNGenerator:
    def __init__(self, filename="hex.pgn"):
        self.filename = filename
        self.games = []


    def start_pgn_generator(self, player1:Player, player2:Player, game_round, board_size=11):
        game = {
            "event" : "Hex Games",
            "site" : "Local",
            "date" : datetime.today().strftime('%Y-%m-%d'),
            "round" : game_round,
            "board_size" : board_size,
            "player1" : player1.__class__.__name__,
            "player2" : player2.__class__.__name__,
            "moves" : [],
            "result" : None
        }
        self.games.append(game)

    def add_move(self, move, game_round):
        # Move ist ein Tupel der das tile beschreibt
        if self.games:
            self.games[game_round-1]["moves"].append(move)

    def set_result(self, result, game_round):
        # Result ist ebenfalls ein tupel
        if self.games:
            self.games[game_round-1]["result"] = result

    def save_file(self):
        with open(self.filename, "w") as file:
            for game in self.games:
                file.write(f"[Event \"{game['event']}\"]\n")
                file.write(f"[Site \"{game['site']}\"]\n")
                file.write(f"[Date \"{game['date']}\"]\n")
                file.write(f"[Round \"{game['round']}\"]\n")
                file.write(f"[BoardSize \"{game['board_size']}\"]\n")
                file.write(f"[Player1 \"{game['player1']}\"]\n")
                file.write(f"[Player2 \"{game['player2']}\"]\n")
                file.write(f"[Result \"{game['result']}\"]\n\n")

                moves = " ".join([f"{i + 1}. ({x},{y})" for i, (x, y) in enumerate(game['moves'])])
                file.write(moves + "\n\n")
                file.write(f"{game['result']}\n\n")

        print(f"PGN-Datei wurde gespeichert: {self.filename}")

