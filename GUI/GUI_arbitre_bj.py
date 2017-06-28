# -*- coding: utf-8 -*-
from pygame import *

from GUI_component import *
from GUI_players import *
from GUI_component_manager import EXIT_GAME_LOOP

from sys import path
path.append('..')
from prise_2_decision import win2, win_split
from prise_3_decision import compute_result

JEU_CLASSIQUE   =   0   #un joueur humain joue contre la banque
IA_VS_BANQUE    =   1   #l'IA joue contre la banque (l'humain n'est que spectateur)
JEU_SYMETRIQUE  =   2   #notre jeu special, avec les regles symetrisees


class Arbitre(GUIComponent):

    """
        l'arbitre est le composant qui gere la partie en respectant les regles
        du blackjack
        c'est lui qui determine quand la partie est finie,
        qui donne la liste des cartes visibles aux autres joueurs,
        qui donne l'historique des cartes passees, ...
    """

    def __init__(self, ordre_joueur, type_jeu, mise):
        """
            ordre joueur doit etre la liste des joueurs dans l'ordre
            dans lequel ils doivent jouer

            type_jeu doit imperativement etre l'une des constantes definies
            plus haut (JEU_CLASSIQUE, ...)

            mise doit etre une instance de la classe Mise !
        """

        GUIComponent.__init__(self, 0, (0, 0), (0, 0),
                              [], [], background=None, identifier="arbitre")


        self.jeu_fini = False
        self.liste_joueur = ordre_joueur

        self.type_jeu = type_jeu
        self.mise = mise



    def update_total_des_gains(self, nouveau_gain):
        #TODO une fonction qui ouvre un fichier et qui met a jour la somme des
        #gains realises sur l'ensemble des parties
        return
        


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

            #cette condition est douteuse... on ne devrait pas avoir a faire ca
            if isinstance(c, JoueurOrdi) and not c.finish:
                c.sarreter()


        for j in self.liste_joueur:
            j.set_face_cachee([])



        pause = PauseComponent(K_RETURN, EXIT_GAME_LOOP)


        if couple_gagnant_perdant == None:
            #TODO c'est pas hyper beau...
            img_draw = ImageComponent(4, (350, 300), "img/draw.png")
            return [self, img_draw, pause]

        l_gagnant, l_perdant = couple_gagnant_perdant
        e_bord = 10
        vide = Surface((0, 0), SRCALPHA, 32)

        comp_finaux = [self, pause]

        

        for gagnant in l_gagnant :

            print "gagnant", gagnant, type(gagnant)

            tx, ty = gagnant.background.get_size()

            contour_g = Surface((tx + e_bord, ty + e_bord), SRCALPHA, 32)
            contour_g.fill(Color(90, 230, 255, 255))
            

            pos_cont_g = (gagnant.position[0] - e_bord / 2,
                         gagnant.position[1] - e_bord / 2)

            comp_finaux.append(FlashingImageComponent(.2, pos_cont_g, [contour_g, vide],
                                            0.15))

            

        for perdant in l_perdant:

            print "perdant", perdant, type(perdant)
            
            tx, ty = perdant.background.get_size()
            contour_p = Surface((tx + e_bord, ty + e_bord), SRCALPHA, 32)
            contour_p.fill(Color(255, 40, 50, 255))

            pos_cont_p = (perdant.position[0] - e_bord / 2,
                          perdant.position[1] - e_bord / 2) 
        
            comp_finaux.append(FlashingImageComponent(.2, pos_cont_p, [contour_p, vide],
                                            0.15))


        
        
        return comp_finaux


    def trouver_gagnant(self):
        """
            renvoie le couple (liste_des_gagnants, liste_des_perdants)
            renvoie None en cas de match nul
        """

        #liste des joueurs qui ont splitte
        l_split = [j for j in self.liste_joueur if j.a_splite]
        #liste des joueurs qui n'ont pas splitte
        l_n_split = [j for j in self.liste_joueur if not j.a_splite]
                
        if self.type_jeu == JEU_CLASSIQUE or self.type_jeu == IA_VS_BANQUE:

            #si personne n'a splitte
            if len(l_split) == 0:

                #NB : joueur 2 a l'avantage de l'asymetrie (c'est la banque)
                print len(self.liste_joueur[0]), len(self.liste_joueur[1])
                r = win2(self.liste_joueur[0], self.liste_joueur[1],
                         self.mise.get_value())

                lj_1  = [self.liste_joueur[0]]
                lj_2 = [self.liste_joueur[1]]

            else:
                #la banque ne pouvant pas splitter, on doit etre dans le cas
                # nb_split == 1
                assert(len(l_split) == 1)

                r = win_split(l_split[0].jeu_1, l_split[0].jeu_2, l_n_split[0], 1)

                lj_1 = [l_split[0].jeu_1, l_split[0].jeu_2]
                lj_2 = [l_n_split[0]]


            self.update_total_des_gains(r)
            draw = (r == 0)

            lg = []
            lp = []

            for j1 in lj_1:
                for j2 in lj_2:

                    r = win2(j1, j2, 1)

                    if r > 0:
                        lg.append(j1)
                        lp.append(j2)

                    elif r < 0:
                        lg.append(j2)
                        lp.append(j1)

            if draw:
                return None

            return (lg, lp)
                

        elif self.type_jeu == JEU_SYMETRIQUE:

            assert (self.liste_joueur[0].a_fini)
            assert (self.liste_joueur[1].a_fini)

            j0 = self.liste_joueur[0]
            j1 = self.liste_joueur[1]

            main_0 = (j0 if not j0.a_splite else [j0.jeu_1, j0.jeu_2])
            main_1 = (j1 if not j1.a_splite else [j1.jeu_1, j1.jeu_2])

            print main_0, main_1

            #du point de vue de j0   
            gain = compute_result(main_0, j0.a_double, j0.a_splite,
                                  main_1, j1.a_double, j1.a_splite,
                                  1)    #--- la mise est toujours unitaire --------

            if gain > 0:
                return ([main_0], [main_1]) 
            elif gain < 0:
                return ([main_1], [main_0])
            else: #match nul
                return None
                

        else:
            raise (ValueError("le type de jeu " + str(self.type_jeu) +
                              "n'est pas reconnu par la fonction de gain"))


    def update(self, other_components):

        r = GUIComponent.update(self, other_components)

        tout_le_monde_a_fini = True

        if self.jeu_fini:
            return r

        
        for i, j in enumerate(self.liste_joueur):
            
            if j.playing:
                break
            
            if not j.playing and not j.a_fini():
                j.commencer_tour()
                break
            

        for i, j in enumerate(self.liste_joueur):

            if not j.a_fini():
                tout_le_monde_a_fini = False

            #oquand on joue contre la banque, celle ci s'arrete quand un joueur perd
            if ((self.type_jeu == JEU_CLASSIQUE
                or self.type_jeu == IA_VS_BANQUE) and j.a_perdu()):
                # ----------- NB : ne marche qu'avec deux joueurs ! -----------

                self.liste_joueur[-1].sarreter()
                #return self.terminer_partie(([self.liste_joueur[1 - i]], [j]),
                #                                other_components)


            


        if tout_le_monde_a_fini:
            return self.terminer_partie(self.trouver_gagnant(),
                                 other_components)


                

        return r

            

            
        
