import GameEngine
import Symbol
import Const
from itertools import combinations
import collections

oceni_bfs_cache = {}
oceni_dfs_cache = {}

def kraj(tabla, stranica):
    if GameEngine.kraj_igre(tabla, stranica, Symbol.C):
        return 1000
    elif GameEngine.kraj_igre(tabla, stranica, Symbol.B):
        return -1000
    
    return 0

def minmax(tabla, stranica, dubina, moj_potez, alpha=(None, -1000), beta=(None, 1000)):
    if moj_potez:
        return max_value(tabla, stranica, dubina, alpha, beta)
    else:
        return min_value(tabla, stranica, dubina, alpha, beta)

def max_value(tabla, stranica, dubina, alpha, beta, potez=None):
    kraj_rezultat = kraj(tabla, stranica)
    if abs(kraj_rezultat) == 1000:
        return (potez, kraj_rezultat)
    
    novi_potezi = nova_stanja(tabla)

    if dubina == 0 or novi_potezi is None or len(novi_potezi) == 0:
        return (potez, oceni(tabla, stranica))
    
    for p in novi_potezi:
        boja, zauzet = tabla[p[0]][p[1]].boja, tabla[p[0]][p[1]].zauzet
        
        if GameEngine.odigraj_potez(tabla, p[0], p[1], Symbol.C):
            alpha = max(alpha, min_value(tabla, stranica, dubina - 1, alpha, beta, p if potez is None else potez), key=lambda x: x[1])
        
        tabla[p[0]][p[1]].boja, tabla[p[0]][p[1]].zauzet = boja, zauzet

        if alpha[1] >= beta[1]:
            break
    
    return alpha

def min_value(tabla, stranica, dubina, alpha, beta, potez=None):
    kraj_rezultat = kraj(tabla, stranica)
    if abs(kraj_rezultat) == 1000:
        return (potez, kraj_rezultat)
    
    novi_potezi = nova_stanja(tabla)

    if dubina == 0 or novi_potezi is None or len(novi_potezi) == 0:
        return (potez, oceni(tabla, stranica))
    
    for p in novi_potezi:
        boja, zauzet = tabla[p[0]][p[1]].boja, tabla[p[0]][p[1]].zauzet

        if GameEngine.odigraj_potez(tabla, p[0], p[1], Symbol.B):
            beta = min(beta, max_value(tabla, stranica, dubina - 1, alpha, beta, p if potez is None else potez), key=lambda x: x[1])

        tabla[p[0]][p[1]].boja, tabla[p[0]][p[1]].zauzet = boja, zauzet
        
        if beta[1] <= alpha[1]:
            break
    
    return beta

def nova_stanja(tabla):
    return [ (i, j) for i, red in enumerate(tabla) for j, kamencic in enumerate(red) if kamencic is not None and not kamencic.zauzet ]

def oceni(tabla, stranica):
    kraj_rezultat = kraj(tabla, stranica)
    if kraj_rezultat != 0:
        return kraj_rezultat

    min_za_pobedu_c = najmanje_koraka_do_pobede(tabla, stranica, Symbol.C)
    min_za_pobedu_b = najmanje_koraka_do_pobede(tabla, stranica, Symbol.B)

    return (min_za_pobedu_b - min_za_pobedu_c) * 10

def najmanje_koraka_do_pobede(tabla, stranica, potez):
    def generisi_kes_kljuc(tabla, stranica, pocetak, kraj, potez):
        tabla_kljuc = [ (i, j) for i, red in enumerate(tabla) for j, kamencic in enumerate(red) if kamencic is not None and kamencic.zauzet and kamencic.boja == potez ]

        return (tuple(tabla_kljuc), stranica, pocetak, tuple(kraj), potez)


    def bfs(tabla, stranica, pocetak, kraj, potez):
        if pocetak in kraj:
            return 0
        
        kes_kljuc = generisi_kes_kljuc(tabla, stranica, pocetak, kraj, potez)
        if kes_kljuc in oceni_bfs_cache.keys():
            return oceni_bfs_cache[kes_kljuc]
        
        q = collections.deque()
        q.append((pocetak, 0))
        poseceni = set()
        poseceni.add(pocetak)

        pronadjen = False
        rezultat = float('inf')

        while not pronadjen and q:
            cvor, broj_praznih = q.popleft()

            for di, dj in Const.SUSEDNI_KAMENCICI[(cvor[0] + stranica % 2) % 2]:
                novi_cvor = (cvor[0] + di, cvor[1] + dj)
                
                if not (0 <= novi_cvor[0] < len(tabla)) or not (0 <= novi_cvor[1] < len(tabla[0])):
                    continue
                    
                if novi_cvor in poseceni or tabla[novi_cvor[0]][novi_cvor[1]] is None:
                    continue

                if novi_cvor in kraj:
                    pronadjen = True
                    rezultat = broj_praznih
                    break

                poseceni.add(novi_cvor)

                if tabla[novi_cvor[0]][novi_cvor[1]].zauzet and tabla[novi_cvor[0]][novi_cvor[1]].boja == potez:
                    q.append((novi_cvor, broj_praznih))
                elif not tabla[novi_cvor[0]][novi_cvor[1]].zauzet:
                    q.append((novi_cvor, broj_praznih + 1))
        
        oceni_bfs_cache[kes_kljuc] = rezultat
        return rezultat
    
    kombinacije_pocetnih_ostrva = combinations(Const.POCETNA_OSTRVA[stranica + 5][potez], 2)

    sve_duzine = []
    for pocetak, kraj in kombinacije_pocetnih_ostrva:
        obodne_duzine = []
        for kamencic in pocetak:
            obodne_duzine.append(GameEngine.bfs_perimiter(tabla, stranica, kamencic, kraj))

        min_obodna = min(obodne_duzine)
        if min_obodna >= (Const.MIN_PERIMITER if stranica < 4 else Const.MIN_PERIMITER + 1):
            duzine = []
            for kamencic in pocetak:
                duzine.append(bfs(tabla, stranica, kamencic, kraj, potez))
            sve_duzine.append(min(duzine))

    return min(sve_duzine) if sve_duzine else float('inf')