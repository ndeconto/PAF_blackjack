# -*- coding: utf-8 -*-
from pygame import *
from pygame.locals import *
from sys import path
path.append("..")
import Prise_De_Decision as pdd

from time import clock, sleep

from GUI_cards_img import *

from serveurchaussette import IP_SERVEUR, PORT
from clientchaussette import Client, piocher_bloquant


class Arbitrable:

    def __init__(self):
        
        #si le joueur a commence son tour
        self.playing = False

        #si le joueur a fini de joueur
        self.finish = False

        #si le joueur a splitte
        self.a_splite = False

        #si le joueur a double
        self.a_double = False


    def a_fini(self):
        """
            renvoie vrai si le joueur a terminer son tour (ie il s'est arrete)
            faux s'il va encore effectuer des actions
        """

        return self.finish


    def commencer_tour(self):
        self.playing = True

    

class Joueur(MainGraphique, Arbitrable):
    """
        objet graphique representant un joueur, ie sa main et ses actions de jeu
    """


    def __init__(self, position, pioche, sens, mise, identifier="",
                 carte_ini=[], face_cachee=[]):
        """
            cf Banque pour les parametres...
            carte_ini represente la main initiale du joueur : [] pour piocher
            automatiquement 2 cartes, preciser les cartes sinon
        """

        MainGraphique.__init__(self,
                               [pioche.piocher(), pioche.piocher()] if carte_ini == []
                               else carte_ini,
                               position, sens=sens, identifier=identifier,
                               face_cachee=face_cachee)

        Arbitrable.__init__(self)


        self.pioche = pioche
        self.mise = mise
        
        self.joueur_split = None


    def a_perdu(self):
        if not self.a_splite:
            return self.get_m_valeur() > 21
        return self.jeu_1.a_perdu() and self.jeu_2.a_perdu()


    def piocher(self):
        """
            pioche une carte dans la pioche et la rajoute dans la main
        """
        if not self.a_splite:
            self.ajouter(self.pioche.piocher())

        else :
            
            if self.jeu_1.playing: self.jeu_1.piocher()
            else:
                
                self.jeu_2.piocher()


    def doubler(self):
        self.mise.doubler()
        self.a_double = True


    def sarreter(self):
        """
            pour terminer son tour
        """
        if not self.a_splite:
            self.playing = False
            self.finish = True

        else :
            if self.jeu_1.playing:
                self.jeu_1.sarreter()
                self.jeu_2.commencer_tour()

            else:
                self.jeu_2.sarreter()


            self.maj_play_and_finish()



    def maj_play_and_finish(self):
        
        self.playing = self.jeu_1.playing or self.jeu_2.playing
        self.finish = self.jeu_1.finish and self.jeu_2.finish
        

    def splitter(self):

        if self.a_splite: return     #split impossible
        
        self.a_splite = True

        DX = TX / 1.7 #ou TX est la taille des cartes en X
        DY = 0

        x, y = self.position

        self.jeu_1 = Joueur((x - DX, y + DY), self.pioche, VERTICAL, self.mise,
                            identifier=self.id+"split_1", carte_ini=[self[0]])

        self.jeu_2 = Joueur((x + DX, y + DY), self.pioche, VERTICAL, self.mise,
                            identifier=self.id+"split_2", carte_ini=[self[1]])

        self.jeu_1.commencer_tour()
    


    def display(self):

        if not self.a_splite:
            MainGraphique.display(self)

        else :
            self.jeu_1.display()
            return self.jeu_2.display()

    


    def update(self, other_comp):

        if self.a_perdu() and not self.finish:
            self.sarreter()
        
        if not self.a_splite:
            self.encircling_enable = self.playing
            MainGraphique.update(self, other_comp)
            
        else:
            self.jeu_1.update(other_comp)
            self.jeu_2.update(other_comp)

            self.maj_play_and_finish()

            #print self.playing, self.jeu_1.playing, self.jeu_2.playing

        return [self]


    def manage_event(self, ev_list):
        if self.a_splite:
            self.jeu_1.manage_event(ev_list)
            self.jeu_2.manage_event(ev_list)
            return CONTINUE

        return MainGraphique.manage_event(self, ev_list)
        


class JoueurHumain(Joueur):


    def __init__(self, position, pioche, identifier=""):

        Joueur.__init__(self, position, pioche, VERTICAL, identifier)

        
        self.bouton_pioche = None
        self.bouton_stop = None


    def piocher(self):

        if not self.finish:
            Joueur.piocher(self)


    def sarreter(self):
        if not self.finish:
            Joueur.sarreter(self)
            

