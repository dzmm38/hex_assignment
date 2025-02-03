from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, color='red'):
        self.color = color

    @abstractmethod
    def get_move(self):
        """
        Hier soll dann in den konkreten Klassen die methode choose_move implementiert werden
        hierbei soll dann der zug berechnet oder ausgewählt werden den der jeweilige Spieler tätigen möchte
        """
        pass

    def set_player_color(self,color):
        self.color = color

    def get_player_color(self):
        return self.color

