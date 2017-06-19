import pygame#, pygame._view
from pygame.locals import *

from GUI_component_manager import *
from GUI_component import *
from GUI_cards_img import*
from GUI_players import *
from GUI_arbitre_bj import *

from GUI_slidemenu import slidemenu


def init_GUI():
    
    pygame.font.init(); pygame.display.init()
    pygame.display.set_mode((1000, 712), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption("Blackjack")

    #TODO mettre une icone


def stop_button_action(joueur_humain, joueur_ordi):
    def f():
        joueur_humain.sarreter()
        joueur_ordi.commencer_tour()
    return f



def jeu_un_joueur():

    X_PREMIER_BOUTON = 150
    D_X_BOUTON = 200
    Y_BOUTON = 670


    # ---------- creation des composants de la GUI -------- #

    
    tapis = ImageComponent(0, (0, 0), "img/tapis_bj_new.png")

    pioche = DeckGraphique((422, 330))

    joueur_humain = JoueurHumain((125, 250), pioche, "humain")
    joueur_ordi = JoueurOrdi((735, 250), pioche, "IA")

    arbitre = Arbitre()


    bouton_piocher = Bouton(2, (X_PREMIER_BOUTON, Y_BOUTON),
                            "img/bouton_piocher.png",
                            joueur_humain.piocher)

    bouton_stop = Bouton(2, (X_PREMIER_BOUTON + D_X_BOUTON, Y_BOUTON),
                         "img/bouton_stop.png",
                         stop_button_action(joueur_humain, joueur_ordi))

    bouton_split = Bouton(2, (X_PREMIER_BOUTON + 2 * D_X_BOUTON, Y_BOUTON),
                          "img/bouton_split.png",
                          lambda : None)

    bouton_double = Bouton(2, (X_PREMIER_BOUTON + 3 * D_X_BOUTON, Y_BOUTON),
                           "img/bouton_double.png",
                           lambda : None)

    
    


    # ---------- on donne tous les composants a un manager ------------ #
    # le manager se debrouille avec tout ca et fait sa cuisine
    game_manager = GUIComponentManager([tapis, joueur_humain, joueur_ordi,
                                        pioche, bouton_piocher, bouton_stop,
                                        arbitre, bouton_split, bouton_double],
                                       20)

    game_manager.run()


def main():


    m, t = slidemenu(['one player',
                'two players',
                '',
                'options',
                're-show::click here to show again',
                'quit::good bye'])

    if t == 4:
        quit()
        return

    
    # ----------   intialisation  ----------------- #
    init_GUI()
    init_lib_cartes()


    #
    jeu_un_joueur()


    
    pygame.quit()


if __name__ == "__main__" :
    main()






