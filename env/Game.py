import consts
import pygame
import sys
import random

from HexBoard import Grid
from Buttons import Button
from env.PGNGenerator import PGNGenerator
from env.agents import Player, RandomKI, HumanPlayer

class Game:
    EMPTY = '.'
    #TODO hier habe ich zwei variablen hinzugefügt damit man später zwischen den spieler objekten unterscheiden kann
    player1: Player
    player2: Player
    starting_player: Player
    current_game: int = 1
    max_game: int
    pgn_generator: PGNGenerator = None

    def __init__(self, matrix = None):
        self.backgroundColor = consts.BACKGROUND_COLOR
        self.screenSize = (1280, 720)
        self.boardPosition = (250, 80)

        self.tileSize = 30
        self.NUM_ROWS = 11
        self.NUM_COLS = 11

        self.grid = Grid(self.NUM_ROWS, self.NUM_COLS, self.tileSize)
        self.num_emptyTiles = self.NUM_ROWS * self.NUM_COLS   # counter for number of left empty tiles in game

        # colours
        self.emptyColour = (70, 70, 70)
        self.playerColours = {
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'white': (255, 255, 255) # Gewinnfarbe -- wird verwendet für den Lösungspfad
        }

        self.current_player = None
        self.running = True

        for tile in self.hexTiles():
            tile.colour = self.emptyColour

        # used for logic of tile occupancy and terminal output
        self.matrix = matrix or [[self.__class__.EMPTY for _ in range(self.NUM_COLS)] for _ in range(self.NUM_ROWS)]
        self.text = 'Red\'s turn'
        self.solution = None # ist ungleich None, wenn es einen Gewinner gibt (enthält dann Tiles die zum Gewinnpfad gehören)
        self.quitButton = None

        if self.pgn_generator is not None:
            self.star_generator(self.NUM_ROWS)

    def updateGameSize(self, gameSize):
        self.NUM_ROWS = gameSize
        self.NUM_COLS = gameSize
        self.grid = Grid(self.NUM_ROWS, self.NUM_COLS, self.tileSize)
        self.num_emptyTiles = self.NUM_ROWS * self.NUM_COLS
        self.matrix = [[self.__class__.EMPTY for _ in range(self.NUM_COLS)] for _ in range(self.NUM_ROWS)]
        for tile in self.hexTiles():
            tile.colour = self.emptyColour

    # TODO eine methode zum erstellen der spieler objekte hier werden dann die verschiedenen matchups aufgelistet
    def initialise_players(self,opponent_1, opponent_2, player_1_color, player_2_color):
        if opponent_1 == 'mensch':
            self.player1 = HumanPlayer()
        elif opponent_1 == 'ki':
            self.player1 = RandomKI()

        if opponent_2 == 'mensch':
            self.player2 = HumanPlayer()
        elif opponent_2 == 'ki':
            self.player2 = RandomKI()

        self.player1.set_player_color(player_1_color)
        self.player2.set_player_color(player_2_color)

    @classmethod
    def initialiseGame(cls, display, game):
        cls.display = display
        cls.tileSize = game.tileSize

    def hexTiles(self):
        return self.grid.tiles.values()

    def getNearestTile(self, pos):
        nearestTile = None
        minDist = sys.maxsize

        for tile in self.hexTiles():
            distance = tile.distanceSq(pos, self.boardPosition)
            if distance < minDist:
                minDist = distance
                nearestTile = tile
        return nearestTile


    def get_tile(self,x,y):
        return self.grid.tiles[x,y]

    #TODO muss überarbeitet werden damit hier Klassen verwendet werden können
    def changePlayer(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        elif self.current_player == self.player2:
            self.current_player = self.player1

        #self.current_player = 'blue' if self.current_player == 'red' else 'red'

    def findSolutionPath(self):
        '''
        Checkt nach jedem Zug, ob es einen gewinner gibt.
        Macht das für beide Farben (Rot und Blau)
        '''
        for tile in self.grid.topRow():
            if tile.colour == self.playerColours['red']:
                path = self.grid.findPath(
                    tile,
                    self.grid.bottomRow(),
                    self.playerColours['red']
                )

                if path is not None:
                    return path

        for tile in self.grid.leftColumn():
            if tile.colour == self.playerColours['blue']:
                path = self.grid.findPath(
                    tile,
                    self.grid.rightColumn(),
                    self.playerColours['blue']
                )

                if path is not None:
                    return path

        return None


    def isGameOver(self):
        if self.solution is None:
            self.solution = self.findSolutionPath()
        return self.solution is not None


    def drawSolutionPath(self):
        '''
        Ändert die Farbe eines Tiles das zu dem Gewinnpfad gehört auf weiß (ist unter playerColours anpassbar).
        Ruft nach der änderung dann drawBoard auf damit das Spielfeld mit den aktualisierten Farben neu gezeichnet wird
        '''
        path_color = self.playerColours['white']

        for tile in self.solution:
            tile.colour = path_color

        self.drawBoard()


    # terminal output methods
    def showMatrix(self):
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j in range(len(row)):
                if j == 0:
                    print(' ' * i, end='')
                print(str(row[j]), end=' ')
            print()

    def showText(self):
        # Shows the Turn text
        fontObj = pygame.font.SysFont('arial', 40)
        renderedText = fontObj.render(self.text, True, (255, 255, 255))
        width = 400
        height = 100
        left = self.screenSize[0] / 2 - width / 2
        top = self.screenSize[1] - 1.3 * height
        rectangle = pygame.Rect(left, top, width, height)
        rectangleText = renderedText.get_rect(center=rectangle.center)
        pygame.draw.rect(self.display, self.backgroundColor, rectangle)
        self.display.blit(renderedText, rectangleText)

    # drawing methods
    def drawTile(self, tile):
        corners = tile.cornerPoints(self.boardPosition)
        pygame.draw.polygon(self.display, tile.colour, corners)
        pygame.draw.polygon(self.display, (50, 50, 50), corners, 5)
        pygame.draw.polygon(self.display, (255, 255, 255), corners, 3)

    def drawBoard(self):
        self.display.fill(self.backgroundColor)
        for tile in self.hexTiles():
            self.drawTile(tile)

        self.showText()
        self.show_game_number()

        self.drawBorder()
        self.drawQuitButton()
        self.draw_next_button()
        self.drawTHMLogo()

    def drawBorder(self):
        colours = list(self.playerColours.values())
        colour1 = colours[0]
        colour2 = colours[1]
        width = 4

        self.drawOneSideBorder(colour1, self.grid.topRow(), 3, 6, width)
        self.drawOneSideBorder(colour1, self.grid.bottomRow(), 0, 3, width)
        self.drawOneSideBorder(colour2, self.grid.leftColumn(), 1, 4, width)
        self.drawOneSideBorder(colour2, self.grid.rightColumn(), 4, 1, width)

    def drawOneSideBorder(self, colour, row, fromPoint, toPoint, width):
        for tile in row:
            corners = tile.cornerPoints(self.boardPosition)
            if fromPoint >= toPoint:
                corners = corners[fromPoint:] + corners[:toPoint]
            else:
                corners = corners[fromPoint:toPoint]
            pygame.draw.lines(self.display, color=colour, points=corners, width=width, closed=False)

    def drawQuitButton(self):
        buttonWidth = 150
        buttonHeight = 50
        self.quitButton = Button(display=self.display,
                                 pos = [self.screenSize[0] - buttonWidth - 20, 20],
                                 w=buttonWidth,
                                 h=buttonHeight,
                                 text="QUIT",
                                 bgColor=consts.THM_COLOR,
                                 selectedBgColor=consts.THM_LIGHT_COLOR,
                                 fontDimension=26,
                                 textColor=consts.WHITE)
        self.quitButton.draw()

    def draw_next_button(self):
        buttonWidth = 150
        buttonHeight = 50
        self.next_button = Button(display=self.display,
                                  pos = [self.screenSize[0] - buttonWidth - 20, self.screenSize[1] - buttonHeight - 20],
                                  w=buttonWidth,
                                  h=buttonHeight,
                                  text="NEXT",
                                  bgColor=consts.THM_COLOR,
                                  selectedBgColor=consts.THM_LIGHT_COLOR,
                                  fontDimension=26,
                                  textColor=consts.WHITE)
        self.next_button.draw()


    def drawTHMLogo(self):
        logo = pygame.image.load("../images/logo.png")
        scaled_logo = pygame.transform.scale(logo, (210, 70))
        self.display.blit(scaled_logo, (20, self.screenSize[1]-90))


    def handle_move(self,x,y,tile):
        # check whether tile is empty and game is not over yet
        if self.matrix[y][x] == self.EMPTY and not self.isGameOver():

            self.pgn_generator.add_move((x,y),self.current_game)

            tile.colour = self.playerColours[self.current_player.get_player_color()]  # Change
            # update logic in game, that is, matrix, visitedTiles and number of emptyTiles
            self.matrix[y][x] = self.current_player.get_player_color().upper()  # Change
            self.grid.visitedTiles[tile.gridPosition] = 1
            self.num_emptyTiles -= 1

            if self.isGameOver():
                self.text = 'Game over! {} wins!'.format(self.current_player.get_player_color().capitalize())
                self.drawSolutionPath()  # Färbt den Gewinnpfad neu ein

                self.pgn_generator.set_result(("1-0" if self.current_player == self.player1 else "0-1"),self.current_game)

            else:
                # change the player
                self.changePlayer()
                self.text = self.current_player.get_player_color().capitalize() + '\'s turn'

            # update the screen
            self.drawBoard()
            pygame.display.update()

    def reset_game(self, game_size, current_player):
        self.current_game = self.current_game + 1
        self.__init__()
        self.updateGameSize(game_size)
        self.random_starting_player()

    def random_starting_player(self):
        starting_player = random.randint(0,1)
        self.current_player = self.player1 if starting_player == 0 else self.player2

    def show_game_number(self):
        text = "Game: " + str(self.current_game) + " / " + str(self.max_game)
        fontObj = pygame.font.SysFont('arial', 40)
        renderedText = fontObj.render(text, True, (255, 255, 255))
        width = 400
        height = 100
        left = self.screenSize[0] / 2 - width / 2
        top = self.screenSize[1] - 2 * height
        rectangle = pygame.Rect(left, top, width, height)
        rectangleText = renderedText.get_rect(center=rectangle.center)
        pygame.draw.rect(self.display, self.backgroundColor, rectangle)
        self.display.blit(renderedText, rectangleText)


    def set_pgn_generator(self, generator: PGNGenerator):
        self.pgn_generator = generator

    def star_generator(self, board_size):
        self.pgn_generator.start_pgn_generator(player1=self.player1, player2=self.player2,
                                               game_round=self.current_game, board_size=board_size)


