import pygame#, pygame._view
from pygame.locals import *

from GUI_component_manager import *
from GUI_component import *
from GUI_cards_img import*
from GUI_players import *
from GUI_arbitre_bj import *

from GUI_slidemenu import slidemenu

JEU_CLASSIQUE   =   0   #un joueur humain joue contre la banque
IA_VS_BANQUE    =   1   #l'IA joue contre la banque (l'humain n'est que spectateur)
JEU_SYMETRIQUE  =   2   #notre jeu special, avec les regles symetrisees



def init_GUI():
    
    pygame.font.init(); pygame.display.init()
    pygame.display.set_mode((1000, 712), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption("Blackjack")

    #TODO mettre une icone


def stop_button_action(joueur_humain, button_list):
    def f():
        joueur_humain.sarreter()
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



def jeu(type_jeu):

    X_PREMIER_BOUTON = 150
    D_X_BOUTON = 200
    Y_BOUTON = 670

    POS_J_GAUCHE = (125, 250)
    POS_J_DROITE = (735, 250)


    # ---------- creation des composants de la GUI -------- #

    
    tapis = ImageComponent(0, (0, 0), "img/tapis_bj_new.png")

    pioche = DeckGraphique((422, 330))

    mise = Mise(1, (0, 0), 35, font_color=(219, 201, 101))

    if type_jeu == JEU_CLASSIQUE:
        
        joueur_1 = JoueurHumain((125, 250), pioche, "humain")
        joueur_2 = Banque(POS_J_DROITE, pioche)


    elif type_jeu == JEU_SYMETRIQUE:

        joueur_1 = JoueurHumain((125, 250), pioche, "humain")
        joueur_2 = None #TODO definir cette variable !!
        
        
    elif type_jeu == IA_VS_BANQUE:

        joueur_2 = Banque(POS_J_DROITE, pioche)
        joueur_1 = JoueurOrdi(POS_J_GAUCHE, pioche, identifier="ia")
        joueur_1.commencer_tour()
        

    arbitre = Arbitre([joueur_1, joueur_2])


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
                          lambda : None)

        bouton_double = Bouton(2, (X_PREMIER_BOUTON + 3 * D_X_BOUTON, Y_BOUTON),
                           "img/bouton_double.png",
                           double_button_action(mise, joueur_1, button_list))

        button_list.extend([bouton_piocher, bouton_stop, bouton_split,
                            bouton_double])

    


    # ---------- on donne tous les composants a un manager ------------ #
    # le manager se debrouille avec tout ca et fait sa cuisine
    liste_comp = [tapis, mise, joueur_1, joueur_2, pioche, arbitre]
    
    if type_jeu == JEU_CLASSIQUE or type_jeu == JEU_SYMETRIQUE:
        liste_comp += [bouton_piocher, bouton_stop, bouton_split, bouton_double]
    
    game_manager = GUIComponentManager(liste_comp, 20)

    return game_manager.run()


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


    if r == EXIT_GAME_LOOP:
        main()


    
    pygame.quit()


if __name__ == "__main__" :
    main()






