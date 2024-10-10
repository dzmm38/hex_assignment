import pygame

class Button:

    def __init__(self, display = None, pos = None, w=0, h=0,
                 bgColor=(204, 255, 255), selectedBgColor=(0, 204, 204),
                 text='', font='arial', fontDimension=32,
                 textColor=(0, 0, 0), value='', elevation = 5):

        self.display = display
        self.bgColor = bgColor
        self.selectedBgColor = selectedBgColor
        self.text = text
        self.font = font
        self.pos = pos
        self.original_pos = pos
        self.width = w
        self.height = h
        self.selected = False
        self.fontDimension = fontDimension
        self.textColor = textColor
        self.elevation = 5

        fontObj = pygame.font.SysFont(self.font, self.fontDimension)
        self.renderedText = fontObj.render(self.text, True, self.textColor)

        self.rectangle = pygame.Rect(pos, (w, h))
        self.bottom_rectangle = pygame.Rect(pos, (w, h))

        self.rectangleText = self.renderedText.get_rect(center=self.rectangle.center)
        self.value = value

    def select(self, selected):
        self.selected = selected
        self.draw()

    def selectByCoord(self, coord):
        if self.rectangle.collidepoint(coord):
            self.select(True)
            return True
        return False

    def draw(self):
        if self.selected:
            bgColor = self.selectedBgColor
        else:
            bgColor = self.bgColor

        self.bottom_rectangle.x = self.original_pos[0] + self.elevation//2
        self.bottom_rectangle.y = self.original_pos[1] + self.elevation
        pygame.draw.rect(self.display, self.selectedBgColor, self.bottom_rectangle, border_radius=12)
        pygame.draw.rect(self.display, bgColor, self.rectangle, border_radius=12)
        self.display.blit(self.renderedText, self.rectangleText)