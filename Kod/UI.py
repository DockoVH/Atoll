import math
import pygame
import Symbol
import Const
import queue
from itertools import combinations
import GameEngine

def crtaj_tablu(prozor, stranica, beli_krug, crni_krug, tabla):
    boja1 = (54, 62, 64)
    boja2 = (147, 154, 156)
    centar = (prozor.get_width() / 2, prozor.get_height() / 2)
    r_spolja = ((stranica / 4) * prozor.get_height() * 0.15 + prozor.get_height() * 0.8) / 2
    debljina = r_spolja * math.sqrt(3) / (6 + stranica)
    r_unutra = r_spolja - debljina / math.cos(math.radians(30))

    crtaj_sredinu_table(prozor, centar, r_unutra)
    crtaj_linije_tabla(prozor, centar, stranica + 4, r_unutra)
    crtaj_okvir(prozor, centar, r_spolja, r_unutra, boja1, boja2)

    crtaj_kamencice(prozor, stranica + 5, r_unutra, beli_krug, crni_krug, tabla, centar)

def crtaj_okvir(prozor, centar, r_spolja, r_unutra, boja1, boja2):
    tacke_spolja = []
    for i in range(6):
        ugao = math.radians(60 * i - 30)
        x = centar[0] + r_spolja * math.cos(ugao)
        y = centar[1] + r_spolja * math.sin(ugao)
        tacke_spolja.append((x, y))

    tacke_unutra = []
    for i in range(6):
        ugao = math.radians(60 * i - 30)
        x = centar[0] + r_unutra * math.cos(ugao)
        y = centar[1] + r_unutra * math.sin(ugao)
        tacke_unutra.append((x, y))

    for i in range(6):
        sledeci_i = (i + 1) % 6

        sredina_spolja = (
            (tacke_spolja[i][0] + tacke_spolja[sledeci_i][0]) / 2,
            (tacke_spolja[i][1] + tacke_spolja[sledeci_i][1]) / 2
        )

        sredina_unutra = (
            (tacke_unutra[i][0] + tacke_unutra[sledeci_i][0]) / 2,
            (tacke_unutra[i][1] + tacke_unutra[sledeci_i][1]) / 2
        )

        poligon1 = [
            tacke_spolja[i],
            sredina_spolja,
            sredina_unutra,
            tacke_unutra[i]
        ]
        pygame.draw.polygon(prozor, boja1, poligon1)

        poligon2 = [
            sredina_spolja,
            tacke_spolja[sledeci_i],
            tacke_unutra[sledeci_i],
            sredina_unutra
        ]
        pygame.draw.polygon(prozor, boja2, poligon2)

def crtaj_linije_tabla(prozor, centar, broj_linija, r_unutra):
    def crtaj_liniju(x, y, temena):
        uglovi = [90, 30, -30]

        for ugao in uglovi:
            ugao_rad = math.radians(ugao)

            x_kraj = x + 2000 * math.cos(ugao_rad)
            y_kraj = y + 2000 * math.sin(ugao_rad)

            najbolji_presek = None
            min_rastojanje = float('inf')

            for i in range(6):
                sledeci_i = (i + 1) % 6
                teme1 = temena[i]
                teme2 = temena[sledeci_i]

                presek = presek_linija(x, y, x_kraj, y_kraj, teme1[0], teme1[1], teme2[0], teme2[1])
                if presek:
                    rastojanje = math.sqrt((presek[0] - x) ** 2 + (presek[1] - y) ** 2)
                    if presek[2] > 0.001 and rastojanje < min_rastojanje:
                        min_rastojanje = rastojanje
                        najbolji_presek = (presek[0], presek[1])

            if najbolji_presek:
                pygame.draw.line(prozor, (16, 16, 16), (x, y), najbolji_presek)

    def presek_linija(x1, y1, x2, y2, x3, y3, x4, y4):
        imenilac = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(imenilac) < 0.001:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / imenilac
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / imenilac

        if 0 <= u <= 1:
            px = x1 + t * (x2 - x1)
            py = y1 + t * (y2 - y1)
            return  (px, py, t, u)

        return None

    tacke = []
    for i in range(6):
        ugao = math.radians(60 * i - 30)
        x = centar[0] + r_unutra * math.cos(ugao)
        y = centar[1] + r_unutra * math.sin(ugao)
        tacke.append((x, y))

    for i in range(6):
        sledeci_i = (i + 1) % 6
        pocetak = tacke[i]
        kraj = tacke[sledeci_i]

        for j in range(broj_linija):
            t = j / broj_linija
            x = pocetak[0] + t * (kraj[0] - pocetak[0])
            y = pocetak[1] + t * (kraj[1] - pocetak[1])

            crtaj_liniju(x, y, tacke)

