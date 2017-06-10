import pygame#, pygame._view
from pygame.locals import *

from GUI_component_manager import *
from GUI_component import *




def main():
    
    pygame.font.init(); pygame.display.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((500, 356), HWSURFACE | DOUBLEBUF)


    img_tapis = pygame.image.load("img/tapis_blackjack.png").convert_alpha()
    

    
    tapis = GUIComponent(0, (0, 0), img_tapis.get_size(), [], [], img_tapis)
        
    game_manager = GUIComponentManager([tapis], 1)

    game_manager.run()

    pygame.quit()


main()






