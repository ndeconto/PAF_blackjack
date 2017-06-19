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

    VICTOIRE_GAUCHE =   1
    VICTOIRE_DROITE =   0
    MATCH_NUL =         -1


    def __init__(self):

        GUIComponent.__init__(self, 0, (0, 0), (0, 0),
                              [], [], background=None, identifier="arbitre")


        self.jeu_fini = False
        


    def terminer_partie(self, cote_gagnant, other_components):
        """
            tue tous les autres composants, ie fait le menage,
            et termine la partie

            cote_gagnant doit valoir VICTOIRE_GAUCHE si le joueur de gauche a
            gagne,
            VICTOIRE_DROITE si le joueur de droite a gagne,
            MATCH_NUL pour un match nul
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
                    (int(tx / 2) if cote_gagnant == self.VICTOIRE_GAUCHE else 0, 0),
                    [cache, vide], 0.15)


        pause = PauseComponent(K_RETURN, EXIT_GAME_LOOP)
        
        return [self, cache_comp, pause]


    def trouver_gagnant(self, joueur_gauche, joueur_droit):
        #quand cette fonction est appelee, aucun joueur n'a strictement plus de
        # 21 ; enfin normalement... faire le check serait moins paresseux et
        # plus fiable
        g = joueur_gauche.get_m_valeur()
        d = joueur_droit.get_m_valeur()

        if g > d:
            return self.VICTOIRE_GAUCHE
        elif d > g:
            return self.VICTOIRE_DROITE
        else: #d == g
            return self.MATCH_NUL


    def update(self, other_components):

        r = GUIComponent.update(self, other_components)

        tout_le_monde_a_fini = True

        for c in other_components:

            if isinstance(c, Joueur):

                w, h = display.get_surface().get_size()

                #joueur gauche ?
                if c.position[0] < w / 2:
                    j_gauche = c
                else :
                    j_droit = c #joueur droit

                if not c.a_fini():
                    tout_le_monde_a_fini = False

                x = c.get_m_valeur()


                #on verifie qu'aucun joueur n'aie perdu
                if x > 21:

                    w, h = display.get_surface().get_size()

                    return self.terminer_partie(int(2 * c.position[0] / w),
                                                other_components)


        if tout_le_monde_a_fini:
            return self.terminer_partie(self.trouver_gagnant(j_gauche, j_droit),
                                 other_components)


                

        return r

            

            
        