class JoueurOrdi(Joueur):


    def __init__(self, position, pioche, mise, identifier="",
                 fct_decision=None, face_cachee=[0]):
        """
            pioche:
                soit un Deck soit None
                None signifie que la pioche est distance, ie la classe va
                demander les a un serveur. cf serveurchaussette pour l'adresse
                ip et le port associes a la communication
                
            fct_decision : fonction qui est appelee pour decider quoi jouer
            cette fonction doit prendre en parametre la main du joueur ordi,
            la carte de l'adversaire et la liste des cartes deja tombees
            et renvoyer l'une des constantes pdd.CONTINUER, ...

            pour les autres parametres, c'est comme pour le reste...
        """

        #c'est mal d'instancier Joueur avec une pioche None
        #car Joueur ne gere pas la pioche distante
        #pour faire les choses vraiment bien, il faudrait en effet gerer
        #la pioche distante dans Joueur
        #mais cela complique, et nous n'en avons pas besoin... 
        if pioche == None:
            self.client = Client(PORT, IP_SERVEUR)
            c1 = piocher_bloquant(self.client)
            c2 = piocher_bloquant(self.client)
        
        Joueur.__init__(self, position, pioche, VERTICAL, mise,
                        identifier=identifier,
                        carte_ini= [] if pioche != None else [c1, c2],
                        face_cachee=face_cachee)

        self.pioche_valide = True
            
        

        #temps entre deux decisions en secondes
        self.period = 1
        self.derniere_action = clock()

        #
        if fct_decision == None: self.fct_decision = pdd.decision_banque
        else : self.fct_decision = fct_decision

    

    def update(self, other_components):
        r = Joueur.update(self, other_components)
        
        if self.finish:
            return r


        #tant qu'on n'a pas encore reussi a piocher la carte qu'on devait piocher
        #on reessaie.

        #print self.pioche_valide, self.playing, clock() - self.derniere_action > self.period
        
        if not self.pioche_valide:

            
            self.piocher()

        
            
        #sinon on peut se permettre de faire d'autres choses
        elif self.playing and (clock() - self.derniere_action > self.period):

            #TODO : demander les infos sur les cartes de l'adversaires, et sur les
            #cartes passees ici !!
            #ci dessous un exemple bidon juste pour tester
            #car de toute facon, pour l'instant, l'historique n'entre pas en compte
            #dans la decision
            carte_adversaire = Carte(AS, PIQUE)
            l_cartes_passees = [] #TODO il faudra peut etre un historique
                                # plus sophistique (peut on doubler / splitter ... )
        
            self.jouer(carte_adversaire, l_cartes_passees)

            self.derniere_action = clock()


        return r


    def piocher(self):
        if self.pioche != None: #si on pioche en local
            Joueur.piocher(self)
            self.pioche_valide = True

        else :

            c = self.client.has_drawn()
            
            if c[0]:
                Joueur.piocher(c[1]) 
                self.pioche_valide = True
                
            else:
                self.pioche_valide = False



    def sarreter(self):

        Joueur.sarreter(self)

        if self.finish:

            if self.pioche == None:
                self.client.send_decision(False, self.mise.get_value(),
                                          self.a_splite)
                sleep(.5)
                self.client.stop_playing()
                #TODO : il faut envoyer l'etat, pour savoir quand on s'est
                #arreter apres le premier split
                #ou alors il faut passer un entier (0: pas de split) indiquant
                #quand s'arrete la premier main


        

    def jouer(self, carte_adversaire, compteur):
        """
            carte_adversaire : Carte visible de l'adversaire (soit la banque,
                soit un autre joueur)
                
            l_cartes_passees : la liste des cartes qui sont deja passees et qui
                ne peuvent donc pas retomber

            ne renvoie rien, effectue la decision en place

            cette methode est appelee en interne, n'a pas a etre appelee de
            l'exterieur
            voir commencer_tour
        """


        #normalement, la prise de decision est tres rapide, donc pas besoin
        # de faire un thread pour ca

        if      not self.a_splite:  m = self
        elif    self.playing_1:     m = self.jeu_1
        else:                       m = self.jeu_2

        
        can_double = (not self.a_splite and not self.a_double
                      and len(self.contenu) == 2)
        can_split = (can_double and self.contenu[0] == self.contenu[1])

        decision = self.fct_decision(m, carte_adversaire, compteur, can_split,
                                     can_double)
        
        if decision == pdd.CONTINUER:
            self.piocher()
        elif decision == pdd.ARRETER:
            self.sarreter()
        elif decision == pdd.SPLITTER:
            self.splitter()
        elif decision == pdd.DOUBLER:
            self.doubler()
        else:
            raise (ValueError("la decision " + str(decision)
                              + " n'est pas reconnue"))



