import pygame
import time

from Game import Game


if __name__ == '__main__':
    pygame.init()

    icon = pygame.image.load('../images/hex.png')
    pygame.display.set_caption("Hex Game")
    pygame.display.set_icon(icon)

    hexgame = Game()
    display = pygame.display.set_mode(size=hexgame.screenSize)

    hexgame.initialiseGame(display, hexgame)

    hexgame.drawBoard()

    pygame.display.update()
    print('Start')
    hexgame.showMatrix()
    time.sleep(5)
