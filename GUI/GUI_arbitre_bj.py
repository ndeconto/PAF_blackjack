from pygame import *

from GUI_component import *
from GUI_players import *
from GUI_component_manager import EXIT_GAME_LOOP


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


        self.jeu_fini = False
        


    def terminer_partie(self, cote_gagnant, other_components):
        """
            tue tous les autres composants, ie fait le menage,
            et termine la partie

            cote_gagnant doit valoir 1 si le joueur de gauche a gagne,
            0 sinon
        """

        if self.jeu_fini : return [self]
        self.jeu_fini = True
        
        for c in other_components :


            if isinstance(c, Bouton):
                c.desactiver()


            if isinstance(c, JoueurOrdi):
                c.arreter_tour()


        tx, ty = display.get_surface().get_size()
        cache = Surface((int(tx / 2), ty), SRCALPHA, 32)
        cache.fill(Color(255, 0, 0, 120))

        vide = Surface((int(tx / 2), ty), SRCALPHA, 32)
        vide.fill(Color(0, 0, 0, 0))
        
        cache_comp = FlashingImageComponent(3,
                                            (int(tx / 2) if cote_gagnant == 1
                                             else 0, 0),
                                            [cache, vide], 0.15)


        pause = PauseComponent(K_RETURN, EXIT_GAME_LOOP)
        
        return [self, cache_comp, pause]

            


    def update(self, other_components):

        r = GUIComponent.update(self, other_components)

        for c in other_components:

            if isinstance(c, Joueur):

                x = c.get_m_valeur()
                
                if x > 21:

                    w, h = display.get_surface().get_size()

                    return self.terminer_partie(int(2 * c.position[0] / w),
                                                other_components)

        return r

            

            
        
