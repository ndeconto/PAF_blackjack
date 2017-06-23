from pygame import *
from pygame.locals import *
from sys import path
path.append("..")
import Prise_De_Decision as pdd

from time import clock

from GUI_cards_img import *



class Joueur(MainGraphique):
    """
        objet graphique representant un joueur, ie sa main et ses actions de jeu
    """


    def __init__(self, position, pioche, sens, identifier=""):
        """
            cf Banque pour les parametres...
        """

        MainGraphique.__init__(self, [pioche.piocher(), pioche.piocher()],
                               position, sens=sens, identifier=identifier,
                               face_cachee=[0] if identifier=="IA" else [])


        self.pioche = pioche

        #si le joueur a commence son tour
        self.playing = False

        #si le joueur a fini de joueur
        self.finish = False


    def commencer_tour(self):
        self.playing = True


    def piocher(self):
        """
            pioche une carte dans la pioche et la rajoute dans la main
        """
        if not self.finish:
            self.ajouter(self.pioche.piocher())


    def splitter(self):
        #TODO a implementer !
        return

    def doubler(self):
        #TODO a implementer !
        return


    def sarreter(self):
        """
            pour terminer son tour
        """
        self.playing = False
        self.finish = True


    def a_fini(self):
        """
            renvoie vrai si le joueur a terminer son tour (ie il s'est arrete)
            faux s'il va encore effectuer des actions
        """

        return self.finish

    




class JoueurHumain(Joueur):


    def __init__(self, position, pioche, identifier=""):

        Joueur.__init__(self, position, pioche, VERTICAL, identifier)


    

class JoueurOrdi(Joueur):


    def __init__(self, position, pioche, identifier="", fct_decision=None):
        """
            fct_decision : fonction qui est appelee pour decider quoi jouer
            cette fonction doit prendre en parametre la main du joueur ordi,
            la carte de l'adversaire et la liste des cartes deja tombees
            et renvoyer l'une des constantes pdd.CONTINUER, ...

            pour les autres parametres, c'est comme pour le reste...
        """

        Joueur.__init__(self, position, pioche, VERTICAL, identifier)

        #temps entre deux decisions en secondes
        self.period = 1
        self.derniere_action = clock()

        #
        if fct_decision == None: self.fct_decision = pdd.decision_banque
        else : self.fct_decision = fct_decision




    def update(self, other_components):
        r = Joueur.update(self, other_components)

        if self.playing and (clock() - self.derniere_action > self.period):

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

        

    def jouer(self, carte_adversaire, l_cartes_passees):
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

        decision = self.fct_decision(self, carte_adversaire, l_cartes_passees)


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

        JoueurOrdi.__init__(self, position, pioche, identifier="banque",
                            fct_decision=pdd.decision_banque)

