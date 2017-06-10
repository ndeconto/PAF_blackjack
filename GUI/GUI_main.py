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
    

    img_tapis = pygame.image.load("img/tapis_blackjack_big.png").convert_alpha()
    img_main = get_img(Main([Carte(i, COEUR) for i in range(1, 14)]),
                       sens=HORIZONTAL)

    
    tapis = GUIComponent(0, (0, 0), img_tapis.get_size(), [], [], img_tapis)
    as_de_coeur = GUIComponent(1, (150, 300), img_main.get_size(), [], [], img_main)
        
    game_manager = GUIComponentManager([tapis, as_de_coeur], 10)

    game_manager.run()

    pygame.quit()


if __name__ == "__main__" :
    main()






