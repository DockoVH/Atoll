import pygame
from pygame.locals import *
import pygame._sdl2
import UI
import GameEngine
import Symbol

pygame.init()
pygame.font.init()
prozor = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
window = pygame._sdl2.Window.from_display_module()
window.maximize()

prozor_visina = prozor.get_height()
prozor_sirina = prozor.get_width()
dugme_scale = 0.045

pozadina = pygame.image.load('Slike/pozadina.jpg')
beli_krug = pygame.image.load('Slike/beli_krug.png')
beli_krug_prikaz = pygame.transform.scale(beli_krug, (int(prozor_visina * dugme_scale), int(prozor_visina * dugme_scale)))
crni_krug = pygame.image.load('Slike/crni_krug.png')
crni_krug_prikaz = pygame.transform.scale(crni_krug, (int(prozor_visina * dugme_scale), int(prozor_visina * dugme_scale)))
start = pygame.image.load('Slike/start.png')
start_prikaz = pygame.transform.scale(start, (int(prozor_sirina * 0.4), int(prozor_visina * 0.2)))
exit = pygame.image.load('Slike/exit.png')
exit_prikaz = pygame.transform.scale(exit, (int(prozor_sirina * 0.4), int(prozor_visina * 0.2)))
tekst_polje = pygame.image.load('Slike/polje_tekst.png')
tekst_polje_prikaz = pygame.transform.scale(tekst_polje, (int(prozor_visina * 0.2), int(prozor_visina * 0.2)))
precrtano = pygame.image.load('Slike/precrtano.png')
precrtano_prikaz = pygame.transform.scale(precrtano, (int(prozor_visina * 0.15), int(prozor_visina * 0.15)))

