import pygame#, pygame._view
from pygame.locals import *

from GUI_component_manager import *
from GUI_component import *
from GUI_cards_img import*



def init_GUI():
    
    pygame.font.init(); pygame.display.init()
    pygame.display.set_mode((1000, 712), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption("Blackjack")

    #TODO mettre une icone


def main():
    
    
    init_GUI()
    init_lib_cartes()

    
    tapis = ImageComponent(0, (0, 0), "img/tapis_blackjack_big.png")

    pioche = DeckGraphique((10, 10))

    main_banque = MainGraphique([pioche.piocher() for i in range(2)], (700, 10),
                                face_cachee = [0])

    
    main_joueur = MainGraphique([pioche.piocher() for i in range(2)],
                                (150, 300), HORIZONTAL, "main du joueur")

    
    
    game_manager = GUIComponentManager([tapis, main_joueur, pioche, main_banque], 20)

    game_manager.run()

    pygame.quit()


if __name__ == "__main__" :
    main()