def crtaj_sredinu_table(prozor, centar, r_unutra):
    temena = []
    for i in range(6):
        ugao = math.radians(60 * i - 30)
        x = centar[0] + r_unutra * math.cos(ugao)
        y = centar[1] + r_unutra * math.sin(ugao)
        temena.append((x, y))

    pygame.draw.polygon(prozor, (220, 207, 172), temena)

def crtaj_kamencice(prozor, stranica, r_unutra, beli_krug, crni_krug, tabla, centar):
    korak_x = (r_unutra / (stranica - 1)) * math.sqrt(3)
    korak_y = r_unutra / ((stranica - 1) * 2)
    xmin = centar[0] - (r_unutra * math.sqrt(3) / 2 + korak_x / 2)
    ymin = centar[1] - (r_unutra + korak_y)
    kamencic_prikaz_offset = beli_krug.get_width() / 2

    font = pygame.font.SysFont('Comic Sans MS', 25)

    for i, red in enumerate(tabla):
        offset_x = (i % 2) * korak_x / 2 if stranica % 2 == 1 else ((i + 1) % 2) * korak_x / 2
        y = ymin + i * korak_y

        for j, kamencic in enumerate(red):
            x = xmin + offset_x + j * korak_x

            if kamencic is not None:
                kamencic.centar = (x, y)

            if kamencic is not None and kamencic.zauzet:
                if kamencic.boja == Symbol.C:
                    prozor.blit(crni_krug, (kamencic.centar[0] - kamencic_prikaz_offset, kamencic.centar[1] - kamencic_prikaz_offset))
                else:
                    prozor.blit(beli_krug, (kamencic.centar[0] - kamencic_prikaz_offset, kamencic.centar[1] - kamencic_prikaz_offset))

def crtaj_pocetni_meni(prozor, start, exit):
    dugme_offset_x = start.get_width() // 2
    dugme_offset_y = start.get_height() // 2
    centar = (prozor.get_width() / 2 , prozor.get_height() / 2)

    prozor.blit(start, (centar[0] - dugme_offset_x , centar[1] - 3 * dugme_offset_y))
    prozor.blit(exit, (centar[0] - dugme_offset_x , centar[1] + dugme_offset_y))

