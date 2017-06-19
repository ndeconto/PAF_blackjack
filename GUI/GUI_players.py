from pygame import *
from pygame.locals import *


from time import clock

from GUI_cards_img import *



class Banque(MainGraphique):
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

        MainGraphique.__init__(self, [pioche.piocher(), pioche.piocher()],
                               position, face_cachee = [0])


    def jouer(self):
        pass #TODO : a implementer




class Joueur(MainGraphique):
    """
        objet graphique representant un joueur, ie sa main et ses actions de jeu
    """


    def __init__(self, position, pioche, sens, identifier=""):
        """
            cf Banque pour les parametres...
        """

        MainGraphique.__init__(self, [pioche.piocher(), pioche.piocher()],
                               position, sens=sens, identifier=identifier)


        self.pioche = pioche

        #cf methode a_fini pour la signification de cet attribut
        self.finish = False


    def piocher(self):
        """
            pioche une carte dans la pioche et la rajoute dans la main
        """
        self.ajouter(self.pioche.piocher())


    def sarreter(self):
        """
            pour terminer son tour
        """
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


    def __init__(self, position, pioche, identifier=""):

        Joueur.__init__(self, position, pioche, VERTICAL, identifier)

        #boolean indiquant si l'ordi est en train de jouer ou non
        self.playing = False

        #temps entre deux decisions en secondes
        self.period = 1
        self.derniere_action = clock()




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


    def commencer_tour(self):
        """
            demarre le tour de jeu du joueur ordinateur
            ie apres l'appel de cette methode, le joueurOrdi va prendre des
            decisions de maniere periodique, jusqu'a s'arreter
        """

        self.playing = True


    def arreter_tour(self):
        self.playing = False

        

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


        #TODO : aller chercher le code intelligent ici !!!
        #voir s'il ne vaut mieux pas lancer un thread pour prevenir d'un temps
        # de reflexion... ne serait-ce que pour faire plaisir au prof qui va
        #lire ce code...

        self.piocher()
