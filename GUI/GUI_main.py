import pygame#, pygame._view
from pygame.locals import *

from GUI_component_manager import *
from GUI_component import *
from GUI_cards_img import*
from GUI_players import *
from GUI_arbitre_bj import *

from GUI_slidemenu import slidemenu

from serveurchaussette import *

import traceback


BOUTON_PIOCHE   = 0
BOUTON_STOP     = 1
BOUTON_SPLIT    = 2
BOUTON_DOUBLE   = 3


def init_GUI():
    
    pygame.font.init(); pygame.display.init()
    pygame.display.set_mode((1000, 712), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption("Men in Blackjack - Joueur Humain")

    #TODO mettre une icone


def lauch_server(pioche):

    return Serveur(5000, "localhost", pioche)


def stop_button_action(joueur_humain, button_list):
    def f():
        joueur_humain.sarreter()

        #attention avec le split le joueur n'a pas forcement fini !!
        if joueur_humain.a_fini():
            for b in button_list:
                b.desactiver()
    return f


def double_button_action(mise, joueur, button_list):
    def f():
        mise.doubler()
        joueur.do_in_x_seconds(1, joueur.piocher)
        joueur.do_in_x_seconds(2, joueur.sarreter)
        for b in button_list:
            b.desactiver()
    return f


def split_button_action(button_list, joueur):

    def f():
        j = joueur.splitter()
        
        button_list[BOUTON_DOUBLE].desactiver()
        button_list[BOUTON_SPLIT].desactiver()

    return f
    



def jeu(type_jeu):

    global serveur

    X_PREMIER_BOUTON = 150
    D_X_BOUTON = 200
    Y_BOUTON = 670

    POS_J_GAUCHE = (125, 250)
    POS_J_DROITE = (735, 250)


    # ---------- creation des composants de la GUI -------- #

    
    tapis = ImageComponent(0, (0, 0),
                "img/tapis_bj_new.png" if type_jeu in [JEU_CLASSIQUE, IA_VS_BANQUE]
                else "img/tapis_bj_vs_ordi.png")

    pioche = DeckGraphique((422, 330))

    if type_jeu == JEU_SYMETRIQUE:
        serveur = lauch_server(pioche)

    mise = Mise(1, (0, 0), 35, font_color=(219, 201, 101))

    if type_jeu == JEU_CLASSIQUE:
        
        joueur_1 = JoueurHumain((125, 250), pioche, identifier="humain")
        joueur_2 = Banque(POS_J_DROITE, pioche)


    elif type_jeu == JEU_SYMETRIQUE:

        joueur_1 = JoueurHumain(POS_J_GAUCHE, pioche, identifier="humain")
        serveur.set_opponent_card(joueur_1.contenu[1])
        joueur_2 = JoueurDistant(POS_J_DROITE, serveur_local=serveur)
        
        
    elif type_jeu == IA_VS_BANQUE:

        joueur_2 = Banque(POS_J_DROITE, pioche)
        joueur_1 = JoueurOrdi(POS_J_GAUCHE, pioche, mise, identifier="ia",
                              face_cachee=[])
        joueur_1.commencer_tour()
        

    arbitre = Arbitre([joueur_1, joueur_2], type_jeu, mise)  


    if type_jeu == JEU_CLASSIQUE or type_jeu == JEU_SYMETRIQUE:

        button_list = []
        
        #TODO : mettre les boutons en anglais !
        bouton_piocher = Bouton(2, (X_PREMIER_BOUTON, Y_BOUTON),
                            "img/bouton_piocher.png",
                            joueur_1.piocher)

        bouton_stop = Bouton(2, (X_PREMIER_BOUTON + D_X_BOUTON, Y_BOUTON),
                         "img/bouton_stop.png",
                         stop_button_action(joueur_1, button_list))

        bouton_split = Bouton(2, (X_PREMIER_BOUTON + 2 * D_X_BOUTON, Y_BOUTON),
                          "img/bouton_split.png",
                              split_button_action(button_list, joueur_1))

        bouton_double = Bouton(2, (X_PREMIER_BOUTON + 3 * D_X_BOUTON, Y_BOUTON),
                           "img/bouton_double.png",
                           double_button_action(mise, joueur_1, button_list))

        button_list.extend([bouton_piocher, bouton_stop, bouton_split,
                            bouton_double])

    


    # ---------- on donne tous les composants a un manager ------------ #
    # le manager se debrouille avec tout ca et fait sa cuisine
    liste_comp = [tapis, mise, joueur_1, joueur_2, pioche, arbitre]

    if type_jeu == JEU_SYMETRIQUE:
        #s'assurer que arbitre.liste_joueur[0] est bien le joueur humain
        r = GUIComponentManager([ImageComponent(0, (0, 0), "img/wait_client.png"),
                    WaitForTrueComponent(lambda: serveur.a_un_client, EXIT_GAME_LOOP)],
                    5).run()

        if r == CLOSE_WINDOW:
            return r
                     
        liste_comp.append(ServeurManager(serveur,joueur_1))
    
    if type_jeu == JEU_CLASSIQUE or type_jeu == JEU_SYMETRIQUE:
        liste_comp += [bouton_piocher, bouton_stop, bouton_split, bouton_double]
    
    game_manager = GUIComponentManager(liste_comp, 20)

    r = game_manager.run()
    if type_jeu == JEU_SYMETRIQUE: serveur.close_server()
    sleep(.3)
    return r


def main():


    m, t = slidemenu(['IA against dealer::the AI will play against the dealer',
                      'classic game::play against the dealer',
                      'symetric game::play against an other player',
                      '',
                      'rules::click here to learn the rules',
                      #'re-show::click here to show again',
                      'quit::good bye'])

    
    # ----------   intialisation  ----------------- #
    init_GUI()
    init_lib_cartes()

    if t == 0:
        r = jeu(IA_VS_BANQUE)
    elif t == 1:
        r = jeu(JEU_CLASSIQUE)
    elif t == 2:
        r = jeu(JEU_SYMETRIQUE)
    elif t == 4:
        quit()
        return

    if t == 2: serveur.close_server()
    sleep(.2)

    if r == EXIT_GAME_LOOP:
        main()


    
    pygame.quit()


if __name__ == "__main__" :
    try :
        main()
        serveur.close_server()

    except Exception as e:
        
        print (traceback.format_exc())

        raise (e)

    finally:
        serveur.close_server()






