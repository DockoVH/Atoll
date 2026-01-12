import Symbol
import math

class Kamencic:
    def __init__(self, boja: Symbol=None,  zauzet=False, pocetni=False):
        self.boja = boja
        self.zauzet = zauzet
        self.pocetni = pocetni
        self.centar = (0, 0)

    def kliknut(self, click_pos, precnik):
        razdaljina = math.sqrt((click_pos[0] - self.centar[0]) ** 2 + (click_pos[1] - self.centar[1]) ** 2)
        return razdaljina <= precnik
