import time

import consts
import pygame
import sys
import startPage

from Game import Game
from env.agents import HumanPlayer
from PGNGenerator import PGNGenerator


if __name__ == '__main__':
    pgn_generator = PGNGenerator()

    current_game = 1
    pygame.init()

    icon = pygame.image.load('../images/hex.png')
    pygame.display.set_caption("Hex Game")
    pygame.display.set_icon(icon)

    hexgame = Game()
    display = pygame.display.set_mode(size=hexgame.screenSize)


    hexgame.initialiseGame(display, hexgame)

    display.fill(consts.BACKGROUND_COLOR)
    player_1_color, player_2_color, opponent_1_type, opponent_2_type, gameSize, number_of_games = startPage.homePage(hexgame, display)

    # Aktualisiere die Spielfeldgröße mit dem neuen gameSize-Wert
    hexgame.updateGameSize(gameSize)

    # Initialisiere die beiden Spieler
    hexgame.initialise_players(opponent_1=opponent_1_type,opponent_2=opponent_2_type,
                               player_1_color=player_1_color, player_2_color=player_2_color)
    hexgame.max_game = number_of_games

    # sets the pgn generator for the current hexgame and initialises it
    hexgame.set_pgn_generator(generator=pgn_generator)
    hexgame.star_generator(board_size=gameSize)

    # sets starting player
    hexgame.current_player = hexgame.player1
    hexgame.starting_player = hexgame.current_player

    hexgame.drawBoard()
    pygame.display.update()

    while hexgame.running:
        hexgame.drawBoard()

        ## ------ ------------------ ------ ##
        ## ------ Human Player logic ------ ##
        ## ------ ------------------ ------ ##
        """
        Hier werden die Spieler Inputs überprüft
        Dieser Teil des Codes wird ausgeführt wenn ein Menschlicher Spieler Spielt
        """
        if isinstance(hexgame.current_player, HumanPlayer) and not hexgame.isGameOver():
            events = pygame.event.get()

            for event in events:
                # if the x is pressed in pygame window
                if event.type == pygame.QUIT:
                    hexgame.running = False
                    pygame.quit()

                # check if left mouse button pressed
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if hexgame.quitButton.selectByCoord(mouse_pos):
                        hexgame.running = False
                        hexgame.pgn_generator.save_file()
                        pygame.quit()
                        sys.exit(0)

                    # if no button pressed make a move (nearest tile)
                    tile = hexgame.getNearestTile(mouse_pos)
                    x, y = tile.gridPosition

                    if hexgame.matrix[y][x] == hexgame.EMPTY and not hexgame.isGameOver():
                        hexgame.handle_move(x=x, y=y, tile=tile)
                        print("HumanPlayer" + ": (" + str(x) + "," + str(y) + ")")

        ## ------ ------------------ ------ ##
        ## ------- AI Player logic -------- ##
        ## ------ ------------------ ------ ##
        # Anfrage an AI Agents nach einem Zug sofern diese am Zug sind
        elif not isinstance(hexgame.current_player, HumanPlayer) and not hexgame.isGameOver():
            time.sleep(0.1)
            x,y = hexgame.current_player.get_move(hex_board=hexgame.matrix)
            tile = hexgame.get_tile(x=x, y=y)

            if hexgame.matrix[y][x] == hexgame.EMPTY and not hexgame.isGameOver():
                hexgame.handle_move(x=x,y=y,tile=tile)

            player_class = hexgame.player2.__class__.__name__ if hexgame.current_player == hexgame.player1 else hexgame.player1.__class__.__name__
            print(str(player_class) + ": (" + str(x) + "," + str(y) + ")")


        ## ------ ------------------ ------ ##
        ## ----- Input after Game Over ---- ##
        ## ------ ------------------ ------ ##
        """
        Nachdem das Spiel vorbei wird der Spieler Input geprüft um z.B. Next Quit etc. auszuwählen
        """
        if hexgame.isGameOver():
            # Automatische next Game funktion wenn nur KI gegen KI Spielt
            if not isinstance(hexgame.player1, HumanPlayer) and not isinstance(hexgame.player2, HumanPlayer):
                if current_game < number_of_games:
                    time.sleep(2)
                    current_game = current_game + 1
                    hexgame.reset_game(game_size=len(hexgame.matrix),
                                       current_player=hexgame.player1)  # TODO hier ggf. wechsel
                    hexgame.drawBoard()
                    pygame.display.update()
                    continue

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    hexgame.running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if hexgame.quitButton.selectByCoord(mouse_pos):
                        hexgame.pgn_generator.save_file()
                        pygame.quit()
                        sys.exit()

                    if hexgame.next_button.selectByCoord(mouse_pos):
                        if current_game < number_of_games:
                            current_game = current_game + 1
                            hexgame.reset_game(game_size=len(hexgame.matrix), current_player=hexgame.player1) # TODO hier ggf. wechsel
                            hexgame.drawBoard()
                            pygame.display.update()