def main_loop():
    global prozor_visina
    global prozor_sirina
    global beli_krug_prikaz
    global crni_krug_prikaz
    global beli_krug
    global crni_krug
    dugme_scale_prikaz = dugme_scale
    stari_dugme_scale = dugme_scale

    while True:
        pokreni_igru, stranica, drugi_igrac_AI, prvi_potez_AI, prvi_potez_boja = pocetni_meni()

        potez = prvi_potez_boja
        ai_boja = prvi_potez_boja if prvi_potez_AI else GameEngine.sledeci_potez(prvi_potez_boja)

        if pokreni_igru:
            tabla = GameEngine.napravi_tablu(stranica)

            while True:
                if prozor_visina != prozor.get_height():
                    prozor_visina = prozor.get_height()
                    prozor_sirina = prozor.get_width()
                    beli_krug_prikaz = pygame.transform.scale(beli_krug, (int(prozor_visina * dugme_scale_prikaz), int(prozor_visina * dugme_scale_prikaz)))
                    crni_krug_prikaz = pygame.transform.scale(crni_krug, (int(prozor_visina * dugme_scale_prikaz), int(prozor_visina * dugme_scale_prikaz)))

                if dugme_scale_prikaz != stari_dugme_scale:
                    beli_krug_prikaz = pygame.transform.scale(beli_krug, (int(prozor_visina * dugme_scale_prikaz), int(prozor_visina * dugme_scale_prikaz)))
                    crni_krug_prikaz = pygame.transform.scale(crni_krug, (int(prozor_visina * dugme_scale_prikaz), int(prozor_visina * dugme_scale_prikaz)))

                stari_dugme_scale = dugme_scale_prikaz

                prozor.blit(pozadina, (0, 0))

                UI.crtaj_tablu(prozor, stranica, beli_krug_prikaz, crni_krug_prikaz, tabla)

                if drugi_igrac_AI and ai_boja == potez:
                    print('AI POTEZ')
                    potez = GameEngine.sledeci_potez(potez)
                else:
                    UI.crtaj_potez_opcije(prozor, GameEngine.potez_opcije(tabla), beli_krug_prikaz if potez == Symbol.B else crni_krug_prikaz)

                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_BACKSPACE:
                                return
                        if event.type == MOUSEBUTTONDOWN:
                            click_pos = pygame.mouse.get_pos()
                            indeks = GameEngine.odredi_indeks_kamencica(tabla, click_pos, beli_krug_prikaz.get_width() // 2)
                            if indeks is not None:
                                if GameEngine.odigraj_potez(tabla, indeks[0], indeks[1], potez):
                                    potez = GameEngine.sledeci_potez(potez)
                        elif event.type == QUIT:
                            return

                if GameEngine.kraj_igre(tabla, stranica, GameEngine.sledeci_potez(potez)):
                    potez = GameEngine.sledeci_potez(potez)
                    print('kraj')
                    break
            
                pygame.display.update()

            prikazi_pobednika = True

            while prikazi_pobednika:
                UI.crtaj_tablu(prozor, stranica, beli_krug_prikaz, crni_krug_prikaz, tabla)
                UI.crtaj_prikazi_pobednika(prozor, tabla, stranica, potez, prvi_potez_boja, beli_krug if potez == Symbol.B else crni_krug)
                pygame.display.update()

                for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_BACKSPACE:
                                return
                        if event.type == MOUSEBUTTONDOWN:
                            prikazi_pobednika = False
                        elif event.type == QUIT:
                            return
        else:
            return

def pocetni_meni():
    global prozor_visina
    global prozor_sirina
    global start
    global start_prikaz
    global exit
    global exit_prikaz
    global tekst_polje
    global tekst_polje_prikaz
    global precrtano
    global precrtano_prikaz

    dugme_offset_x = start_prikaz.get_width() // 2
    dugme_offset_y = start_prikaz.get_height() // 2
    centar = (prozor_sirina / 2, prozor_visina / 2)

    izbor_pocetni_meni = True
    izbor_velicine_table = False
    izbor_drugi_igrac = False
    izbor_prvi_potez_igrac = False
    izbor_prvi_potez_boja = False

    drugi_igrac_AI = None
    prvi_potez_AI = None
    prvi_potez_boja = None

    while True:
        if prozor_visina != prozor.get_height():
            prozor_visina = prozor.get_height()
            prozor_sirina = prozor.get_width()
            start_prikaz = pygame.transform.scale(start, (int(prozor_sirina * 0.4), int(prozor_visina * 0.2)))
            exit_prikaz = pygame.transform.scale(exit, (int(prozor_sirina * 0.4), int(prozor_visina * 0.2)))
            centar = (prozor_sirina / 2, prozor_visina / 2)
            tekst_polje_prikaz = pygame.transform.scale(tekst_polje,(int(prozor_visina * 0.2), int(prozor_visina * 0.2)))
            precrtano_prikaz = pygame.transform.scale(precrtano, (int(prozor_visina * 0.15), int(prozor_visina * 0.15)))


        prozor.blit(pozadina, (0, 0))
        if izbor_pocetni_meni:
            UI.crtaj_pocetni_meni(prozor, start_prikaz, exit_prikaz)
        elif izbor_drugi_igrac:
            UI.crtaj_izbor_drugi_igrac(prozor, tekst_polje_prikaz, precrtano_prikaz)
        elif izbor_velicine_table:
            UI.crtaj_izbor_velicina_table(prozor, tekst_polje_prikaz)
        elif izbor_prvi_potez_igrac and drugi_igrac_AI is not None and drugi_igrac_AI:
            UI.crtaj_izbor_prvi_potez_igrac(prozor, tekst_polje_prikaz, precrtano_prikaz)
        elif izbor_prvi_potez_boja:
            UI.crtaj_izbor_prvi_potez_boja(prozor, tekst_polje_prikaz, beli_krug, crni_krug)

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                if izbor_pocetni_meni and centar[0] - dugme_offset_x < clickPos[0] < centar[0] + dugme_offset_x and centar[1] - 3 * dugme_offset_y < clickPos[1] < centar[1] - dugme_offset_y:
                    izbor_drugi_igrac = True
                    izbor_pocetni_meni = False
                elif izbor_pocetni_meni and centar[0] - dugme_offset_x < clickPos[0] < centar[0] + dugme_offset_x and centar[1] + dugme_offset_y < clickPos[1] < centar[1] + 3 * dugme_offset_y:
                    return False, -1, drugi_igrac_AI, prvi_potez_AI, prvi_potez_boja
                elif izbor_velicine_table:
                    slika_visina = tekst_polje_prikaz.get_height()
                    slika_sirina = tekst_polje_prikaz.get_width()
                    slika_offset = slika_sirina * 1.1
                    xmin = (prozor.get_width() - 5 * slika_sirina) // 2
                    ymin = (prozor.get_height() - slika_visina) // 2

                    if ymin < clickPos[1] < ymin + slika_visina:
                        for i in range(5):
                            if xmin + i * slika_offset < clickPos[0] < xmin + i * slika_offset + slika_sirina:
                                return True, i, drugi_igrac_AI, prvi_potez_AI, prvi_potez_boja
                elif (prozor.get_height() - tekst_polje_prikaz.get_height()) // 2 < clickPos[1] < (prozor.get_height() + tekst_polje_prikaz.get_height()) // 2:
                    dugme_sirina = tekst_polje_prikaz.get_width()
                    xmin = (prozor.get_width() - 2.4 * dugme_sirina) // 2

                    if xmin < clickPos[0] < xmin + dugme_sirina:
                        if izbor_drugi_igrac:
                            drugi_igrac_AI = False
                            izbor_drugi_igrac = False
                            izbor_prvi_potez_boja = True
                        elif izbor_prvi_potez_igrac:
                            prvi_potez_AI = False
                            izbor_prvi_potez_igrac = False
                            izbor_prvi_potez_boja = True
                        elif izbor_prvi_potez_boja:
                            prvi_potez_boja = Symbol.B
                            izbor_prvi_potez_boja = False
                            izbor_velicine_table = True
                    elif xmin + 1.2 * dugme_sirina < clickPos[0] < xmin + 1.2 * dugme_sirina + dugme_sirina:
                        if izbor_drugi_igrac:
                            drugi_igrac_AI = True
                            izbor_drugi_igrac = False
                            izbor_prvi_potez_igrac = True
                        elif izbor_prvi_potez_igrac:
                            prvi_potez_AI = True
                            izbor_prvi_potez_igrac = False
                            izbor_prvi_potez_boja = True
                        elif izbor_prvi_potez_boja:
                            prvi_potez_boja = Symbol.C
                            izbor_prvi_potez_boja = False
                            izbor_velicine_table = True

            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    return False, -1, drugi_igrac_AI, prvi_potez_AI, prvi_potez_boja
            elif event.type == QUIT:
                return False, -1, drugi_igrac_AI, prvi_potez_AI, prvi_potez_boja

        pygame.display.update()

if __name__ == '__main__':
    main_loop()