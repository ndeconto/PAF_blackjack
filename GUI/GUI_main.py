import pygame#, pygame._view
from pygame.locals import *

from GUI_component_manager import *
from GUI_component import *
from GUI_cards_img import*
from GUI_players import *
from GUI_arbitre_bj import *


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

def main():


    
    # ----------   intialisation  ----------------- #
    init_GUI()
    init_lib_cartes()




    # ---------- creation des composants de la GUI -------- #

    
    tapis = ImageComponent(0, (0, 0), "img/tapis_blackjack_big.png")

    pioche = DeckGraphique((10, 10))

    joueur_humain = JoueurHumain((150, 300), pioche, "humain")
    joueur_ordi = JoueurOrdi((700, 10), pioche, "IA")

    arbitre = Arbitre()


    bouton_piocher = Bouton(2, (500, 200), "img/bouton_piocher.png",
                            joueur_humain.piocher)

    bouton_stop = Bouton(2, (600, 300), "img/bouton_stop.png",
                         stop_button_action(joueur_humain, joueur_ordi))

    



    # ---------- on donne tous les composants a un manager ------------ #
    # le manager se debrouille avec tout ca et fait sa cuisine
    game_manager = GUIComponentManager([tapis, joueur_humain, joueur_ordi,
                                        pioche, bouton_piocher, bouton_stop,
                                        arbitre],
                                       20)

    game_manager.run()

    pygame.quit()


if __name__ == "__main__" :
    main()






