from pygame import *
from pygame.locals import *


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


    def __init__(self, position, pioche):
        """
            cf Banque pour les parametres...
        """

        MainGraphique.__init__(self, [pioche.piocher(), pioche.piocher()],
                               position)



class JoueurHumain(Joueur):

    #TODO reflechir a comment cette methode jouer est appelee
    # par les boutons quand on clique dessus ?
    def jouer(self, action):
        #TODO effectuer l'action demandee !
        pass


class JoueurOrdi(Joueur):

    def jouer(self, carte_adversaire, l_cartes_passees):
        """
            carte_adversaire : Carte visible de l'adversaire (soit la banque,
                soit un autre joueur)
                
            l_cartes_passees : la liste des cartes qui sont deja passees et qui
                ne peuvent donc pas retomber

            l'arbitre se chargera d'appeler cette fonction avec les bons
            arguments
        """


        #TODO : aller chercher le code intelligent ici !!!
        #voir s'il ne vaut mieux pas lancer un thread pour prevenir d'un temps
        # de reflexion... ne serait-ce que pour faire plaisir au prof qui va
        #lire ce code...