class Banque(JoueurOrdi):
    """
        objet graphique representant la banque
    """

    def __init__(self, position, pioche):
        """
            position : couple (x, y) qui est le coin haut gauche de l'image qui
                va etre affichee

            pioche : DeckGraphique (ou juste deck ???) dans lequel on va piocher

        """

        ## ----------------- TODO ----------------------------------##
        # reflechir si on a besoin en argument d'un DeckGraphique ou
        # seulement d'un Deck...
        ## ----------------------------------------------------------##

        JoueurOrdi.__init__(self, position, pioche, 0, identifier="banque",
                            fct_decision=pdd.decision_banque)

        self.sleep_time_before_playing = 0.5 #second
        self.begin = -1

    def jouer(self, *args, **kargs):
        if self.begin == -1:
            self.set_face_cachee([])
            self.begin = clock()
        elif clock() - self.begin > self.sleep_time_before_playing:
            JoueurOrdi.jouer(self, *args, **kargs)




class JoueurDistant(Joueur):

    REFRESH_PERIOD = 2. #seconds

    def __init__(self, position, serveur_local=None):

        """

                serveur local sert a indiquer ou les cartes sont piochees
                (en local ou en distant)
                si serveur local == None, alors les cartes sont piochees
                en distant. Sinon, serveur_local doit etre l'instance de Serveur
                avec laquelle il faut demander les cartes qui ont ete piochees
        """

        self.client = Client(PORT, IP_SERVEUR)

        self.serveur_local = serveur_local

        if serveur_local == None:
            c1 = Carte(AS, PIQUE) #on s'en fout, elle apparait face cachee
            while True:
                c2 = self.client.opponent_card()
                if c2 != None : break
                
        else:
            #attention, ceci est bloquant tant que le client n'a rien demande
            #TODO :s'arranger pour que le serveur ait un "buffer" qui ne bloque
            #pas l'execution
            while 1:
                try:
                    print "donnees en local", serveur_local.cartes_donnees
                    c1, c2 = serveur_local.cartes_donnees[:2]
                    break
                except ValueError as e:
                    sleep(.5)
                    

        Joueur.__init__(self, position, None, VERTICAL, None,
                        carte_ini=[c1, c2], face_cachee=[0])

        self.last_refresh = clock()

        self.doit_piocher = 0


    def reconstruire(self):
        """
            methode a appeler pour reconstuire le joueur a partir de ce qui a
            ete fait a l'autre bout

        """

        if self.serveur_local == None:
            split, r = self.client.end_turn_state()
            if split :
                # -------------------------   TODO ----------------------
                pass
        return


    def update(self, other_comp):

        r = Joueur.update(self, other_comp)

        #if self.doit_piocher > 0:
        #    self.piocher()

        if self.finish or clock() - self.last_refresh < self.REFRESH_PERIOD:
            return r

        self.last_refresh = clock()

        #si on tourne sur le client
        if self.serveur_local == None and not self.finish:

            if self.client.human_is_finished():

                sleep(.2)
        
                end = self.client.end_turn_state()
                if end[0]: #si on a fini
                    self.contenu = end[1:]
                    self.sarreter()

        
        elif self.serveur_local.fin_manche and not self.finish:
            self.sarreter()
            print "j'ai fini ! "

        return r
            


class ServeurManager(GUIComponent):
    """
        s'occupe de coordonner les donnees que le serveur peut envoyer
        avec les vraies donneees
    """

    def __init__(self, serveur, arbitre, i=0):

        GUIComponent.__init__(self, 0, (0, 0), (0, 0), [], [])

        self.serveur = serveur

        self.arbitre = arbitre
        self.i = i

        self.serveur.set_opponent_card(self.arbitre.liste_joueur[i].contenu[1])


    def update(self, other_comp):

        j = self.arbitre.liste_joueur[self.i]

        self.serveur.human_finish = k.finished
        self.serveur.cartes_du_serveur = self.serveur_format(j)


        return [self]


    def serveur_format(player):

        if isinstance(player, JoueurSplitte) or player.a_splite:
            return [len(player.jeu_1),
                    player.jeu_1.contenu + player.jeu_2.contenu]

        return [0, player.contenu]

    
        

    

        