def crtaj_izbor_drugi_igrac(prozor, tekst_polje, precrtano):
    font_size = 130
    font_AI = pygame.font.SysFont('Comic Sans MS', font_size)
    font_naslov = pygame.font.SysFont('Comic Sans MS', 2 * font_size)
    ymin = (prozor.get_height() - tekst_polje.get_height()) // 2
    xmin = (prozor.get_width() - 2.4 * tekst_polje.get_width()) // 2
    dugme_sirina = tekst_polje.get_width()
    dugme_visina = tekst_polje.get_height()

    naslov_prozor = font_naslov.render('Drugi igrač:', False, (255, 255, 255))
    naslov_x = (prozor.get_width()) // 2 - naslov_prozor.get_width() // 2
    naslov_y = ymin - naslov_prozor.get_height() * 1.4
    prozor.blit(naslov_prozor, (naslov_x, naslov_y))

    tekst_prozor = font_AI.render('AI', False, (255, 255, 255))
    prozor.blit(tekst_polje, (xmin, ymin))
    prozor.blit(tekst_prozor, (xmin + dugme_sirina // 2 - font_size // 3, ymin + dugme_sirina // 2 - font_size // 3))
    prozor.blit(precrtano, (xmin + (dugme_sirina - precrtano.get_width()) // 2, ymin + (dugme_visina - precrtano.get_height()) // 2))

    tekst_prozor = font_AI.render('AI', False, (255, 255, 255))
    prozor.blit(tekst_polje, (xmin + dugme_sirina * 1.2, ymin))
    prozor.blit(tekst_prozor, (xmin + dugme_sirina * 1.2 + dugme_sirina // 2 - font_size // 3, ymin + dugme_sirina // 2 - font_size // 3))

def crtaj_izbor_prvi_potez_igrac(prozor, tekst_polje, precrtano):
    font_size = 130
    font_AI = pygame.font.SysFont('Comic Sans MS', font_size)
    font_naslov = pygame.font.SysFont('Cosmic Sans MS', 2 * font_size)
    ymin = (prozor.get_height() - tekst_polje.get_height()) // 2
    xmin = (prozor.get_width() - 2.4 * tekst_polje.get_width()) // 2
    dugme_sirina = tekst_polje.get_width()
    dugme_visina = tekst_polje.get_height()

    naslov_prozor = font_naslov.render('Prvi na potezu:', False, (255, 255, 255))
    naslov_x = (prozor.get_width()) // 2 - naslov_prozor.get_width() // 2
    naslov_y = ymin - naslov_prozor.get_height() * 1.4
    prozor.blit(naslov_prozor, (naslov_x, naslov_y))

    tekst_prozor = font_AI.render('AI', False, (255, 255, 255))
    prozor.blit(tekst_polje, (xmin, ymin))
    prozor.blit(tekst_prozor, (xmin + dugme_sirina // 2 - font_size // 3, ymin + dugme_sirina // 2 - font_size // 3))
    prozor.blit(precrtano, (xmin + (dugme_sirina - precrtano.get_width()) // 2, ymin + (dugme_visina - precrtano.get_height()) // 2))

    tekst_prozor = font_AI.render('AI', False, (255, 255, 255))
    prozor.blit(tekst_polje, (xmin + dugme_sirina * 1.2, ymin))
    prozor.blit(tekst_prozor, (xmin + dugme_sirina * 1.2 + dugme_sirina // 2 - font_size // 3, ymin + dugme_sirina // 2 - font_size // 3))

def crtaj_izbor_prvi_potez_boja(prozor, tekst_polje, beli_krug, crni_krug):
    font_size = 130
    font_naslov = pygame.font.SysFont('Comic Sans MS', font_size)
    ymin = (prozor.get_height() - tekst_polje.get_height()) // 2
    xmin = (prozor.get_width() - 2.4 * tekst_polje.get_width()) // 2
    dugme_sirina = tekst_polje.get_width()
    dugme_visina = tekst_polje.get_height()
    beli_krug_prikaz = pygame.transform.scale(beli_krug, (int(dugme_sirina * 0.5), int(dugme_sirina * 0.5)))
    crni_krug_prikaz = pygame.transform.scale(crni_krug, (int(dugme_sirina * 0.5), int(dugme_sirina * 0.5)))
    krug_offset = beli_krug_prikaz.get_width()

    naslov_prozor = font_naslov.render('Prvi na potezu:', False, (255, 255, 255))
    naslov_x = (prozor.get_width()) // 2 - naslov_prozor.get_width() // 2
    naslov_y = ymin - naslov_prozor.get_height() * 1.4
    prozor.blit(naslov_prozor, (naslov_x, naslov_y))

    krug_x = xmin + (dugme_sirina - krug_offset) // 2
    krug_y = ymin + (dugme_visina - krug_offset) // 2

    prozor.blit(tekst_polje, (xmin, ymin))
    prozor.blit(beli_krug_prikaz, (krug_x, krug_y))

    prozor.blit(tekst_polje, (xmin + dugme_sirina * 1.2, ymin))
    prozor.blit(crni_krug_prikaz, (krug_x + 1.2 * dugme_sirina, krug_y))

def crtaj_izbor_velicina_table(prozor, tekst_polje):
    font_size = 130
    font_broj = pygame.font.SysFont('Comic Sans MS', font_size)
    font_naslov = pygame.font.SysFont('Comic Sans MS', 2 * font_size)
    dugme_offset = tekst_polje.get_width() * 1.1
    dugme_sirina = tekst_polje.get_width()
    ymin = (prozor.get_height() - tekst_polje.get_height()) // 2
    xmin = (prozor.get_width() - 5 * tekst_polje.get_width()) // 2

    naslov_prozor = font_naslov.render('Veličina table:', False, (255, 255, 255))
    naslov_x = (prozor.get_width()) // 2 - naslov_prozor.get_width() // 2
    naslov_y = ymin - naslov_prozor.get_height() * 1.4
    prozor.blit(naslov_prozor, (naslov_x, naslov_y))

    for i in range(5):
        text_prozor = font_broj.render(f'{i + 5}', False, (255, 255, 255))
        prozor.blit(tekst_polje, (xmin + i * dugme_offset, ymin))
        prozor.blit(text_prozor, (xmin + i * dugme_offset + dugme_sirina // 2 - font_size // 4, ymin + dugme_sirina // 2 - font_size // 4))

def crtaj_potez_opcije(prozor, potez_opcije, kamencic_slika):
    kamencic_prikaz = pygame.transform.scale(kamencic_slika, (int(kamencic_slika.get_width() * 0.5), int(kamencic_slika.get_width() * 0.5)))
    kamencic_prikaz.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
    kamencic_prikaz_offset = kamencic_prikaz.get_width() // 2

    for kamencic in potez_opcije:
        prozor.blit(kamencic_prikaz, (kamencic.centar[0] - kamencic_prikaz_offset, kamencic.centar[1] - kamencic_prikaz_offset))

def crtaj_prikazi_pobednika(prozor, tabla, stranica, pobednik, prvi_potez_boja, kamencic):
    kombinacije_pocetnih_ostrva = combinations(Const.POCETNA_OSTRVA[stranica + 5][pobednik], 2)

    for pocetak, kraj in kombinacije_pocetnih_ostrva:
        duzina1 = GameEngine.bfs_perimiter(tabla, stranica, pocetak[0], kraj)
        duzina2 = GameEngine.bfs_perimiter(tabla, stranica, pocetak[1], kraj)

        duzina = min(duzina1, duzina2)

        if duzina >= Const.MIN_PERIMITER if stranica < 4 else duzina >= Const.MIN_PERIMITER + 1:
            put = GameEngine.bfs_zauzeta_polja(tabla, stranica, pocetak[0], kraj, pobednik, ukljuci_pocetak_i_kraj=True)

            if len(put) > 0:
                for i in range(len(put) - 1):
                    pocetak = tabla[put[i][0]][put[i][1]].centar
                    kraj = tabla[put[i + 1][0]][put[i + 1][1]].centar
                    pygame.draw.line(prozor, (255, 0, 0), pocetak, kraj, 3)

    centar = (prozor.get_width() // 2, prozor.get_height() // 2)
    font_pobednik = pygame.font.SysFont('Comic Sans MS', 85)
    font_izlaz = pygame.font.SysFont('Comic Sans MS', 40)
    kamencic_prikaz = pygame.transform.scale(kamencic, (int(prozor.get_height() * 0.15), int(prozor.get_height() * 0.15)))

    izlaz_prozor = font_izlaz.render('Kliknite bilo gde da bi ste izašli.', False, (255, 255, 0))
    pobednik_prozor = font_pobednik.render('POBEDA', False, (255, 255, 255) if pobednik == Symbol.B else (0, 0, 0))
    
    tabla_sirina = ((stranica / 4) * prozor.get_height() * 0.15 + prozor.get_height() * 0.8)
    pobednik_offset_x = 1.2 * pobednik_prozor.get_width() + tabla_sirina // 2
    if pobednik != prvi_potez_boja:
        pobednik_offset_x *= -2 / 3

    prozor.blit(izlaz_prozor, (centar[0] - izlaz_prozor.get_width() // 2, prozor.get_height() - 2 * izlaz_prozor.get_height()))
    prozor.blit(pobednik_prozor, (centar[0] - pobednik_offset_x, centar[1] -  2 * pobednik_prozor.get_height()))
    prozor.blit(kamencic_prikaz, (centar[0] - pobednik_offset_x, centar[1]))