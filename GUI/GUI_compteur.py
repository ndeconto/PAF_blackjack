from pygame import *
from pygame.locals import *

from GUI_component import*
from GUI_arbitre_bj import*
from GUI_component_manager import *

from sys import path
path.append('..')
from compteur import read_total


font.init(); display.init()
display.set_mode((550, 100), HWSURFACE | DOUBLEBUF)
display.set_caption("Men in Blackjack - Compteur")


class MonCompteur(TextComponent):

    def update(self, o_c):
        x, n = read_total()
        if x == int(x): x = int(x)
        self.texte = "GAINS : " + str(x) + " / " + str(n)
        display.get_surface().fill((0, 0, 0))

        TextComponent.update(self, o_c)
        return [self]



mon_compteur = MonCompteur(1, (10, 20), " ", 70, font_color=(255, 128, 25),
                     enable_bg=True)
GUIComponentManager([mon_compteur], 3).run() 

quit()


    
