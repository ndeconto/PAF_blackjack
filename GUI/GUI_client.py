import pygame#, pygame._view
from pygame.locals import *


import sys
sys.path.append('..')

from GUI_component_manager import *
from GUI_component import *
from GUI_cards_img import*
from GUI_players import *
from GUI_arbitre_bj import *

from GUI_slidemenu import slidemenu



#la fonction de decision qui va etre utilisee pour jouer
from decision_method_list import makeBestDecision


from sys import path
path.append('..')
from clientchaussette import *

from serveurchaussette import IP_SERVEUR, PORT


def init_GUI():
    
    pygame.font.init(); pygame.display.init()
    pygame.display.set_mode((1000, 712), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption("Men in Blackjack - Ordinateur")
    pygame.display.set_icon(pygame.image.load("img/icone.png"))

    #TODO mettre une icone


def jeu():

    POS_J_GAUCHE = (125, 250)
    POS_J_DROITE = (735, 250)

    # ---------- creation des composants de la GUI -------- #

    
    tapis = ImageComponent(0, (0, 0), "img/tapis_bj_vs_ordi.png")

    pioche = DeckGraphique((422, 330)) #juste pour decorer

    mise = Mise(1, (0, 0), 35, font_color=(219, 201, 101))


    client_bidon = Client(PORT, IP_SERVEUR)
    #attente d'avoir un serveur dispo
    r = GUIComponentManager([ImageComponent(0, (0, 0), "img/wait_serveur.png"),
                    WaitForTrueComponent(client_bidon.server_up, EXIT_GAME_LOOP)],
                    5).run()

    if r == CLOSE_WINDOW:
        return r

    sleep(1)


    joueur_1 = JoueurDistant(POS_J_GAUCHE)
    joueur_2 = JoueurOrdi(POS_J_DROITE, None, mise,
                          fct_decision=makeBestDecision,
                          face_cachee=[], regle="sym")

    arbitre = Arbitre([joueur_2, joueur_1], JEU_SYMETRIQUE, mise,
                      cote_serveur=False)
    


    # ---------- on donne tous les composants a un manager ------------ #
    # le manager se debrouille avec tout ca et fait sa cuisine

    liste_comp = [tapis, mise, joueur_1, joueur_2, pioche, arbitre]

    
    
    game_manager = GUIComponentManager(liste_comp, 20)

    return game_manager.run()



def main():

    init_GUI()
    init_lib_cartes()

    while jeu() != CLOSE_WINDOW:
        pass

    pygame.quit()

if __name__ == "__main__":
    main()

    






