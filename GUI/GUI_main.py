import pygame#, pygame._view
from pygame.locals import *

from GUI_component_manager import *
from GUI_component import *
from GUI_cards_img import*




def main():
    
    pygame.font.init(); pygame.display.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((1000, 712), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption("Blackjack")

    charger_img()

    
    tapis = ImageComponent(0, (0, 0), "img/tapis_blackjack_big.png")
    main_joueur = MainGraphique([Carte(i, CARREAU) for i in range(1, 14)],
                                (150, 300), HORIZONTAL, "main du joueur")
    
    game_manager = GUIComponentManager([tapis, main_joueur], 10)

    game_manager.run()

    pygame.quit()


if __name__ == "__main__" :
    main()






