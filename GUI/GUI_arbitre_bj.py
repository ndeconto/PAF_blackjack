from pygame import *

from GUI_component import *
from GUI_players import *
from GUI_component import *


class Arbitre(GUIComponent):

    """
        l'arbitre est le composant qui gere la partie en respectant les regles
        du blackjack
        c'est lui qui determine quand la partie est finie,
        qui donne la liste des cartes visibles aux autres joueurs,
        qui donne l'historique des cartes passees, ...
    """


    def __init__(self):

        GUIComponent.__init__(self, 0, (0, 0), (0, 0),
                              [], [], background=None, identifier="arbitre")
        


    def terminer_partie(self, other_components):
        """
            tue tous les autres composants, ie fait le menage,
            et termine la partie
        """

        for c in other_components :


            if isinstance(c, Bouton):
                c.desactiver()


            if isinstance(c, JoueurOrdi):
                c.arreter_tour()
            
        return [self]

            


    def update(self, other_components):

        r = GUIComponent.update(self, other_components)

        for c in other_components:

            if isinstance(c, Joueur):

                if all(x > 21 for x in c.valeur):

                    return self.terminer_partie(other_components)

        return r

            

            
        
