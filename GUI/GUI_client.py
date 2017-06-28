import pygame#, pygame._view
from pygame.locals import *

from GUI_component_manager import *
from GUI_component import *
from GUI_cards_img import*
from GUI_players import *
from GUI_arbitre_bj import *

from GUI_slidemenu import slidemenu


from sys import path
path.append('..')
from clientchaussette import *


def init_GUI():
    
    pygame.font.init(); pygame.display.init()
    pygame.display.set_mode((1000, 712), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption("Blackjack")

    #TODO mettre une icone


def jeu():

    POS_J_GAUCHE = (125, 250)
    POS_J_DROITE = (735, 250)

    # ---------- creation des composants de la GUI -------- #

    
    tapis = ImageComponent(0, (0, 0), "img/tapis_bj_vs_ordi.png")

    pioche = DeckGraphique((422, 330)) #juste pour decorer

    mise = Mise(1, (0, 0), 35, font_color=(219, 201, 101))


    joueur_1 = JoueurDistant(POS_J_GAUCHE)
    joueur_2 = JoueurOrdi(POS_J_DROITE, None, mise, face_cachee=[])

    arbitre = Arbitre([joueur_2, joueur_1], JEU_SYMETRIQUE, mise)
    


    # ---------- on donne tous les composants a un manager ------------ #
    # le manager se debrouille avec tout ca et fait sa cuisine

    #TODO rajouter un arbitre special
    liste_comp = [tapis, mise, joueur_1, joueur_2, pioche, arbitre]
    
    game_manager = GUIComponentManager(liste_comp, 20)

    return game_manager.run()



def main():

    init_GUI()
    init_lib_cartes()

    jeu()

if __name__ == "__main__":
    main()

    






