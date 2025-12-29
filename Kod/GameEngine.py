import Const
from Kamencic import Kamencic
import Symbol

def napravi_tablu(stranica):
    return [[None if element == '0' else napravi_kamencic(element) for element in red] for red in Const.TABLE[stranica + 5]]
def napravi_kamencic(oznaka):
    if oznaka == '1':
        return Kamencic()
    elif oznaka == 'C':
        return Kamencic(Symbol.C, True, True)
    elif oznaka == 'B':
        return  Kamencic(Symbol.B, True, True)
    else:
        print('greska')
        return None
def odigraj_potez(tabla, i, j, potez_boja):
    if ispravan_potez(tabla, i, j):
        tabla[i][j].boja = potez_boja
        tabla[i][j].zauzet = True
        return True
    return  False
def ispravan_potez(tabla, i, j):
    if i < 0 or j < 0 or i > len(tabla) - 1 or j > len(tabla) - 1:
        return False

    if tabla[i][j] is None or tabla[i][j].zauzet:
        return False

    return True



