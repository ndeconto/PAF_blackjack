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

    def __init__(self, ordre_joueur):
        """
            ordre joueur doit etre la liste des joueurs dans l'ordre
            dans lequel ils doivent jouer
        """

        GUIComponent.__init__(self, 0, (0, 0), (0, 0),
                              [], [], background=None, identifier="arbitre")


        self.jeu_fini = False
        self.liste_joueur = ordre_joueur

        for j in self.liste_joueur:
            print j.playing, j.finish
        


    def terminer_partie(self, couple_gagnant_perdant, other_components):
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
                c.sarreter()



        pause = PauseComponent(K_RETURN, EXIT_GAME_LOOP)


        if couple_gagnant_perdant == None:
            #TODO tester le match nul !!!
            img_draw = ImageComponent(4, (400, 300), "img/draw.png")
            return [self, img_draw, pause]

        gagnant, perdant = couple_gagnant_perdant
        e_bord = 10

        tx, ty = gagnant.background.get_size()
        contour_g = Surface((tx + e_bord, ty + e_bord), SRCALPHA, 32)
        contour_g.fill(Color(90, 230, 255, 255))
        
        tx, ty = perdant.background.get_size()
        contour_p = Surface((tx + e_bord, ty + e_bord), SRCALPHA, 32)
        contour_p.fill(Color(255, 40, 50, 255))

        vide = Surface((0, 0), SRCALPHA, 32)

        pos_cont_g = (gagnant.position[0] - e_bord / 2,
                     gagnant.position[1] - e_bord / 2)

        pos_cont_p = (perdant.position[0] - e_bord / 2,
                      perdant.position[1] - e_bord / 2) 
        
        cache_comp = FlashingImageComponent(.2, pos_cont_g, [contour_g, vide],
                                            0.15)
        cache_comp2 = FlashingImageComponent(.2, pos_cont_p, [contour_p, vide],
                                            0.15)


        
        
        return [self, cache_comp, cache_comp2, pause]


    def trouver_gagnant(self):
        """
            renvoie le couple (gagnant, perdant)
            renvoie None en cas de match nul
            quand cette fonction est appelee, aucun joueur n'a strictement plus de
            21 ; enfin normalement... faire le check serait moins paresseux et
            plus fiable
        """
        g = self.liste_joueur[0].get_m_valeur()
        d = self.liste_joueur[1].get_m_valeur()

        if g > d:
            return (self.liste_joueur[0], self.liste_joueur[1])
        elif d > g:
            return (self.liste_joueur[0], self.liste_joueur[1])
        else: #d == g
            return None


    def update(self, other_components):

        r = GUIComponent.update(self, other_components)

        tout_le_monde_a_fini = True


        for i, j in enumerate(self.liste_joueur):
            if j.playing:
                break
            
            if not j.playing and not j.a_fini():
                j.commencer_tour()
                break

        for i, j in enumerate(self.liste_joueur):

            if not j.a_fini():
                tout_le_monde_a_fini = False

            x = j.get_m_valeur()

            #on verifie qu'aucun joueur n'aie perdu
            if x > 21:
                # ----------- NB : ne marche qu'avec deux joueurs ! -----------
                return self.terminer_partie((self.liste_joueur[1 - i], j),
                                                other_components)


        if tout_le_monde_a_fini:
            return self.terminer_partie(self.trouver_gagnant(),
                                 other_components)


                

        return r

            

            
        
