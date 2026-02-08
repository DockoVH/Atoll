import Const
from Kamencic import Kamencic
import Symbol
import queue
from itertools import combinations

bfs_perimiter_cache = {}

def napravi_tablu(stranica):
    return [[None if element == '0' else napravi_kamencic(element) for element in red] for red in Const.TABLE[stranica + 5]]

def napravi_kamencic(oznaka):
    if oznaka == '1':
        return Kamencic(boja=None, zauzet=False, pocetni=False)
    elif oznaka == 'C':
        return Kamencic(boja=Symbol.C, zauzet=True, pocetni=True)
    elif oznaka == 'B':
        return  Kamencic(boja=Symbol.B, zauzet=True, pocetni=True)
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
    if not (0 <= i < len(tabla)) or not (0 <= j < len(tabla[0])):
        return False

    if tabla[i][j] is None or tabla[i][j].zauzet:
        return False

    return True

def bfs_perimiter(tabla, stranica, pocetak, kraj):
    if pocetak in kraj:
        return []
    
    kes_kljuc = (pocetak, tuple(kraj))
    if kes_kljuc in bfs_perimiter_cache.keys():
        return bfs_perimiter_cache[kes_kljuc]
    
    q = queue.Queue()
    q.put(pocetak)
    prethodni = dict()
    prethodni[pocetak] = None
    poseceni = set()
    poseceni.add(pocetak)

    pronadjen = False
    kranji_cvor = None

    while not pronadjen and not q.empty():
        cvor = q.get()

        for di, dj in Const.SUSEDNI_KAMENCICI[(cvor[0] + stranica % 2) % 2]:
            novi_cvor = (cvor[0] + di, cvor[1] + dj)
            
            if not (0 <= novi_cvor[0] < len(tabla)) or not (0 <= novi_cvor[1] < len(tabla[0])):
                continue

            if novi_cvor in kraj:
                prethodni[novi_cvor] = cvor
                pronadjen = True
                kranji_cvor = novi_cvor
                break
                
            if novi_cvor in poseceni or tabla[novi_cvor[0]][novi_cvor[1]] is None:
                continue

            if tabla[novi_cvor[0]][novi_cvor[1]].pocetni:
                continue

            prethodni[novi_cvor] = cvor

            poseceni.add(novi_cvor)

            pored_pocetnog = False
            for dx, dy in Const.SUSEDNI_KAMENCICI[(novi_cvor[0] + stranica % 2) % 2]: 
                susedni = (novi_cvor[0] + dx, novi_cvor[1] + dy)
                if not (0 <= susedni[0] < len(tabla)) or not (0 <= susedni[1] < len(tabla[0])):
                    continue
                if tabla[susedni[0]][susedni[1]] is not None and tabla[susedni[0]][susedni[1]].pocetni:
                    pored_pocetnog = True
                    break
            
            if pored_pocetnog:
                q.put(novi_cvor)

    putanja = list()
    if pronadjen:
        prethodni_cvor = prethodni[kranji_cvor]

        while prethodni_cvor is not pocetak:
            putanja.append(prethodni_cvor)
            prethodni_cvor = prethodni[prethodni_cvor]

        bfs_perimiter_cache[kes_kljuc] = len(putanja)
    
    return len(putanja)

def dfs_zauzeta_polja(tabla, stranica, pocetak, kraj, potez, ukljuci_pocetak_i_kraj=False):
    if pocetak in kraj:
        return [ pocetak ] if ukljuci_pocetak_i_kraj else []
    
    s = []
    s.append(pocetak)
    prethodni = dict()
    prethodni[pocetak] = None
    poseceni = set()
    poseceni.add(pocetak)

    pronadjen = False
    kranji_cvor = None

    while not pronadjen and s:
        cvor = s.pop()

        for di, dj in Const.SUSEDNI_KAMENCICI[(cvor[0] + stranica % 2) % 2]:
            novi_cvor = (cvor[0] + di, cvor[1] + dj)
            
            if not (0 <= novi_cvor[0] < len(tabla)) or not (0 <= novi_cvor[1] < len(tabla[0])):
                continue
                
            if novi_cvor in poseceni or tabla[novi_cvor[0]][novi_cvor[1]] is None:
                continue

            if not tabla[novi_cvor[0]][novi_cvor[1]].zauzet or tabla[novi_cvor[0]][novi_cvor[1]].boja != potez:
                continue

            prethodni[novi_cvor] = cvor

            if novi_cvor in kraj:
                pronadjen = True
                kranji_cvor = novi_cvor
                break

            poseceni.add(novi_cvor)
            s.append(novi_cvor)

    putanja = list()
    if pronadjen:
        if ukljuci_pocetak_i_kraj:
            putanja.append(kranji_cvor)
        prethodni_cvor = prethodni[kranji_cvor]

        while prethodni_cvor is not None if ukljuci_pocetak_i_kraj else prethodni_cvor is not pocetak:
            putanja.append(prethodni_cvor)
            prethodni_cvor = prethodni[prethodni_cvor]

        putanja.reverse()
    
    return putanja

def kraj_igre(tabla, stranica, potez):
    kombinacije_pocetnih_ostrva = combinations(Const.POCETNA_OSTRVA[stranica + 5][potez], 2)

    for pocetak, kraj in kombinacije_pocetnih_ostrva:
        duzine = []
        for x in pocetak:
            duzine.append(bfs_perimiter(tabla, stranica, x, kraj))

        duzina = min(duzine)

        if duzina >= Const.MIN_PERIMITER if stranica < 4 else duzina >= Const.MIN_PERIMITER + 1:
            duzina_puta = len(dfs_zauzeta_polja(tabla, stranica, pocetak[0], kraj, potez))

            if duzina_puta > 0:
                return True
            
    return False

def sledeci_potez(potez):
    if potez == Symbol.C:
        return Symbol.B
    return Symbol.C

def odredi_indeks_kamencica(tabla, click_pos, krug_precnik):
    for i in range(len(tabla)):
        for j in range(len(tabla[0])):
            if tabla[i][j] is not None and tabla[i][j].kliknut(click_pos, krug_precnik):
                return (i, j)
    return None

def potez_opcije(tabla):
    return [ x for red in tabla for x in red if x is not None and not x.zauzet ]