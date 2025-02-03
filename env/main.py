import consts
import pygame
import sys
import startPage

from Game import Game
from env.agents import HumanPlayer, RandomKI


if __name__ == '__main__':
    pygame.init()

    icon = pygame.image.load('../images/hex.png')
    pygame.display.set_caption("Hex Game")
    pygame.display.set_icon(icon)

    hexgame = Game()
    display = pygame.display.set_mode(size=hexgame.screenSize)

    hexgame.initialiseGame(display, hexgame)

    display.fill(consts.BACKGROUND_COLOR)
    startColor, opponentType, gameSize = startPage.homePage(hexgame, display)

    # Aktualisiere die Spielfeldgröße mit dem neuen gameSize-Wert
    hexgame.updateGameSize(gameSize)

    # Initialisiere die beiden Spieler
    hexgame.initialise_players(opponent=opponentType,color=startColor)

    hexgame.current_player = hexgame.player1 #TODO Player 1 fängt aktuell immer an d.h. das dass auch immer der menschliche spieler ist

    hexgame.drawBoard()
    pygame.display.update()

    while hexgame.running:
        hexgame.drawBoard()
        events = pygame.event.get()

        for event in events:
            # if the x is pressed in pygame window
            if event.type == pygame.QUIT:
                hexgame.running = False
                pygame.quit()

### ---------------------------------------------------------------------- ###
### ------------------------- Human Player Logic ------------------------- ###
### ---------------------------------------------------------------------- ###
            if isinstance(hexgame.current_player, HumanPlayer):
                # if the mouse is pressed with left-click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    # if the quit button is pressed during game
                    if hexgame.quitButton.selectByCoord(mouse_pos):
                        hexgame.running = False
                        pygame.quit()
                        sys.exit(0)

                    # make move
                    tile = hexgame.getNearestTile(mouse_pos)
                    x, y = tile.gridPosition

                    if hexgame.matrix[y][x] == hexgame.EMPTY and not hexgame.isGameOver():
                        hexgame.handle_move(x=x,y=y,tile=tile)

### ---------------------------------------------------------------------- ###
### ------------------------ RandomKI Agent Logic ------------------------ ###
### ---------------------------------------------------------------------- ###
            elif isinstance(hexgame.current_player, RandomKI):
                x,y = hexgame.current_player.get_move(gameSize) # get a move from the agent

                # checks if the move is valid -- if not gets a new move --> does this till a valid move is returned
                while(hexgame.matrix[y][x] != hexgame.EMPTY and not hexgame.isGameOver()):
                    x,y = hexgame.current_player.get_move(gameSize)

                tile = hexgame.get_tile(x,y)    # converts the two values form the agent into a tile

                # check whether tile is empty and game is not over yet
                if hexgame.matrix[y][x] == hexgame.EMPTY and not hexgame.isGameOver():
                    hexgame.handle_move(x=x,y=y,tile=tile)

