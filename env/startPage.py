import math
import sys

import pygame
from pygame import font

from Buttons import *

buttonHeight = 50
algButtonWidth = 170
playerButtonWidth = 100
startButtonWidth = 110
difficultyButtonWidth = 200
gametypeButtonWidth = 300
topMargin = 60
number_of_games = 0


def homePage(game, display):
    fieldSize = ButtonGroup(
        top=4 * topMargin + buttonHeight,
        left=game.screenSize[0] / 2 - (playerButtonWidth + playerButtonWidth/2),
        buttonList=[
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="7x7", value=7,
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="9x9", value=9,
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="11x11", value=11,
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK)
        ],
        selected=0
    )

    start = Button(display=display,
                   pos=[game.screenSize[0] / 2 - startButtonWidth / 2, 6*topMargin + 1*buttonHeight],
                   w = startButtonWidth,
                   h = buttonHeight,
                   textColor=consts.BLACK,
                   text = "Start")
    quitbtn = Button(display=display,
                     pos=[game.screenSize[0] / 2 - startButtonWidth / 2, 6*topMargin + 2*buttonHeight+35],
                     w = startButtonWidth,
                     h = buttonHeight,
                     textColor=consts.BLACK,
                     text = "Quit")

    text = "Welcome to the Game Hex. Please choose from the following options"
    fontObj = pygame.font.SysFont('arial', 40)
    renderedText = fontObj.render(text, True, (255, 255, 255))
    width = 400
    height = 100
    left = game.screenSize[0] / 2 - width / 2
    top = topMargin
    rectangle = pygame.Rect(left, top, width, height)
    rectangleText = renderedText.get_rect(center=rectangle.center)
    pygame.draw.rect(game.display, game.backgroundColor, rectangle)
    game.display.blit(renderedText, rectangleText)

    # Custom Layout
    # Buttons für Spieler 1
    renderedText = fontObj.render("Player 1", True, (255, 255, 255))
    width = playerButtonWidth
    height = 50
    left = game.screenSize[0] / 4 - width / 2
    top = topMargin + 100
    rectangle = pygame.Rect(left, top, width, height)
    rectangleText = renderedText.get_rect(center=rectangle.center)
    pygame.draw.rect(game.display, game.backgroundColor, rectangle)
    game.display.blit(renderedText, rectangleText)

    # Button um gegen Mensch vs Mensch oder Mensch vs KI zu spielen
    opponent_1 = ButtonGroup(
        top=3 * topMargin + buttonHeight,
        left=game.screenSize[0] / 4 - playerButtonWidth,
        buttonList=[
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="Mensch", value="mensch",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="KI-Agent", value="ki",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
        ],
        selected=0
    )

    player_1_color = ButtonGroup(
        top=4 * topMargin + buttonHeight,
        left=game.screenSize[0] / 4 - playerButtonWidth,
        buttonList=[
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="Red", value="red",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="Blue", value="blue",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK)
        ],
        selected=0
    )

    # Buttons für Spieler 2
    renderedText = fontObj.render("Player 2", True, (255, 255, 255))
    width = 50
    height = 50
    left = (game.screenSize[0] / 4) * 3 - width /2
    top = topMargin + 100
    rectangle = pygame.Rect(left, top, width, height)
    rectangleText = renderedText.get_rect(center=rectangle.center)
    pygame.draw.rect(game.display, game.backgroundColor, rectangle)
    game.display.blit(renderedText, rectangleText)

    opponent_2 = ButtonGroup(
        top=3 * topMargin + buttonHeight,
        left=(game.screenSize[0] / 4)*3 - playerButtonWidth,
        buttonList=[
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="Mensch", value="mensch",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="KI-Agent", value="ki",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
        ],
        selected=0
    )

    player_2_color = ButtonGroup(
        top=4 * topMargin + buttonHeight,
        left=(game.screenSize[0] / 4)*3 - playerButtonWidth,
        buttonList=[
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="Red", value="red",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="Blue", value="blue",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK)
        ],
        selected=1
    )



    #Textfeld
    #Textfeld für Anzahl der Spiele
    FONT = pygame.font.Font(None, 40)
    color_activ = consts.BACKGROUND_COLOR
    color_inactive = consts.BLACK
    color = color_inactive
    active = False
    input_text = "1"
    width, height = 200, buttonHeight
    top = 3 * topMargin + buttonHeight
    left = game.screenSize[0] / 2 - width / 2
    input_box = pygame.Rect(left, top, width, buttonHeight)

    player_1_color.draw()
    player_2_color.draw()
    opponent_1.draw()
    opponent_2.draw()
    fieldSize.draw()

    start.draw(12,12,12,12)
    quitbtn.draw(12,12,12,12)

    game.drawTHMLogo()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #TODO am besten sollte das noch in die buttons datei irgednwie ausgelagert werden
                if player_1_color.selectByCoord(event.pos):
                   if player_2_color.getValue() == player_1_color.getValue():
                       player_2_color.selected = 0 if player_2_color.selected else 1

                       player_2_color.buttonList[0].selected = True if player_2_color.selected == 0 else False
                       player_2_color.buttonList[1].selected = True if player_2_color.selected == 1 else False

                elif player_2_color.selectByCoord(event.pos):
                   if player_1_color.getValue() == player_2_color.getValue():
                       player_1_color.selected = 0 if player_1_color.selected else 1

                       player_1_color.buttonList[0].selected = True if player_1_color.selected == 0 else False
                       player_1_color.buttonList[1].selected = True if player_1_color.selected == 1 else False


                player_1_color.draw()
                player_2_color.draw()
                print("Player 1: " + player_1_color.getValue())
                print("Player 2: " + player_2_color.getValue())

                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_activ if active else color_inactive
                pos = pygame.mouse.get_pos()
                if quitbtn.selectByCoord(pos):
                    pygame.quit()
                    sys.exit(0)
                if (
                        not opponent_1.selectByCoord(pos) and
                        not opponent_2.selectByCoord(pos) and
                        not fieldSize.selectByCoord(pos)
                ): #Aktivierung des Opponent-Buttons
                    if start.selectByCoord(pos):
                        return player_1_color.getValue(), player_2_color.getValue(), opponent_1.getValue(),opponent_2.getValue(), fieldSize.getValue(), int(input_text)


            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        pygame.draw.rect(game.display, color, input_box)
        text_surface = FONT.render(input_text, True, consts.BLACK)
        game.display.blit(text_surface, (input_box.x + 5, input_box.y + 10))
        pygame.display.update()
